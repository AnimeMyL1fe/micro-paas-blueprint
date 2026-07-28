# ---------------------------------------
# Default Configuration
# ---------------------------------------
# SSH
variable "vm_user" {
  type    = string
  default = "ansible"
}
variable "path_ssh" {
  type    = string
  default = "~/.ssh/proxmox_key.pub"
}
variable "private_ssh" {
  type    = string
  default = "~/.ssh/proxmox_key"
}
# PROXMOX
variable "node_name" {
  type    = string
  default = "proxmox2"
}
variable "clone_id" {
  type    = number
  default = 9000
}

# ---------------------------------------
# Firewall Configuration
# ---------------------------------------
variable "source_ip" {
  type    = string
  default = "192.168.0.0/24"
}

# ---------------------------------------
# Virtual Machines
# ---------------------------------------
variable "vm_vnet" {
  type    = string
  default = "vn1"
}

variable "instances" {
  type = map(object({
    name    = string
    cpu     = number
    ram_mb  = number
    disk_gb = number
    vm_id   = number
    vm_ipv4 = string
    gateway = string

    inbound_rules = list(object({
      port     = number
      protocol = string
    }))

  }))
}
