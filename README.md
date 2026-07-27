# micro-paas-blueprint

Автоматизированное развертывание сервисов в **Proxmox VE** с использованием **Blueprint**, **Terraform** и **Ansible**.

Проект исследует подход к построению собственного **micro-PaaS**, где инфраструктура и сервис разворачиваются одной командой.

---

## Архитектура

```text
CLI
 │
 ▼
Python Generator
 │
 ▼
Blueprint
 │
 ▼
terraform.tfvars.json
 │
 ▼
Terraform
 │
 ▼
Proxmox VE
 │
 ▼
Cloud-Init
 │
 ▼
Ansible Inventory
 │
 ▼
Ansible
 │
 ▼
Docker Compose
 │
 ▼
Service
```

---

## Используемые технологии

- Python
- Terraform
- Proxmox VE
- Ansible
- Docker
- Docker Compose

---

## Возможности

На текущем этапе проект умеет автоматически:

- ✅ Генерировать `terraform.tfvars.json`
- ✅ Работать через Blueprint
- ✅ Разворачивать несколько виртуальных машин
- ✅ Автоматически выделять свободные IP-адреса
- ✅ Автоматически выделять VM ID
- ✅ Настраивать Proxmox SDN
- ✅ Создавать Security Group и Firewall Rules
- ✅ Генерировать Ansible Inventory
- ✅ Ожидать готовность SSH
- ✅ Устанавливать Docker
- ✅ Разворачивать сервисы через Ansible

### Реализованные Blueprint

- PostgreSQL:
    - PostgreSQL
    - Adminer
    - postgres_exporter

---

## Структура проекта

```text
.
├── ansible
│   ├── host_vars
│   ├── inventory
│   ├── roles
│   │   ├── docker-install
│   │   └── postgresql
│   └── deploy.yml
│
├── blueprints
│   └── postgresql
│       ├── blueprint.yml
│       └── profiles
│
├── terraform
│   ├── templates
│   ├── main.tf
│   ├── subnet.tf
│   ├── security_group.tf
│   ├── variables.tf
│   └── output.tf
│
├── main.py
├── pipeline.sh
└── README.md
```

---

## Использование

Перед запуском необходимо экспортировать переменные окружения Terraform Provider для Proxmox.

Запуск pipeline:

```bash
chmod +x pipeline.sh
./pipeline.sh
```

После запуска необходимо выбрать Blueprint и профиль.

Например:

```text
vm_count: 5
template: postgresql
profile: small
```

После этого автоматически выполняется полный цикл развертывания.

```text
pipeline.sh
        │
        ▼
Python Generator
        │
        ▼
terraform.tfvars.json
        │
        ▼
terraform init
        │
        ▼
terraform apply
        │
        ▼
Создание виртуальных машин
        │
        ▼
Генерация Ansible Inventory
        │
        ▼
Ожидание SSH
        │
        ▼
Ansible
        │
        ▼
Docker Compose
        │
        ▼
Развертывание сервиса
```

---

## Blueprint

Каждый сервис описывается собственным Blueprint.

Blueprint определяет:

- параметры виртуальной машины;
- профиль ресурсов;
- сетевые настройки (открываемые порты);
- роли Ansible;
- параметры сервиса.

Это позволяет добавлять новые сервисы практически без изменения основной логики генератора.

---

## Планы развития

Возможные направления развития проекта:

- [ ] Поддержка нескольких Blueprint
- [ ] Redis Blueprint
- [ ] MinIO Blueprint
- [ ] Prometheus Blueprint
- [ ] Grafana Blueprint
- [ ] Destroy Pipeline
- [ ] FastAPI API
- [ ] Web UI
- [ ] CI/CD

---

## Статус проекта

🚧 Проект находится в активной разработке.

На текущем этапе реализован **MVP**, позволяющий автоматически развернуть готовый сервис в Proxmox VE с использованием Terraform и Ansible.

Архитектура продолжает развиваться и может изменяться по мере появления новых возможностей.