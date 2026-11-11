
import subprocess
from datetime import datetime

CONTAINER_NAME = "banking-container"


def get_docker_logs():
    try:
        result = subprocess.run(
            ["sudo", "docker", "logs", "--since", "30m", CONTAINER_NAME],
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0:
            print("Unable to retrieve Docker logs:")
            print(result.stderr)
            return []

        return (result.stdout + result.stderr).splitlines()

    except Exception as error:
        print(f"Log retrieval failed: {error}")
        return []


def analyze_logs(logs):
    errors = []
    warnings = []

    for line in logs:
        if " ERROR " in line:
            errors.append(line)

        elif " WARNING " in line:
            warnings.append(line)

    return errors, warnings


def main():
    print("\n========== AIOPS LOG ANALYZER ==========")
    print(f"Analysis time: {datetime.now()}")
    print(f"Container: {CONTAINER_NAME}")

    logs = get_docker_logs()

    if not logs:
        print("\nNo logs found or Docker log retrieval failed.")
        return

    errors, warnings = analyze_logs(logs)

    print(f"\nTotal log lines analyzed: {len(logs)}")
    print(f"Errors detected: {len(errors)}")
    print(f"Warnings detected: {len(warnings)}")

    print("\n========== ERROR DETAILS ==========")

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
    else:
        print("No application errors found.")

    print("\n========== WARNING DETAILS ==========")

    if warnings:
        for warning in warnings:
            print(f"[WARNING] {warning}")
    else:
        print("No application warnings found.")

    print("\n========== ANALYSIS SUMMARY ==========")

    if errors:
        print("Critical finding: Application errors require investigation.")

    if warnings:
        print("Performance finding: Warning messages require investigation.")

    if not errors and not warnings:
        print("No ERROR or WARNING messages detected.")

    print("\nLog analysis completed. Human validation is required.")


if __name__ == "__main__":
    main()
