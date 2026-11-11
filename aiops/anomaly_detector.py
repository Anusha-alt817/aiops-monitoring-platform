import json
import math
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

QUERIES = {
    "CPU Usage": '100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))',
    "Memory Usage": '100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))',
    "Disk Usage": '100 * (1 - (node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} / node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}))',
    "API P95 Latency": 'histogram_quantile(0.95, sum by (endpoint, le) (rate(banking_app_request_latency_seconds_bucket[5m])))',
    "HTTP 5xx Errors": 'sum(increase(banking_app_requests_total{status=~"5.."}[30m]))'
}

THRESHOLDS = {
    "CPU Usage": 80,
    "Memory Usage": 85,
    "Disk Usage": 85,
    "API P95 Latency": 1
}


def get_metrics(name, query):
    try:
        params = urllib.parse.urlencode({"query": query})
        url = f"{PROMETHEUS_URL}?{params}"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        return data["data"]["result"]

    except Exception as error:
        print(f"{name}: Unable to retrieve metric: {error}")
        return None


def analyze_metrics():
    print("\n========== AIOPS ANOMALY DETECTION ==========\n")

    metric_results = []
    incidents = []
    unavailable = []

    for name, query in QUERIES.items():
        results = get_metrics(name, query)

        if results is None or not results:
            message = f"{name}: Metric unavailable"

            unavailable.append(message)
            metric_results.append({
                "name": name,
                "value": None,
                "unit": "seconds" if name == "API P95 Latency" else None,
                "threshold": THRESHOLDS.get(name),
                "status": "INSUFFICIENT_DATA",
                "reason": message
            })

            print(message)
            continue

        for result in results:
            labels = result.get("metric", {})
            endpoint = labels.get("endpoint")

            try:
                value = float(result["value"][1])
            except (KeyError, IndexError, TypeError, ValueError):
                value = float("nan")

            target = f" ({endpoint})" if endpoint else ""

            if not math.isfinite(value):
                message = f"{name}{target}: Unavailable (NaN or infinite)"
                unavailable.append(message)

                metric_results.append({
                    "name": name,
                    "endpoint": endpoint,
                    "value": None,
                    "threshold": THRESHOLDS.get(name),
                    "status": "INSUFFICIENT_DATA",
                    "reason": message
                })

                print(message)
                continue

            threshold = THRESHOLDS.get(name)

            if name == "HTTP 5xx Errors":
                status = "ALERT" if value > 0 else "OK"
            elif threshold is not None:
                status = "ALERT" if value > threshold else "OK"
            else:
                status = "OK"

            metric_results.append({
                "name": name,
                "endpoint": endpoint,
                "value": round(value, 2),
                "threshold": threshold,
                "status": status
            })

            print(f"{name}{target}: {value:.2f}")

            if status == "ALERT":
                if name == "HTTP 5xx Errors":
                    incidents.append(
                        "Application errors detected. Check application logs."
                    )
                else:
                    incidents.append(
                        f"{name}{target} is above threshold ({threshold})."
                    )

    if incidents:
        overall_status = "ALERT"
    elif unavailable:
        overall_status = "INSUFFICIENT_DATA"
    else:
        overall_status = "OK"

    print("\n========== INCIDENT REPORT ==========\n")

    if incidents:
        for incident in incidents:
            print(f"[ALERT] {incident}")
    elif unavailable:
        print("[INSUFFICIENT_DATA] Some metrics could not be evaluated.")
    else:
        print("[OK] No threshold-based anomalies detected.")

    print("\n========== RECOMMENDATIONS ==========\n")

    if incidents:
        print("- Inspect application and system logs.")
        print("- Check resource utilization and recent changes.")
        print("- Validate the cause before taking corrective action.")
    elif unavailable:
        print("- Generate traffic to restore missing application metrics.")
        print("- Verify Prometheus targets and metric collection.")
    else:
        print("- Continue monitoring CPU, memory, disk and API latency.")

    report = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "overall_status": overall_status,
        "metric_count": len(metric_results),
        "alert_count": len(incidents),
        "insufficient_data_count": len(unavailable),
        "metrics": metric_results,
        "alerts": incidents,
        "unavailable_metrics": unavailable
    }

    output_file = REPORT_DIR / "metrics_analysis.json"

    with output_file.open("w") as file:
        json.dump(report, file, indent=4)

    print(f"\nStructured metrics report saved: {output_file}")
    print("\nAnalysis complete. Human validation is required.")


if __name__ == "__main__":
    analyze_metrics()
