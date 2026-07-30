all:
  children:
    # --- LINUX SERVERS ---
    linux_servers: 
      hosts:
%{for name, vm in vms ~}
        ${name}:
          ansible_host: ${vm.ip}
%{ endfor ~}
  vars:
    ansible_user: ${ans_user}
    ansible_ssh_private_key_file: ${ans_ssh_key}
    ansible_become: true