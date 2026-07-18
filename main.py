import yaml
import json
from pathlib import Path


file_path = Path("terraform/terraform.tfvars.json")
# ip_pool
IP_POOL = []
for host in range(10, 21):
    IP_POOL.append(f"10.100.100.{host}")

GATEWAY = "10.100.100.1"

# read files
with open("blueprints/postgresql/blueprint.yml") as f:
    data = yaml.safe_load(f)
 
#check file
if file_path.exists():
    print('Файл уже существует')
else:
    print('Файла нет')

# check ip
exists_ip = []
if file_path.exists():
    with open("terraform/terraform.tfvars.json", "r", encoding="utf-8") as f:
        f_tfvars = json.load(f)
        for vm in f_tfvars['instances'].values():
            exists_ip.append(vm["vm_ipv4"])

# get free ip
new_name = data["name"]
if file_path.exists():
    if new_name in f_tfvars["instances"]:
        print('Имя сервиса занято')
    else:
        for ip in IP_POOL:
            if ip not in exists_ip:
                free_ip = ip
                break
else:
    for ip in IP_POOL:
        if ip not in exists_ip:
            free_ip = ip
            break


# готовим data 
full_list = {
    "instances": {
        data['name']: {
            "name": data['name'],
            "cpu": data['infrastructure']['cpu'],
            "ram_mb": data['infrastructure']['ram_mb'],
            "disk_gb": data['infrastructure']['disk_gb'],
            "vm_id": 2000,
            "vm_ipv4": free_ip,
            "gateway": GATEWAY
        }
    },
    "inbound_rules": data["network"]["inbound_ports"]
}
#check data

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