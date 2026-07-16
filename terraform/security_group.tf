resource "proxmox_virtual_environment_cluster_firewall_security_group" "default_vm" {
  name = "default-vm"

  rule {
    type    = "in"
    action  = "ACCEPT"
    proto   = "tcp"
    dport   = "22"
    source  = var.source_ip
    comment = "SSH from LAN"
  }

  rule {
    type    = "in"
    action  = "ACCEPT"
    proto   = "tcp"
    dport   = "80"
    source  = var.source_ip
    comment = "HTTP from LAN"
  }

  rule {
    type    = "in"
    action  = "ACCEPT"
    proto   = "tcp"
    dport   = "443"
    source  = var.source_ip
    comment = "HTTPS from LAN"
  }

  rule {
    type    = "in"
    action  = "ACCEPT"
    proto   = "icmp"
    source  = var.source_ip
    comment = "Ping from LAN"
  }
}

resource "proxmox_virtual_environment_firewall_rules" "vm_rules" {
  for_each = proxmox_virtual_environment_vm.instance

  node_name = each.value.node_name
  vm_id     = each.value.vm_id

  rule {
    security_group = proxmox_virtual_environment_cluster_firewall_security_group.default_vm.name
    iface          = "net0"
    comment        = "Apply micro-paas security group"
  }
}

resource "proxmox_virtual_environment_firewall_options" "vm_options" {
  for_each = proxmox_virtual_environment_vm.instance

  node_name = each.value.node_name
  vm_id     = each.value.vm_id

  enabled       = true
  input_policy  = "DROP"
  output_policy = "ACCEPT"
}