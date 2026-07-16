# ---------------------------------------
# SUBNET
# ---------------------------------------
resource "proxmox_virtual_environment_sdn_zone_simple" "zone_1" {
  id    = "zn1"
  nodes = ["proxmox2"]
  mtu   = 1500
}


# SDN VNet
resource "proxmox_virtual_environment_sdn_vnet" "vnet_1" {
  id   = "vn1"
  zone = proxmox_virtual_environment_sdn_zone_simple.zone_1.id
}


# Subnet
resource "proxmox_virtual_environment_sdn_subnet" "subnet_1" {
  cidr    = "10.100.100.0/24"
  vnet    = proxmox_virtual_environment_sdn_vnet.vnet_1.id
  gateway = "10.100.100.1"
  snat    = true
}

# SDN Applier for all resources
resource "proxmox_virtual_environment_sdn_applier" "subnet_applier" {
  depends_on = [
    proxmox_virtual_environment_sdn_zone_simple.zone_1,
    proxmox_virtual_environment_sdn_vnet.vnet_1,
    proxmox_virtual_environment_sdn_subnet.subnet_1,
  ]
}