import argparse
import json
from pathlib import Path


IP_POOL = [
    f"10.100.100.{host}"
    for host in range(10, 20)
]

#CIDR_SUFFIX = "/24"
GATEWAY = "10.100.100.1"


def get_free_ip(instances: dict) -> str:
    used_ips = {
        vm["vm_ipv4"].split("/")[0]
        for vm in instances.values()
        if "vm_ipv4" in vm
    }

    for ip in IP_POOL:
        if ip not in used_ips:
            return f"{ip}" #CIDR_SUFFIX

    raise RuntimeError("Свободных IP-адресов в пуле больше нет")


parser = argparse.ArgumentParser(
    description="Terraform tfvars generator for micro-paas"
)

parser.add_argument("--name", required=True)
parser.add_argument("--cpu", type=int, required=True)
parser.add_argument("--ram", type=int, required=True)
parser.add_argument("--disk", type=int, required=True)
parser.add_argument("--vm-id", type=int, required=True)

args = parser.parse_args()

output_path = Path("terraform") / "terraform.tfvars.json"
output_path.parent.mkdir(parents=True, exist_ok=True)

if output_path.exists():
    with output_path.open("r", encoding="utf-8") as file:
        config = json.load(file)
else:
    config = {"instances": {}}

instances = config.setdefault("instances", {})

if args.name in instances:
    raise RuntimeError(f"Инстанс '{args.name}' уже существует")

if any(vm.get("vm_id") == args.vm_id for vm in instances.values()):
    raise RuntimeError(f"VM ID '{args.vm_id}' уже используется")

free_ip = get_free_ip(instances)

instances[args.name] = {
    "name": args.name,
    "cpu": args.cpu,
    "ram_mb": args.ram,
    "disk_gb": args.disk,
    "vm_id": args.vm_id,
    "vm_ipv4": free_ip,
    "gateway": GATEWAY,
}

with output_path.open("w", encoding="utf-8") as file:
    json.dump(config, file, indent=4)

print(f"Terraform variables written to: {output_path}")
print(f"Assigned IPv4: {free_ip}")
print(f"Gateway: {GATEWAY}")