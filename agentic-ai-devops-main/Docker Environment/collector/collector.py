import uuid
import threading
import time
from datetime import datetime
from jenkins_client import fetch_last_build, fetch_console_log

LATEST_FAILURE_EVENT = None
LAST_FAILED_BUILD_NUMBER = None


def capture_failure(build):
    global LATEST_FAILURE_EVENT, LAST_FAILED_BUILD_NUMBER

    build_number = build["number"]

    print(f"🚨 Capturing failure for build #{build_number}")

    try:
        log = fetch_console_log(build_number)
    except Exception as e:
        log = f"Failed to fetch console log: {e}"

    LATEST_FAILURE_EVENT = {
        "event_id": f"evt-{uuid.uuid4()}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "jenkins",
        "ci": {
            "job_name": build["fullDisplayName"],
            "build_id": build_number,
            "result": build["result"],
            "url": build["url"],
        },
        "error": {
            "type": "PIPELINE_FAILURE",
            "raw_log": log
        }
    }

    LAST_FAILED_BUILD_NUMBER = build_number
    print("✅ Failure event stored")


def watcher():
    global LAST_FAILED_BUILD_NUMBER

    print("🟢 Jenkins watcher running...")

    while True:
        try:
            build = fetch_last_build()
            print("DEBUG:", build["result"], build["building"])

            if build["result"] == "FAILURE" and not build["building"]:
                if build["number"] != LAST_FAILED_BUILD_NUMBER:
                    capture_failure(build)

        except Exception as e:
            print("❌ Watcher error:", e)

        time.sleep(5)


def start_watcher():
    print("🚀 Starting Jenkins failure watcher")

    # 🔥 CAPTURE FAILURE IMMEDIATELY ON STARTUP
    try:
        build = fetch_last_build()
        print("Startup build state:", build["result"], build["building"])

        if build["result"] == "FAILURE" and not build["building"]:
            capture_failure(build)

    except Exception as e:
        print("❌ Startup check failed:", e)

    t = threading.Thread(target=watcher, daemon=True)
    t.start()


def get_failed_event():
    if LATEST_FAILURE_EVENT:
        return LATEST_FAILURE_EVENT

    return {
        "status": "ok",
        "message": "No pipeline failure detected"
    }
