import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def run_script(script_name):
    result = subprocess.run(
        [sys.executable, f"aiops/{script_name}"],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed: {result.stderr}"
        )

    return result.stdout


def generate_report():
    print("\nGenerating centralized incident report...")

    metrics_output = run_script("anomaly_detector.py")
    logs_output = run_script("log_analyzer.py")

    metrics_file = REPORT_DIR / "metrics_analysis.json"

    with metrics_file.open() as file:
        metrics_data = json.load(file)

    alerts = metrics_data["alerts"]
    unavailable = metrics_data["unavailable_metrics"]

    report = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "project": "AI-Powered DevOps Monitoring Platform",
        "status": metrics_data["overall_status"],
        "alert_count": len(alerts),
        "insufficient_data_count": len(unavailable),
        "metrics": metrics_data["metrics"],
        "detected_alerts": alerts,
        "insufficient_data": unavailable,
        "metrics_analysis": metrics_output,
        "log_analysis": logs_output
    }

    json_file = REPORT_DIR / "incident_report.json"

    with json_file.open("w") as file:
        json.dump(report, file, indent=4)

    text_file = REPORT_DIR / "incident_report.txt"

    with text_file.open("w") as file:
        file.write("AI-POWERED DEVOPS INCIDENT REPORT\n")
        file.write("=" * 45 + "\n\n")
        file.write(f"Generated: {report['timestamp']}\n")
        file.write(f"Project: {report['project']}\n")
        file.write(f"Status: {report['status']}\n")
        file.write(f"Alert count: {report['alert_count']}\n")
        file.write(
            f"Unavailable metrics: "
            f"{report['insufficient_data_count']}\n\n"
        )

        file.write("METRIC DETAILS\n")
        file.write("-" * 45 + "\n")

        for metric in report["metrics"]:
            endpoint = metric.get("endpoint")
            target = f" ({endpoint})" if endpoint else ""

            file.write(
                f"{metric['name']}{target}: "
                f"{metric['value']} | "
                f"Status: {metric['status']} | "
                f"Threshold: {metric['threshold']}\n"
            )

        file.write("\nDETECTED ALERTS\n")
        file.write("-" * 45 + "\n")

        if alerts:
            for alert in alerts:
                file.write(f"- {alert}\n")
        else:
            file.write("No metric alerts detected.\n")

        file.write("\nINSUFFICIENT DATA\n")
        file.write("-" * 45 + "\n")

        if unavailable:
            for item in unavailable:
                file.write(f"- {item}\n")
        else:
            file.write("No unavailable metrics.\n")

        file.write("\nAPPLICATION LOG ANALYSIS\n")
        file.write("-" * 45 + "\n")
        file.write(logs_output + "\n")

    print("\nIncident report generated successfully!")
    print(f"Incident status: {report['status']}")
    print(f"Detected alerts: {report['alert_count']}")
    print(
        f"Unavailable metrics: "
        f"{report['insufficient_data_count']}"
    )
    print(f"JSON report: {json_file}")
    print(f"Text report: {text_file}")


if __name__ == "__main__":
    try:
        generate_report()
    except Exception as error:
        print(f"Report generation failed: {error}")
