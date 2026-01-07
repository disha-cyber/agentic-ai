import requests

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "agentic-ai-devops-pipeline"

def fetch_last_build():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def fetch_console_log():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/consoleText"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text
