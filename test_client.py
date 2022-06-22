import paramiko
import re

import pytest

output_file = "paramiko.log"


@pytest.fixture
def connection():
    port = 22
    global client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="192.168.170.104", port=22, username="node1", password="Rk@8531")
    yield
    client.close()


def test_DiskSpace(connection):
    print("paramiko opration for DiskSpace")
    try:

        (stdin, stdout, stderr) = client.exec_command("df --output=pcent /dev/sda3")
        (stdin1, stdout1, stderr1) = client.exec_command("date")
        cmd_output = stdout.read()
        TimeStamp = stdout1.read()
        list1 = [r"\n", "'", "b"]
        for i in list1:
            cmd_output = str(cmd_output).replace(i, "")
            TimeStamp = str(TimeStamp).replace(i, "")
        x = re.findall("\d{2}", cmd_output)
        value = int(x[0])
        assert value < 90
        with open(output_file, "a+") as file:
            file.write("\n" + str(TimeStamp) + "\t" + "Disk::" + str(cmd_output))
        return output_file
    finally:
        print("1st")


def test_CPU(connection):
    print("paramiko opration fro Cpu")
    try:
        (stdin, stdout, stderr) = client.exec_command("mpstat | grep -A 5 %idle | tail -n 1 | awk '{print $14}'")
        cmd_output1 = stdout.read()
        print(str(cmd_output1))
        list1 = [r"\n", "'", "b"]
        for i in list1:
            cmd_output1 = str(cmd_output1).replace(i, "")
        x = re.findall("\d{2}.{3}", cmd_output1)
        value = float(x[0])
        assert value < 99
        with open(output_file, "a+") as file:
            file.write("\t" + "CPU:: " + str(cmd_output1) + "%")
    finally:
        print("2nd")


def test_memory(connection):
    print("paramiko opration for memory")
    try:
        (stdin, stdout, stderr) = client.exec_command("vmstat |  tail -n 1 | awk '{print $4}'")
        cmd_output2 = stdout.read()
        print(str(cmd_output2))
        list1 = [r"\n", "'", "b"]
        for i in list1:
            cmd_output2 = str(cmd_output2).replace(i, "")
        x = re.findall("\d{7}", cmd_output2)
        value = float(x[0])
        assert value < 3000000

        with open(output_file, "a+") as file:
            file.write("\t" + "memory:: " + str(cmd_output2) + "KB")
    finally:
        print("3rd")
