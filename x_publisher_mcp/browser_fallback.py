"""Browser fallback planning and optional Edge automation."""

from __future__ import annotations

import platform
import time
from typing import Any

from .post_text import build_intent_url, validate_post


class BrowserFallbackError(RuntimeError):
    """Raised when browser automation cannot complete safely."""


def _truncate(value: str, limit: int = 80) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _normalize_account(username: str | None) -> str | None:
    if not username:
        return None
    return username.strip().lstrip("@") or None


def build_browser_fallback_plan(
    text: str,
    *,
    account_username: str | None = None,
    repost_after_post: bool = False,
    edge_profile_hint: str = "Work",
) -> dict[str, Any]:
    result = validate_post(text)
    if not result.valid:
        return {
            "status": "invalid_post",
            "message": "Post text is too long for X.",
            "validation": result.to_dict(),
        }
    account = _normalize_account(account_username)
    summary = browser_confirmation_summary(text, account, repost_after_post)
    fallback = {
        "kind": "browser_post",
        "requires_signed_in_browser": True,
        "browser": "Microsoft Edge",
        "edge_profile_hint": edge_profile_hint,
        "account_username": account,
        "repost_after_post": repost_after_post,
        "text": result.text,
        "composer_url": build_intent_url(result.text).replace("twitter.com", "x.com", 1),
        "steps": [
            "Focus the signed-in Microsoft Edge profile.",
            "Open X home or the prefilled composer.",
            "Paste the exact post text and verify the visible account/text.",
            "Click Post only after verification.",
        ],
    }
    if repost_after_post:
        fallback["steps"].extend(
            [
                "Open the newly posted item from the target profile.",
                "Click the repost control on that exact post.",
                "Confirm Repost and verify the action changes to Reposted.",
            ]
        )
    return {
        "status": "browser_fallback_plan",
        "message": "Browser fallback is available for a locally signed-in Edge session.",
        "required_confirmation": summary,
        "browser_fallback": fallback,
        "validation": result.to_dict(),
    }


def browser_confirmation_summary(text: str, account_username: str | None, repost_after_post: bool) -> str:
    account = f"@{account_username}" if account_username else "visible_account"
    return f"execute_browser_fallback account={account} repost={repost_after_post} text={_truncate(text)}"


def execute_browser_fallback_plan(
    text: str,
    *,
    account_username: str | None = None,
    repost_after_post: bool = False,
    edge_profile_hint: str = "Work",
    confirmation: str | None = None,
    execute: bool = False,
) -> dict[str, Any]:
    account = _normalize_account(account_username)
    plan = build_browser_fallback_plan(
        text,
        account_username=account,
        repost_after_post=repost_after_post,
        edge_profile_hint=edge_profile_hint,
    )
    if plan["status"] != "browser_fallback_plan":
        return plan
    required = plan["required_confirmation"]
    if confirmation != required:
        return {
            "status": "confirmation_required",
            "message": "Browser publishing changes public X state and requires exact confirmation.",
            "required_confirmation": required,
            "browser_fallback": plan["browser_fallback"],
        }
    if not execute:
        return {
            "status": "browser_execution_preview",
            "message": "Confirmation matched. Pass execute=True to operate the local Edge browser.",
            "required_confirmation": required,
            "browser_fallback": plan["browser_fallback"],
        }
    if not account:
        return {
            "status": "account_required",
            "message": "account_username is required before executing so the posted item can be verified on the target profile.",
            "browser_fallback": plan["browser_fallback"],
        }
    try:
        result = run_edge_post_workflow(
            text,
            account_username=account,
            repost_after_post=repost_after_post,
            edge_profile_hint=edge_profile_hint,
        )
    except BrowserFallbackError as exc:
        return {
            "status": "browser_error",
            "message": str(exc),
            "browser_fallback": plan["browser_fallback"],
        }
    return {
        "status": "ok",
        "message": "Browser fallback completed.",
        "result": result,
        "browser_fallback": plan["browser_fallback"],
    }


