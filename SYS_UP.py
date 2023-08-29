from netmiko import ConnectHandler, NetMikoAuthenticationException , NetmikoTimeoutException, NetmikoBaseException
from prettytable import PrettyTable
import yaml

def get_external_data():
    host_info = "host_info.yaml"
    with open ("host_info.yaml") as file:
        data = yaml.safe_load(file)
    return data

external_data = get_external_data()
username = external_data["user_pass"]["my_username"]
my_pass  = external_data["user_pass"]["my_password"]
hosts    = external_data["hosts"]


def host_connect_parameters(hostname):
    dev_params = {
        "device_type": "cisco_ios",
        "host": hostname,
        "username": username,
        "password": my_pass
        }
    return dev_params

def connect_to_dev():
    hostinf={}
    host_sys_info = []
    for host in hosts:
        print("Gathering data on {}".format(host))
        host_params = host_connect_parameters(host)
        try:
            with ConnectHandler(**host_params) as dev_connect:
                result = dev_connect.send_command("show version" , use_textfsm=True)
                host_sys_info.append(result[0])
        except NetMikoAuthenticationException:
            print("WARNING!!! AUTHENTICATION FAILED - DEVICE: {} ".format(host))
        except NetmikoTimeoutException:
            print("WARNING!!! DEVICE {} NOT REACHABLE OR SSH NOT ENABLED".format(host))

    return host_sys_info

def sys_up_view():
    table_view = PrettyTable(["DEVICES", "UPTIME"])
    host_details = connect_to_dev()
    if len(host_details) > 0:
        print("")
        print("    UPTIME PER DEVICE - SUMMARY VIEW  ")
        for info in host_details:
            hostname = info["hostname"]
            uptime = info["uptime"]
            table_view.add_row([hostname, uptime])
        return table_view
    else:
        print("Device info not found, please ssh and devices reachability")

print(sys_up_view(), "\n")

print("MIT License")
print("Copyright (c) 2023 ThierryLab.com")