import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Terraform tfvars generator for micro-paas"
)

parser.add_argument("--name", required=True)
parser.add_argument("--cpu", type=int, required=True)
parser.add_argument("--ram", type=int, required=True)
parser.add_argument("--disk", type=int, required=True)
parser.add_argument("--vm-id", type=int, required=True)

args = parser.parse_args()

config = {
    "instances": {
        args.name: {
            "name": args.name,
            "cpu": args.cpu,
            "ram_mb": args.ram,
            "disk_gb": args.disk,
            "vm_id": args.vm_id,
        }
    }
}

output_path = Path("terraform") / "terraform.tfvars.json"

with output_path.open("w", encoding="utf-8") as file:
    json.dump(config, file, indent=4)

print(f"Terraform variables written to: {output_path}")