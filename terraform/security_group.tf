resource "proxmox_virtual_environment_cluster_firewall_security_group" "default_vm" {
  for_each = var.instances
  name     = "fw-${each.key}"
  dynamic "rule" {
    for_each = each.value.inbound_rules

    content {
      type   = "in"
      action = "ACCEPT"
      proto  = rule.value.protocol
      dport  = rule.value.port
    }
  }
  rule {
    type   = "in"
    action = "ACCEPT"
    proto  = "icmp"
  }
}

resource "proxmox_virtual_environment_firewall_rules" "vm_rules" {
  for_each = proxmox_virtual_environment_vm.instance

  node_name = each.value.node_name
  vm_id     = each.value.vm_id

  rule {
    security_group = proxmox_virtual_environment_cluster_firewall_security_group.default_vm[each.key].name
    iface          = "net0"
    comment        = "Apply micro-paas security group"
  }
}

resource "proxmox_virtual_environment_firewall_options" "vm_options" {
  for_each = proxmox_virtual_environment_vm.instance

  node_name = each.value.node_name
  vm_id     = each.value.vm_id

  enabled       = true
  input_policy  = "ACCEPT"
  output_policy = "ACCEPT"
}