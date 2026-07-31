#!/usr/bin/env python3
import json
import urllib.request

# 1. Fetch IP list from your 3rd party API or Node-RED wrapper endpoint
API_URL = "http://localhost:1880/api/devices"

def get_inventory():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Ansible-Inventory"})
    with urllib.request.urlopen(req) as response:
        devices = json.loads(response.read().decode())

    inventory = {
        "_meta": {"hostvars": {}},
        "all": {"hosts": []},
        "knot_gateways": {"hosts": []}
    }

    for dev in devices:
        # Expecting dev = {"ip": "10.8.0.12", "id": "knot-01"}
        host_key = dev.get("id", dev["ip"])
        inventory["all"]["hosts"].append(host_key)
        inventory["knot_gateways"]["hosts"].append(host_key)

        inventory["_meta"]["hostvars"][host_key] = {
            "ansible_host": dev["ip"]
        }

    return inventory

if __name__ == "__main__":
    print(json.dumps(get_inventory()))
