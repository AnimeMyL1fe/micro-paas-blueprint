#!/bin/bash
echo " =============================== "
echo "ВНИМАНИЕ! НЕ ЗАБУДЬТЕ ЭКСПОРТИРОВАТЬ CREDENTIALS ДЛЯ PROXMOX PROVIDER"
echo " =============================== "
echo ""
#echo "INSTANCES VARIABLES"

#read -p "name: " NAME
#read -p "cpu: " CPU
#read -p "ram(MB): " RAM
#read -p "disk(GB): " DISK
#read -p "id: " ID

# python dynamice .tfvars script
# --name NAME --cpu CPU --ram RAM --disk DISK --id ID
#echo "PYTHON SCRIPT ..."
#python3 main.py \
#    --name "$NAME"\
#    --cpu "$CPU" \
#    --ram "$RAM" \
#    --disk "$DISK" \
#    --vm-id "$ID"
python3 main.py

sleep 3
# terraform check
terraform -chdir=terraform init
terraform -chdir=terraform apply -auto-approve

echo "ожидание ssh ... (15s)"
sleep 15
# ansible
echo "ANSIBLE DEPLOY ..."
cd ansible && ansible-playbook test_deploy.yml
