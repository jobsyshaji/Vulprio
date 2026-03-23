import nmap
import json
import os

print("\n=== Nmap Automated Scanner ===\n")


target = input("Enter target IP or network range (example: 192.168.56.101 or 192.168.56.0/24): ")

scanner = nmap.PortScanner()

print(f"\n[*] Starting scan on {target}...\n")

try:
    scanner.scan(hosts=target, arguments="-sV")

    results = []

    for host in scanner.all_hosts():

        print(f"Host: {host}")
        print(f"State: {scanner[host].state()}")

        for proto in scanner[host].all_protocols():

            ports = scanner[host][proto].keys()

            for port in ports:

                service = scanner[host][proto][port]

                data = {
                    "ip": host,
                    "port": port,
                    "protocol": proto,
                    "service": service["name"],
                    "version": service.get("version", "")
                }

                results.append(data)

                print(
                    f"Port: {port} | Service: {service['name']} | Version: {service.get('version','')}"
                )

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # Save scan results
    with open("data/scan_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("\n[+] Scan completed successfully.")
    print("[+] Results saved to data/scan_results.json\n")

except Exception as e:
    print("\n[!] Scan failed:", e)