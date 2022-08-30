import requests
import sys
from datetime import datetime

github_api = "https://api.github.com/repos"
packages = ["simplejson/simplejson", "ijl/orjson", "ultrajson/ultrajson", "Tencent/rapidjson"]

latest_benchmark = datetime.strptime(
    requests.get(f"{github_api}/fuchsde/orjson-benchmark/actions/workflows/benchmark.yml/runs")
    .json()
    .get("workflow_runs")[0]["run_started_at"],
    "%Y-%m-%dT%H:%M:%SZ",
)

release_dates = [
    datetime.strptime(
        requests.get(f"{github_api}/{package}/releases").json()[0].get("published_at"), "%Y-%m-%dT%H:%M:%SZ"
    )
    for package in packages
]

print(f"Latest Benchmark: {latest_benchmark}")
for date in release_dates:
    print(f"Release : {date} - {latest_benchmark < date}")

if any([latest_benchmark < date for date in release_dates]):
    response = requests.post(
        "https://api.github.com/repos/fuchsde/orjson-benchmark/actions/workflows/benchmark.yml/dispatches",
        headers={"Authorization": f"token {sys.argv[1]}", "Accept": "application/vnd.github.v3+json"},
        json={"ref": "refs/heads/master"},
    )
    print(response.text)