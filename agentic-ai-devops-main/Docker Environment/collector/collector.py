import uuid
import threading
import time
from datetime import datetime

from jenkins_client import fetch_last_build, fetch_console_log

LATEST_FAILURE_EVENT = None


def capture_failure(build):
    global LATEST_FAILURE_EVENT

    log = fetch_console_log()

    LATEST_FAILURE_EVENT = {
        "event_id": f"evt-{uuid.uuid4()}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "jenkins",
        "ci": {
            "job_name": build.get("fullDisplayName"),
            "build_id": build.get("number"),
            "result": build.get("result"),
            "url": build.get("url"),
        },
        "error": {
            "type": "PIPELINE_FAILURE",
            "raw_log": log,
        },
    }

    print(f"🚨 FAILURE CAPTURED: build #{build.get('number')}")


def watcher():
    print("🟢 Jenkins failure watcher started")

    while True:
        try:
            build = fetch_last_build()

            if not build.get("building") and build.get("result") == "FAILURE":
                capture_failure(build)

        except Exception as e:
            print("❌ Watcher error:", e)

        time.sleep(10)


def start_watcher():
    # 🔥 BOOTSTRAP: capture existing failure at startup
    try:
        build = fetch_last_build()
        if not build.get("building") and build.get("result") == "FAILURE":
            capture_failure(build)
    except Exception as e:
        print("❌ Bootstrap error:", e)

    threading.Thread(target=watcher, daemon=True).start()


def get_failed_event():
    return LATEST_FAILURE_EVENT or {
        "status": "no_failed_build_detected"
    }
