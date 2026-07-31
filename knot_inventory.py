#!/usr/bin/env python3
import json
import urllib.request

API_URL = "http://10.1.0.25:1880/api/devices" # IP address of the server, can't run on local hust as AWX is under kubernetes

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
        host_key = dev.get("id", dev["ip"])
        inventory["all"]["hosts"].append(host_key)
        inventory["knot_gateways"]["hosts"].append(host_key)

        inventory["_meta"]["hostvars"][host_key] = {
            "ansible_host": dev["ip"]
        }

    return inventory

if __name__ == "__main__":
    print(json.dumps(get_inventory()))
