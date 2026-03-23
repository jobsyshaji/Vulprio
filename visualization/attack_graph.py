import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

print("[*] Loading vulnerability data...")

df = pd.read_csv("data/prioritized_vulnerabilities.csv")

# keep only real CVE IDs
df = df[df["cve"].astype(str).str.contains("CVE", na=False)]

# keep top 6 highest risk vulnerabilities
df = df.sort_values("risk_score", ascending=False).head(6)

# -----------------------------
# Create Attack Path Graph
# -----------------------------

G = nx.DiGraph()

attacker = "Attacker"
G.add_node(attacker)

pos = {attacker: (0,0)}

services = []

y_offset = 0

for _, row in df.iterrows():

    service = row["service"]
    cve = row["cve"]
    risk = round(row["risk_score"],2)

    services.append(service)

    service_node = service
    vuln_node = cve

    pos[service_node] = (2, -y_offset)
    pos[vuln_node] = (4, -y_offset)

    G.add_node(service_node)
    G.add_node(vuln_node)

    G.add_edge(attacker, service_node)
    G.add_edge(service_node, vuln_node, weight=risk)

    y_offset += 2


# -----------------------------
# Create Combined Visualization
# -----------------------------

fig = plt.figure(figsize=(12,8))

# Small attack graph (top)
ax1 = plt.subplot2grid((3,1),(0,0))

nx.draw(
    G,
    pos,
    ax=ax1,
    with_labels=True,
    node_size=2000,
    node_color=[
        "red" if node=="Attacker"
        else "lightblue" if node in services
        else "orange"
        for node in G.nodes
    ],
    font_size=9
)

edge_labels = nx.get_edge_attributes(G,"weight")
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,ax=ax1)

ax1.set_title("Attack Path Visualization")


# -----------------------------
# Risk Score Bar Chart
# -----------------------------

ax2 = plt.subplot2grid((3,1),(1,0), rowspan=2)

labels = df["cve"]
scores = df["risk_score"]

ax2.barh(labels, scores)

ax2.set_xlabel("Risk Score")
ax2.set_title("Top Vulnerabilities by Risk Score")

plt.tight_layout()

plt.savefig("docs/vulnerability_risk_dashboard.png")

plt.show()

print("[+] Dashboard chart generated → docs/vulnerability_risk_dashboard.png")