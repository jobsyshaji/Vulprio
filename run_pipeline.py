import subprocess
import sys

def run_script(script_path):
    print(f"\n[+] Running {script_path}...\n")

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(f"[!] Error while running {script_path}")
        print(result.stderr)
        exit()


def main():

    print("\n===== Vulnerability Intelligence Pipeline =====\n")

    # Step 1 - Run Nmap scanner
    run_script("scanner/nmap_automation.py")

    # Step 2 - Map CVEs
    run_script("vuln_intel/cve_mapper.py")

    # Step 3 - Risk scoring
    run_script("risk_engine/risk_score.py")

    # Step 4 - Generate visualization
    run_script("visualization/vulnerability_dashboard_chart.py")

    print("\n✓ Pipeline completed successfully.\n")
    print("You can now start the dashboard using:\n")
    print("python dashboard/app.py\n")


if __name__ == "__main__":
    main()