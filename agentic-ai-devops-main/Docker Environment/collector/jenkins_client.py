import requests

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "agentic-ai-devops-pipeline"

# If Jenkins needs auth, uncomment:
# AUTH = ("admin", "password")
AUTH = None


def fetch_last_build():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"
    resp = requests.get(url, auth=AUTH, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_console_log(build_number):
    url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/consoleText"
    resp = requests.get(url, auth=AUTH, timeout=10)
    resp.raise_for_status()
    return resp.text
