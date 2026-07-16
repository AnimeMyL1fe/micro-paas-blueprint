# ---------------------------------------
# CREATE INSTANCE
# ---------------------------------------
resource "proxmox_virtual_environment_vm" "instance" {
  for_each    = var.instances
  name        = each.value.name
  node_name   = var.node_name
  description = "Managed by micro-paas-blueprint"
  vm_id       = each.value.vm_id

  clone {
    vm_id = var.clone_id 
  }

  cpu {
    cores = each.value.cpu
  }

  memory {
    dedicated = each.value.ram_mb
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = each.value.disk_gb
  }

  network_device {
    bridge = var.vm_vnet
    model    = "virtio"
    firewall = true
  }


  initialization {
    ip_config {
      ipv4 {
        address = "${each.value.vm_ipv4}/24"
        gateway = each.value.gateway
      }
    }
    user_account {
      username = var.vm_user
      keys     = [file(pathexpand(var.path_ssh))]
    }
  }
}

# ---------------------------------------
# DYNAMIC INVENTORY
# ---------------------------------------
locals {
  vm_info = {
    for name, vm in proxmox_virtual_environment_vm.instance : name =>{
      ip = split("/", vm.initialization[0].ip_config[0].ipv4[0].address)[0]
    }
  }

}

resource "local_file" "ansible_inventory" {
  content = templatefile("${path.module}/templates/inventory.tpl", {
    vms           = local.vm_info
    ans_ssh_key   = var.private_ssh
    ans_user      = var.vm_user
  })
  filename = "${path.module}/../ansible/inventory/hosts.yaml"
}
