import paramiko
import re

output_file = "paramiko.log"


def test_operation():
    print("paramiko opration")
    try:
        port = 22
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname="192.168.43.166", port=22, username="node1", password="Rk@8531")
        (stdin, stdout, stderr) = client.exec_command("df --output=source,pcent /dev/sda3")
        (stdin1, stdout1, stderr1) = client.exec_command("date")
        cmd_output = stdout.read()
        TimeStamp = stdout1.read()
        cmd_output = str(cmd_output).replace(r"\n", "")
        TimeStamp = str(TimeStamp).replace(r"\n", "")
        x = re.findall("\d{2}", cmd_output)
        value = int(x[0])
        assert value < 80

        with open(output_file, "a+") as file:
            file.write("\n" + "TimeStamp" + "\t" + "file name" + "\t" + "percentage")
            file.write("\n" + str(TimeStamp) + "\t" + str(cmd_output))

        return output_file
    finally:
        client.close()
