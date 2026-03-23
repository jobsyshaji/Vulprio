import json
import requests

API_KEY = "PUHMF7EDQ8WXEDRPYQN18GD00GUK0KM22GRFUQCX97QFXFSGL0JCKCEFP3CF5NYO"

url = "https://vulners.com/api/v3/search/lucene/"

headers = {
    "X-Api-Key": API_KEY
}

# Load scan results
with open("data/scan_results.json") as f:
    scan_data = json.load(f)

vulnerabilities = []

print("[*] Fetching vulnerability intelligence...")

for item in scan_data:
    service = item.get("service")
    version = item.get("version")

    if service and version:
        query = f"{service} {version}"

        params = {
            "query": query,
            "size": 3
        }

        try:
            response = requests.get(url, headers=headers, params=params)

            data = response.json()

            if "data" in data and "search" in data["data"]:
                results = data["data"]["search"]

                for r in results:
                    source = r.get("_source", {})

                    vulnerabilities.append({
                        "ip": item["ip"],
                        "port": item["port"],
                        "service": service,
                        "cve": source.get("id"),
                        "cvss": source.get("cvss", {}).get("score", 0),
                        "title": source.get("title")
                    })

        except Exception as e:
            print(f"[!] Error querying {query}: {e}")

# Save results
with open("data/vulnerabilities.json", "w") as f:
    json.dump(vulnerabilities, f, indent=4)

print("[+] Vulnerability mapping complete → data/vulnerabilities.json")