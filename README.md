# micro-paas-blueprint

Инструмент для автоматической генерации и развёртывания инфраструктуры на базе **Terraform** и **Ansible**.

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

## Что уже реализовано
- ✅ Базовая Terraform-конфигурация
- ✅ Создание виртуальных машин из Cloud-Init Template (Proxmox VE)
- ✅ Генерация terraform.tfvars.json через Python CLI
- ✅ Автоматическое назначение статических IP из пула
- ✅ Настройка Proxmox SDN (VNet + Subnet)

## Структура проекта

```text
.
├── README.md
├── main.py
├── pipeline.sh
└── terraform
    ├── main.tf
    ├── output.tf
    ├── provider.tf
    ├── subnet.tf
    ├── variables.tf
    └── templates
        └── inventory.tpl
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
main.py
        ↓
terraform.tfvars.json
        ↓
terraform plan
```

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

## Pipeline

```
Python CLI
      │
      ▼
Terraform
      │
      ▼
Proxmox VE
      │
      ▼
Virtual Machine

      --- Планируется --- 

      ▼
Ansible Inventory
      │
      ▼
Ansible Playbook
```

## Планируемые возможности

Проект находится на стадии исследования архитектуры, поэтому список ниже не является строгим roadmap и может изменяться.

Возможные направления развития:

- [ ] Автоматический запуск Terraform
- [ ] Автоматический запуск Ansible
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