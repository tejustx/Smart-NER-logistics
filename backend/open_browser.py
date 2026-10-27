"""
Smart NER Logistics Platform - Browser Launcher Helper
Waits for FastAPI server to become healthy before launching the user's default browser.
Prevents 'connection refused' errors on server startup.
"""
import sys
import time
import urllib.request
import webbrowser


def main():
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    health_url = target_url.rstrip("/") + "/api/health"

    # Poll for up to 20 seconds (50 attempts * 0.4s)
    for _ in range(50):
        time.sleep(0.4)
        try:
            req = urllib.request.Request(
                health_url,
                headers={"User-Agent": "SmartNER-BrowserLauncher/1.0"}
            )
            with urllib.request.urlopen(req, timeout=1) as resp:
                if resp.status == 200:
                    webbrowser.open(target_url)
                    return
        except Exception:
            pass

    # Fallback: if server took longer than 20s, launch anyway
    webbrowser.open(target_url)


if __name__ == "__main__":
    main()
