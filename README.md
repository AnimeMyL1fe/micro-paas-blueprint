# micro-paas-blueprint

Автоматизированное создание виртуальных машин и развёртывание сервисов в Proxmox VE с использованием Terraform, Cloud-Init и Ansible.


## Цель проекта

Создать инструмент, который по одной команде сможет автоматически:

```text
CLI
    ↓
Python
    ↓
Terraform
    ↓
Создание виртуальных машин
    ↓
Генерация Ansible Inventory
    ↓
Ansible
    ↓
Развёртывание сервисов
```

## Используемые технологии

- Python
- Terraform
- Proxmox VE
- Cloud-Init
- Ansible

## Что уже реализовано
- ✅ Базовая Terraform-конфигурация
- ✅ Создание виртуальных машин из Cloud-Init Template (Proxmox VE)
- ✅ Генерация `terraform.tfvars.json` через Python CLI
- ✅ Автоматическое назначение статических IP из пула
- ✅ Настройка Proxmox SDN: Zone, VNet, Subnet и SNAT
- ✅ Создание и применение базовой Security Group
- ✅ Автоматическая генерация Ansible Inventory
- ✅ Автоматический запуск Terraform
- ✅ Ожидание готовности SSH после создания VM
- ✅ Автоматический запуск Ansible Playbook
- ✅ Установка Docker через Ansible

## Структура проекта

```text
.
├── README.md
├── ansible
│   ├── ansible.cfg
│   ├── inventory
│   │   └── hosts.yaml
│   ├── roles
│   │   └── docker-install
│   └── test_deploy.yml
├── main.py
├── pipeline.sh
├── terraform
    ├── main.tf
    ├── output.tf
    ├── provider.tf
    ├── security_group.tf
    ├── subnet.tf
    ├── templates
    │   └── inventory.tpl
    └── variables.tf
```

## Использование

Перед запуском необходимо экспортировать переменные окружения для Terraform Provider (Proxmox).

Запуск локального pipeline:

```bash
chmod +x pipeline.sh
./pipeline.sh
```

Во время запуска скрипт запросит параметры виртуальной машины:

```text
INSTANCES VARIABLES

name: postgresql
cpu: 2
ram(MB): 2048
disk(GB): 32
id: 5000
```

После этого pipeline автоматически:

```text
pipeline.sh
        ↓
Python CLI
        ↓
terraform.tfvars.json
        ↓
terraform init
        ↓
terraform plan
        ↓
terraform apply
        ↓
Создание VM в Proxmox VE
        ↓
Генерация Ansible Inventory
        ↓
Ожидание доступности SSH
        ↓
Ansible Playbook
        ↓
Установка Docker
```

## Текущий pipeline

На текущем этапе проект способен автоматически:

- создать виртуальную машину в Proxmox VE;
- настроить сеть (SDN);
- применить базовую Security Group;
- сгенерировать Ansible Inventory;
- дождаться доступности SSH;
- выполнить Ansible Playbook;
- установить Docker.

## Прямой запуск Python

Также генератор можно использовать напрямую:

```bash
python3 main.py \
    --name "$NAME"\
    --cpu "$CPU" \
    --ram "$RAM" \
    --disk "$DISK" \
    --vm-id "$ID" 
```

После выполнения будет создан файл:

```text
terraform/terraform.tfvars.json
```

который используется Terraform.


## Планируемые возможности

Проект находится на стадии исследования архитектуры, поэтому список ниже не является строгим roadmap и может изменяться.

Возможные направления развития:

- [ ] Metadata сервисов
- [ ] Поддержка нескольких сервисов
- [ ] Поддержка нескольких виртуальных машин
- [ ] PostgreSQL Blueprint
- [ ] Redis Blueprint
- [ ] Prometheus Blueprint
- [ ] CI/CD

## Статус проекта

🚧 **MVP в активной разработке.**

Проект создаётся как pet-проект для исследования подходов к автоматизации развёртывания инфраструктуры.

Архитектура и функциональность могут существенно изменяться по мере развития проекта.