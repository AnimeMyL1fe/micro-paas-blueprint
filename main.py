import yaml
import json
from pathlib import Path
import argparse

# --- global parametrs ---
GATEWAY = "10.100.100.1"
vm_limit_count = 20
exists_names = []
exists_ip = []
exists_ids = []

# --- input ---
parser = argparse.ArgumentParser(description="CLI input")
parser.add_argument("--vm-count", type=int, default=1, help="Количество vm по умолчанию: 1)")
parser.add_argument("--template", type=str, help="Выбор шаблона")
parser.add_argument("--preset", type=str, default='small', help="Параметры vm")
args = parser.parse_args()




# --- pools ---
IP_POOL = []
for host in range(10, 30):
    IP_POOL.append(f"10.100.100.{host}")

ID_POOL = []
id_start, id_max = 2000, 2020
for vm_id in range (id_start, id_max):
    ID_POOL.append(vm_id)

# --- read file ---
file_path = Path("terraform/terraform.tfvars.json")

with open(f"blueprints/{args.template}/blueprint.yml") as f:
    inbound_data = yaml.safe_load(f)

with open(f"blueprints/{args.template}/profiles/{args.preset}.yml") as f:
    vm_data = yaml.safe_load(f)

if file_path.exists():
    with open("terraform/terraform.tfvars.json", "r", encoding="utf-8") as f:
        tfvars = json.load(f) 
else:
    tfvars = {
    "instances": {},
    }

# --- functions ---
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


# --- generation tfvars ---
for _ in range(args.vm_count):
    base_name = args.template
    for vm_count in range(1, vm_limit_count + 1):
        candidate_name = f"{base_name}--{vm_count}"
        if candidate_name not in exists_names:
            free_name = candidate_name
            exists_names.append(free_name)
            break
    free_id = get_pool(ID_POOL, exists_ids)
    free_ip = get_pool(IP_POOL, exists_ip)
    if free_id is None or free_ip is None:
        raise SystemExit("---ERROR--- pool (id, ip) заполнен ---ПРОЦЕСС ПРЕКРАЩЕН---")

    tfvars["instances"][free_name] = {
            "name": free_name,
            "cpu": vm_data['infrastructure']['cpu'],
            "ram_mb": vm_data['infrastructure']['ram_mb'],
            "disk_gb": vm_data['infrastructure']['disk_gb'],
            "vm_id": free_id,
            "vm_ipv4": free_ip,
            "gateway": GATEWAY,
            "inbound_rules": inbound_data["network"]["inbound_ports"]
        }

    ansible_hostvars = {
        "shared_roles": inbound_data['ansible']['shared_roles'],
        "service_roles": inbound_data['ansible']['service_roles'],
        args.template: vm_data[args.template],
        "features": vm_data['features']
    }

    with open(f"ansible/host_vars/{free_name}.yml", "w", encoding="utf-8") as f:
        yaml.safe_dump(
            ansible_hostvars,
            f,
            sort_keys=False,
            allow_unicode=True
        )
    
# --- output ---
with open("terraform/terraform.tfvars.json", "w", encoding="utf-8") as f:
    json.dump(tfvars, f, indent=2)



print('-' * 16)
print('tfvars создан')
print('-' * 16)

with open("terraform/terraform.tfvars.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print_json = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
print(print_json)