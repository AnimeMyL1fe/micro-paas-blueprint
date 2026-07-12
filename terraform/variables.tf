# ---------------------------------------
# Default Configuration
# ---------------------------------------
# SSH
variable "vm_user" {
  type = string
  default = "ansible"
}
variable "path_ssh" {
  type = string
  default = "~/.ssh/proxmox_key.pub"
}
variable "private_ssh" {
  type = string
  default = "~/.ssh/proxmox_key"
}
# PROXMOX
variable "node_name" {
  type = string
  default = "proxmox2"
}
variable "clone_id" {
  type = number
  default = 9000
}

# ---------------------------------------
# Virtual Machines
# ---------------------------------------
variable "instances" {
  type = map(object({
    name     = string
    cpu      = number
    ram_mb   = number
    disk_gb  = number
    vm_id    = number
  }))
}