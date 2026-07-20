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
for host in range(10, 29):
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
        tfvars = json.load(f)
else:
    tfvars = {
    "instances": {},
    "inbound_rules": data["network"]["inbound_ports"]
    }


def get_values(f_file, find_text):
    array = []
    for vm in f_file["instances"].values():
        array.append(vm[find_text])
    return array

def get_pool(pool, exists_array):
    for value in pool:
        if value not in exists_array:
            free_value = value
            exists_array.append(free_value)
            return free_value
    return None        
    
exists_names = get_values(tfvars, "name")
exists_ip = get_values(tfvars, "vm_ipv4")
exists_ids = get_values(tfvars, "vm_id")


# append tfvars
for _ in range(args.vm_count):
    base_name = data["name"]
    for vm_count in range(1, vm_limit_count + 1):
        candidate_name = f"{base_name}--{vm_count}"
        if candidate_name not in exists_names:
            free_name = candidate_name
            exists_names.append(free_name)
            break

    free_id = get_pool(ID_POOL, exists_ids)
    free_ip = get_pool(IP_POOL, exists_ip)
    if free_id is None or free_ip is None:
        raise SystemExit("---ERROR--- pool заполнен ---ПРОЦЕСС ПРЕКРАЩЕН---")
    tfvars["instances"][free_name] = {
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
    json.dump(tfvars, f, indent=2)

print('tfvars сгенерирован')
with open("terraform/terraform.tfvars.json", "r", encoding="utf-8") as f:
    print(json.load(f))
