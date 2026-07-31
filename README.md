# micro-paas-blueprint

[![CI Checks](https://github.com/AnimeMyL1fe/micro-paas-blueprint/actions/workflows/ci_check.yml/badge.svg?branch=main)](https://github.com/AnimeMyL1fe/micro-paas-blueprint/actions/workflows/ci_check.yml)

Автоматизированное развёртывание сервисов в **Proxmox VE** на основе Blueprint с использованием **Python**, **Terraform**, **Ansible** и **GitHub Actions**.

Проект представляет собой прототип micro-PaaS: пользователь выбирает сервис, профиль ресурсов и количество экземпляров, после чего система генерирует конфигурацию и выполняет полный цикл развёртывания.

---

## Архитектура

```text
Blueprint + Profile
        │
        ▼
Python Generator
        │
        ▼
terraform.tfvars.json
        │
        ▼
Terraform ───────────────► MinIO S3 Backend
        │                      │
        ▼                      ▼
Proxmox VE              Remote Terraform State
        │
        ▼
Virtual Machines
        │
        ▼
Generated Inventory
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

### Bootstrap-инфраструктура

Каталог `infra/` содержит отдельный слой инфраструктуры, используемый самой платформой:

- Terraform создаёт VM и сетевые правила для MinIO;
- Ansible устанавливает Docker и разворачивает MinIO;
- MinIO используется как S3 remote backend для хранения Terraform State.

Bootstrap-инфраструктура имеет независимый Terraform State и не уничтожается вместе с пользовательскими сервисами.

---

## Используемые технологии

- Python
- Terraform
- Proxmox VE
- Ansible
- Docker
- Docker Compose
- MinIO
- GitHub Actions
- S3 remote backend

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
- ✅ Хранить Terraform State в MinIO
- ✅ Использовать отдельную bootstrap-инфраструктуру
- ✅ Выполнять CI-проверки через GitHub Actions
- ✅ Запускать Deploy Pipeline вручную
- ✅ Удалять инфраструктуру через подтверждаемый Destroy Pipeline
- ✅ Хранить секреты Ansible в Ansible Vault
- ✅ Выбирать Blueprint и профиль через GitHub Actions
- ✅ Выполнять полный цикл Deploy через GitHub Actions
- ✅ Разворачивать чистый Docker-хост

---

### Реализованные Blueprint

- Docker:
    - виртуальная машина с установленными Docker Engine и Docker Compose;
    - профили ресурсов `small` и `medium`.

- PostgreSQL:
    - PostgreSQL;
    - Adminer;
    - postgres_exporter;
    - профили ресурсов `small` и `medium`.

---

## Структура проекта

```text
.
├── .github
│   └── workflows
│       ├── ci_check.yml
│       ├── deploy.yml
│       └── destroy.yml
├── ansible
│   ├── deploy.yml
│   ├── group_vars
│   ├── host_vars
│   ├── inventory
│   └── roles
│       ├── bootstrap
│       ├── docker-install
│       └── postgresql
├── blueprints
│   ├── docker
│   │   ├── blueprint.yml
│   │   └── profiles
│   │       ├── medium.yml
│   │       └── small.yml
│   └── postgresql
│       ├── blueprint.yml
│       └── profiles
│           ├── medium.yml
│           └── small.yml
├── infra
│   ├── ansible
│   │   ├── bootstrap_infra.yml
│   │   └── roles
│   │       ├── docker-install
│   │       └── minio
│   └── terraform
├── terraform
├── main.py
├── pipeline.sh
├── requirements-dev.txt
├── requirements.txt
└── README.md
```

---

## CI/CD

В проекте настроены GitHub Actions workflows:

- `ci_check.yml` — Pylint для Python 3.13 и 3.14, проверка форматирования и валидация Terraform, синтаксическая проверка Ansible Playbook;
- `deploy.yml` — ручной запуск развёртывания;
- `destroy.yml` — ручное удаление инфраструктуры с подтверждением `DESTROY`.

Workflows выполняются на self-hosted runner. Terraform State хранится в приватном MinIO-бакете через S3 remote backend.

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

- [x] Поддержка нескольких Blueprint
- [x] Docker Blueprint
- [x] PostgreSQL Blueprint
- [x] Отдельная bootstrap-инфраструктура
- [x] MinIO S3 backend для Terraform State
- [x] Deploy и Destroy pipelines
- [x] CI/CD
- [ ] Redis Blueprint
- [ ] Nginx Blueprint
- [ ] WordPress Blueprint
- [ ] MongoDB Blueprint
- [ ] MinIO Blueprint
- [ ] Мониторинг инфраструктуры: Prometheus и Grafana
- [ ] Централизованный сбор логов
- [ ] FastAPI API
- [ ] Web UI
- [ ] Kubernetes

---

## Статус проекта

🚧 Проект находится в активной разработке.

Реализован рабочий MVP, выполняющий полный цикл развёртывания сервисов:

`Blueprint → Python Generator → Terraform → Proxmox VE → Ansible → Docker Compose`.

Поддерживаются Docker и PostgreSQL Blueprint, профили ресурсов, CI-проверки, ручные Deploy/Destroy pipelines и хранение Terraform State в MinIO.