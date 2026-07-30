# ---------------------------------------
# SUBNET
# ---------------------------------------
resource "proxmox_sdn_zone_simple" "zone_2" {
  id    = "zn2"
  nodes = ["proxmox2"]
  mtu   = 1500
}


# SDN VNet
resource "proxmox_sdn_vnet" "vnet_2" {
  id   = "vn2"
  zone = proxmox_sdn_zone_simple.zone_2.id
}


# Subnet
resource "proxmox_sdn_subnet" "subnet_2" {
  cidr    = "10.100.110.0/24"
  vnet    = proxmox_sdn_vnet.vnet_2.id
  gateway = "10.100.110.1"
  snat    = true
}

# SDN Applier for all resources
resource "proxmox_sdn_applier" "subnet_applier" {
  depends_on = [
    proxmox_sdn_zone_simple.zone_2,
    proxmox_sdn_vnet.vnet_2,
    proxmox_sdn_subnet.subnet_2,
  ]
}