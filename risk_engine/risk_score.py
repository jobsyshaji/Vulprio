import json
import pandas as pd

print("[*] Loading vulnerability intelligence data...")

# Load vulnerability data
with open("data/vulnerabilities.json") as f:
    vulnerabilities = json.load(f)

df = pd.DataFrame(vulnerabilities)

# If no vulnerabilities found
if df.empty:
    print("No vulnerabilities found.")
    exit()

# Add exploit availability column
df["exploit_available"] = 1

# Add exposure column
df["exposure"] = 1

# Calculate custom risk score
df["risk_score"] = (
    df["cvss"] * 0.5 +
    df["exploit_available"] * 0.3 +
    df["exposure"] * 0.2
)

# Sort vulnerabilities by risk score
df_sorted = df.sort_values(by="risk_score", ascending=False)

# Save prioritized results
df_sorted.to_csv("data/prioritized_vulnerabilities.csv", index=False)

print("[+] Risk prioritization complete.")
print("[+] Output saved → data/prioritized_vulnerabilities.csv")