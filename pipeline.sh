#!/bin/bash
echo " =============================== "
echo "ВНИМАНИЕ! НЕ ЗАБУДЬТЕ ЭКСПОРТИРОВАТЬ CREDENTIALS ДЛЯ PROXMOX PROVIDER"
echo " =============================== "
echo ""
echo "INSTANCES VARIABLES"
read -p "name: " NAME
read -p "cpu: " CPU
read -p "ram(MB): " RAM
read -p "disk(GB): " DISK
read -p "id: " ID

# python dynamice .tfvars script
# --name NAME --cpu CPU --ram RAM --disk DISK --id ID
echo "PYTHON SCRIPT ..."
python3 main.py \
  --name "$NAME" \
  --cpu "$CPU" \
  --ram "$RAM" \
  --disk "$DISK" \
  --id "$ID"

sleep 3
# terraform check
terraform -chdir=terraform plan
