#!/bin/bash
echo " =============================== "
echo "TERRAFORM ---> ANSIBLE DEPLOY"
echo " =============================== "
echo ""
#echo "INSTANCES VARIABLES"

read -p "vm_count: " VM_COUNT
read -p "template_name: " TEMPLATE_NAME
read -p "preset_config: " PRESET_NAME

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
python3 main.py \
    --vm-count "$VM_COUNT" \
    --template "$TEMPLATE_NAME" \
    --preset "$PRESET_NAME" 

sleep 3
# terraform check
terraform -chdir=terraform init
#terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve -parallelism=2

echo "ожидание ssh ... (20s)"
sleep 20
# ansible
echo "ANSIBLE DEPLOY ..."
cd ansible && ansible-playbook test_deploy.yml --vault-pass-file=.vault_pass