def run_edge_post_workflow(
    text: str,
    *,
    account_username: str,
    repost_after_post: bool = False,
    edge_profile_hint: str = "Work",
    page_wait_seconds: float = 8.0,
) -> dict[str, Any]:
    if platform.system() != "Windows":
        raise BrowserFallbackError("Browser fallback execution currently requires Windows desktop automation.")
    try:
        import pyperclip
        from pywinauto import Application, keyboard, mouse
        from pywinauto.findwindows import find_windows
    except ImportError as exc:
        raise BrowserFallbackError(
            "Missing browser automation dependencies. Install pywinauto and pyperclip in the active Python environment."
        ) from exc

    handles = find_windows(title_re=rf".*{edge_profile_hint}.*Microsoft.*Edge.*", class_name="Chrome_WidgetWin_1")
    if not handles:
        raise BrowserFallbackError(f"No Microsoft Edge window found for profile hint {edge_profile_hint!r}.")

    import ctypes

    hwnd = handles[0]
    user32 = ctypes.windll.user32
    user32.ShowWindow(hwnd, 3)
    time.sleep(0.2)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)

    app = Application(backend="uia").connect(handle=hwnd)
    win = app.window(handle=hwnd)
    win.set_focus()
    keyboard.send_keys("{ESC}")
    _navigate(win, keyboard, pyperclip, "https://x.com/home", page_wait_seconds)

    post_button = _find_home_post_button(win)
    if post_button is None:
        raise BrowserFallbackError("Could not find the X home composer Post button.")
    br = post_button.rectangle()
    mouse.click(button="left", coords=(br.left - 270, max(80, br.top - 95)))
    time.sleep(0.3)
    pyperclip.copy(text)
    keyboard.send_keys("^v")
    time.sleep(1.0)
    if not _find_exact_text(win, text):
        raise BrowserFallbackError("Exact post text was not visible in the composer, so posting was aborted.")
    post_button.click_input()
    time.sleep(page_wait_seconds)

    profile_url = f"https://x.com/{account_username}"
    _navigate(win, keyboard, pyperclip, profile_url, page_wait_seconds)
    post_rect = _find_exact_post_rect(win, text)
    if post_rect is None:
        raise BrowserFallbackError(f"Could not verify the exact post on @{account_username}.")

    response: dict[str, Any] = {
        "posted": True,
        "reposted": False,
        "account_username": account_username,
        "profile_url": profile_url,
    }
    if repost_after_post:
        _repost_exact_post(win, post_rect, mouse)
        time.sleep(4.0)
        if not _find_reposted_button(win, post_rect):
            raise BrowserFallbackError("Repost confirmation was clicked, but the exact post did not change to Reposted.")
        response["reposted"] = True
    return response


def _navigate(win: Any, keyboard: Any, pyperclip: Any, url: str, wait_seconds: float) -> None:
    win.set_focus()
    keyboard.send_keys("^l")
    time.sleep(0.1)
    pyperclip.copy(url)
    keyboard.send_keys("^v")
    keyboard.send_keys("{ENTER}")
    time.sleep(wait_seconds)


def _find_home_post_button(win: Any) -> Any | None:
    candidates = []
    for button in win.descendants(control_type="Button"):
        name = (button.window_text() or "").strip()
        if name in {"Post", "Tweet"}:
            rect = button.rectangle()
            if 80 <= rect.top <= 350:
                candidates.append((rect.top, rect.left, button))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][2]


def _find_exact_text(win: Any, text: str) -> bool:
    needle = text.strip()
    for control in win.descendants():
        name = (control.window_text() or "").strip()
        if needle in name:
            return True
    return False


def _find_exact_post_rect(win: Any, text: str) -> Any | None:
    needle = text.strip()
    fallback = None
    for control in win.descendants():
        name = (control.window_text() or "").strip()
        if needle not in name:
            continue
        rect = control.rectangle()
        if control.friendly_class_name() == "GroupBox":
            return rect
        fallback = fallback or rect
    return fallback


def _repost_exact_post(win: Any, post_rect: Any, mouse: Any) -> None:
    candidates = []
    for button in win.descendants(control_type="Button"):
        name = (button.window_text() or "").strip()
        if "Repost" not in name:
            continue
        rect = button.rectangle()
        if post_rect.top - 10 <= rect.top <= post_rect.bottom + 40:
            candidates.append((abs(rect.top - (post_rect.bottom - 20)), button))
    if not candidates:
        raise BrowserFallbackError("Could not find the repost control for the exact post.")
    candidates.sort(key=lambda item: item[0])
    candidates[0][1].click_input()
    time.sleep(1.0)
    for control in win.descendants():
        name = (control.window_text() or "").strip()
        if name == "Repost" and control.friendly_class_name() in {"MenuItem", "Button", "Text"}:
            try:
                control.click_input()
            except Exception:
                rect = control.rectangle()
                mouse.click(button="left", coords=(rect.left + 20, rect.top + 10))
            return
    raise BrowserFallbackError("Could not find the Repost confirmation menu item.")


def _find_reposted_button(win: Any, post_rect: Any) -> bool:
    for button in win.descendants(control_type="Button"):
        name = (button.window_text() or "").strip()
        rect = button.rectangle()
        if "Reposted" in name and post_rect.top - 20 <= rect.top <= post_rect.bottom + 60:
            return True
    return False
