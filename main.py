import yaml
import json
from pathlib import Path
import argparse

# defaults
GATEWAY = "10.100.100.1"
vm_limit_count = 20
exists_names = []
exists_ip = []
exists_ids = []

# parse
parser = argparse.ArgumentParser(description="CLI input")
parser.add_argument("--vm-count", type=int, default=1, help="Количество vm по умолчанию: 1)")
args = parser.parse_args()

# path for file terrafrorm.tfvars.json
file_path = Path("terraform/terraform.tfvars.json")

# pools
IP_POOL = []
for host in range(10, 21):
    IP_POOL.append(f"10.100.100.{host}")

ID_POOL = []
id_start, id_max = 2000, 2020
for vm_id in range (id_start, id_max + 1):
    ID_POOL.append(vm_id)


# read files
with open("blueprints/postgresql/blueprint.yml") as f:
    data = yaml.safe_load(f)

if file_path.exists():
    with open("terraform/terraform.tfvars.json", "r", encoding="utf-8") as f:
        f_tfvars = json.load(f)

# --- NAME ---
# generator name
#check name 

if file_path.exists():
    for vm in f_tfvars["instances"].values():
        exists_names.append(vm["name"])
base_name = data["name"]

# --- IP ---
# check ip

if file_path.exists():
    for vm in f_tfvars['instances'].values():
        exists_ip.append(vm["vm_ipv4"])

# --- ID ---
# check id

if file_path.exists():
    for vm in f_tfvars["instances"].values():
        exists_ids.append(vm["vm_id"])

full_list = {
    "instances": {},
    "inbound_rules": data["network"]["inbound_ports"]
}

# append full_list
for _ in range(args.vm_count):
    for vm_count in range(1, vm_limit_count + 1):
        candidate_name = f"{base_name}--{vm_count}"
        if candidate_name not in exists_names:
            free_name = candidate_name
            exists_names.append(free_name)
            break
    for vm_id in ID_POOL:
        if vm_id not in exists_ids:
            free_id = vm_id
            exists_ids.append(free_id)
            break
    for ip in IP_POOL:
        if ip not in exists_ip:
            free_ip = ip
            exists_ip.append(free_ip)
            break
    full_list["instances"][free_name] = {
            "name": free_name,
            "cpu": data['infrastructure']['cpu'],
            "ram_mb": data['infrastructure']['ram_mb'],
            "disk_gb": data['infrastructure']['disk_gb'],
            "vm_id": free_id,
            "vm_ipv4": free_ip,
            "gateway": GATEWAY
        }

# упаковываем в файл .json
with open("terraform/terraform.tfvars.json", "w", encoding="utf-8") as f:
    json.dump(full_list, f, indent=2)

with open("terraform/terraform.tfvars.json", "r", encoding="utf-8") as f:
    print(json.load(f))

if file_path.exists():
    print("tfvars generated successfully")
    print(f'ip address: {free_ip}')
else:
    print("ERROR")