import argparse
import json
from pathlib import Path


parser = argparse.ArgumentParser()

parser.add_argument("--name", required=True)
parser.add_argument("--cpu", type=int, required=True)
parser.add_argument("--ram", type=int, required=True)
parser.add_argument("--disk", type=int, required=True)
parser.add_argument("--id", type=int, required=True)

args = parser.parse_args()


config = {
    "vm_list": {
        args.name: {
            "name": args.name,
            "cpu": args.cpu,
            "ram": args.ram,
            "disk_size": args.disk,
            "id": args.id,
        }
    }
}


output_path = Path("terraform/terraform.tfvars.json")

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(config, file, indent=2)


print(f"Файл создан: {output_path}")
