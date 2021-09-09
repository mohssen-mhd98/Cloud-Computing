import virtualbox
import subprocess
import re
import sys


def get_state(vm_name):
    vm_info = subprocess.check_output(["D:\\Apps\\VB\\VBoxManage.exe",
                                       "showvminfo", vm_name, "--machinereadable"]).decode(sys.stdout.encoding)
    state_pattern = r"VMState=\"\w+\""
    machine_state = re.search(state_pattern, vm_info)
    machine_state = machine_state.group(0).split('=')
    machine = machine_state[1].split("\"")

    return machine[1]


def get_states():
    vbox = virtualbox.VirtualBox()
    vm_list = [m.name for m in vbox.machines]
    details = []
    for vm in vm_list:
        tmp_dic = {}
        vm_info = subprocess.check_output(["D:\\Apps\\VB\\VBoxManage.exe",
                                           "showvminfo", vm, "--machinereadable"]).decode(sys.stdout.encoding)
        state_pattern = r"VMState=\"\w+\""
        name_pattern = r"name=\"\w+\""
        machine_state = re.search(state_pattern, vm_info)
        machine_state = machine_state.group(0).split('=')
        machine_state = machine_state[1].split("\"")
        machine_state = machine_state[1]

        machine_name = re.search(name_pattern, vm_info)
        machine_name = machine_name.group(0).split('=')
        machine_name = machine_name[1].split("\"")
        machine_name = machine_name[1]

        tmp_dic.update({'vmName': machine_name, 'status': machine_state})
        details.append(tmp_dic)

    return details


def execute_command(vm, command):
    ip = subprocess.check_output(["D:\\Apps\\VB\\VBoxManage.exe",
                                  "guestproperty", "get", vm, "/VirtualBox/GuestInfo/Net/0/V4/IP"])
    ip = ip.decode('utf-8')
    ip = str(ip).replace('Value: ', '')
    ip = str(ip).rstrip()
    result = subprocess.check_output(["ssh", "mohssen@" + ip, command])
    result = result.decode('utf-8')
    # subprocess.call(["C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PuTTY (64-bit)\\puTTy",
    #                  "pscp", machine, "poweroff", "soft"])
    return result


def start_machine(vm_name):
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "startvm", vm_name])


def shutdown_machine(vm_name):
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "controlvm", vm_name, "poweroff", "soft"])


def clone_machine(source_machine, cloned_machine):
    subprocess.call(
        ["D:\\Apps\\VB\\VBoxManage.exe", "clonevm", source_machine, "--name=" + cloned_machine, "--register",
         "--mode=all", "--options=keepallmacs", "--options=keepdisknames", "--options=keephwuuids"])


def delete_machine(vm_name):
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "unregistervm", vm_name, "--delete"])


def modify_cores(vm_name, core_number):
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "modifyvm", vm_name, "--cpus", core_number])


def modify_memory(vm_name, memory_volume):
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "modifyvm", vm_name, "--memory", memory_volume])


def upload_file(vm_name, dst_directory, src_path):
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "guestcontrol", vm_name, "copyto", "--target-directory", dst_directory,
                     "--username", "mohssen", "--password", "Emma1998", src_path])


def transfer_file(origin_vm, dst_vm, src_path, middle_path, dst_path):
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe","guestcontrol", origin_vm, "copyfrom", "--target-directory", middle_path,
                     "--username", "mohssen", "--password", "Emma1998", src_path])

    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "guestcontrol", dst_vm, "copyto", "--target-directory", dst_path,
                     "--username", "mohssen", "--password", "Emma1998", middle_path])
