"""Launch the kiosk web page full-screen in a locked-down Chromium (Linux devices)."""

from __future__ import annotations

import logging
import os
import subprocess
import time

logger = logging.getLogger(__name__)

_CHROMIUM_FLAGS = (
    "--kiosk",
    "--incognito",
    "--no-first-run",
    "--disable-pinch",
    "--overscroll-history-navigation=0",
    "--disable-features=TranslateUI",
    "--disable-session-crashed-bubble",
    "--disable-infobars",
    "--check-for-update-interval=31536000",
)


class KioskDisplay:
    """Manage a full-screen Chromium instance pointed at the kiosk web page."""

    def __init__(self) -> None:
        self.process: subprocess.Popen[bytes] | None = None
        self._env = {
            "DISPLAY": os.environ.get("DISPLAY", ":0"),
            "XAUTHORITY": os.environ.get("XAUTHORITY", os.path.expanduser("~/.Xauthority")),
        }

    def start(self, url: str = "http://localhost:8080") -> bool:
        if not self._x_server_available():
            logger.warning("no X server; skipping full-screen display")
            return False
        self._kill_existing()
        self.process = subprocess.Popen(
            ["chromium-browser", *_CHROMIUM_FLAGS, url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=self._env,
        )
        logger.info("kiosk display started (pid=%s)", self.process.pid)
        return True

    def stop(self) -> None:
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self._kill_existing()

    def _x_server_available(self) -> bool:
        try:
            result = subprocess.run(
                ["xset", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=self._env,
                check=False,
            )
        except FileNotFoundError:
            return False
        return result.returncode == 0

    @staticmethod
    def _kill_existing() -> None:
        subprocess.run(["pkill", "-f", "chromium.*kiosk"], stderr=subprocess.DEVNULL, check=False)
        time.sleep(1)
