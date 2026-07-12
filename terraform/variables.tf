# --- DEFAULTS VARIABLES ---
# ssh-user
variable "vm_user" {
  type = string
  default = "ansible"
}
# ssh pubkey
variable "path_ssh" {
  type = string
  default = "~/.ssh/proxmox_key.pub"
}
variable "private_ssh" {
  type = string
  default = "~/.ssh/proxmox_key"
}
variable "node_name" {
  type = string
  default = "proxmox2"
}
variable "clone_id" {
  type = number
  default = 9000
}

# --- VM VARIABLES ---
variable "vm_list" {
    type = map(object({
        name        = string
        cpu         = number
        ram         = number
        disk_size   = number
        id          = number
    }))
}