
import subprocess


def main():
    subprocess.call(["D:\\Apps\\VB\\VBoxManage.exe", "guestcontrol", "vm2", "copyto", "--target-directory", "/home/mohsen",
                     "--username", "mohssen", "--password", "Emma1998",
                     "D:\\Uni\\term4\\Cloud computing\\Asignment\\copy_command.txt"])


if __name__ == '__main__':
    main()