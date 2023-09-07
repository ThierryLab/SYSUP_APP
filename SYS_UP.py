from netmiko import ConnectHandler, NetMikoAuthenticationException , NetmikoTimeoutException, NetmikoBaseException
from prettytable import PrettyTable
import yaml


def get_external_data():
    host_info = "host_info.yaml"
    with open ("host_info.yaml") as file:
        data = yaml.safe_load(file)
    return data


hosts_IOS = {}
hosts_IOS_XR ={}
hosts_NOKIA_SROS= {}
external_data = get_external_data()
username = external_data["user_pass"]["my_username"]
my_pass  = external_data["user_pass"]["my_password"]
hosts_IOS["IOS"]    = external_data["IOS_IOS_XE"]
hosts_IOS_XR["IOS_XR"]     = external_data["IOS_XR"]
hosts_NOKIA_SROS["NOKIA_SROS"]     = external_data["NOKIA_SROS"]



def host_connect_parameters(hostname, os_type):
    dev_params = {
        "device_type": os_type,
        "host": hostname,
        "username": username,
        "password": my_pass
        }
    return dev_params




def connect_to_dev(hosts, comand, dev_os):
    hostinf={}
    host_sys_info = []
    for host in hosts:
        print("Gathering data on {}".format(host))
        host_params = host_connect_parameters(host, dev_os)
        try:
            with ConnectHandler(**host_params) as dev_connect:
                result = dev_connect.send_command(comand, use_textfsm=True)
                #print(result)
                host_sys_info.append(result[0])
        except NetMikoAuthenticationException:
            print("WARNING!!! AUTHENTICATION FAILED - DEVICE: {} ".format(host))
        except NetmikoTimeoutException:
            print("WARNING!!! DEVICE {} NOT REACHABLE OR SSH NOT ENABLED".format(host))
    return host_sys_info




# for devices with  non use_textfsm support  
def tl_dev_output(hosts, sros_command, dev_os, key_comand_ref="result"):
    per_dev_output_collectionnfo = []
    try:
        for host in hosts:
            output_collection = {}
            print("Gathering data on {}".format(host))
            dev = host_connect_parameters(host, dev_os)
            with ConnectHandler(**dev) as dev_connect:
                dev_output = dev_connect.send_command(sros_command)
                output_collection["hostname"] = host
                output_collection[key_comand_ref] = dev_output.split(" : ")[1].strip("sec")
                per_dev_output_collectionnfo.append(output_collection)
    except NetMikoAuthenticationException:
        print("WARNING!!! AUTHENTICATION FAILED - DEVICE: {} ".format(host))
    except NetmikoTimeoutException:
        print("WARNING!!! DEVICE {} NOT REACHABLE OR SSH NOT ENABLED".format(host))      
    return per_dev_output_collectionnfo





def global_dev_info(hosts, comand, sros_command="", key_comand_ref="result" ):
    total_dev_groups = len(hosts)
    host_details = []
    for x_element in range(total_dev_groups):
        for k , v in hosts[x_element].items():
            if k == "NOKIA_SROS":
                dev_os = "nokia_srl"
                _NOKIA_conect_details = tl_dev_output(v, sros_command,dev_os, key_comand_ref=key_comand_ref )
                host_details += _NOKIA_conect_details
            else:
                dev_os = "cisco_ios"
                host_details += connect_to_dev(v,comand, dev_os)
    return host_details





def sys_up_table(devs_grp):
        table_view = PrettyTable(["DEVICES", "UPTIME"])
        devs_info = global_dev_info(devs_grp, "show version", sros_command="show uptime", key_comand_ref="uptime")
        if len(devs_info) > 0:
            print("")
            print("        UPTIME PER DEVICE - SUMMARY VIEW  ")
            for info in devs_info:
                hostname = info["hostname"]
                uptime = info["uptime"]
                table_view.add_row([hostname, uptime])
            return table_view
        else:
            print("Device info not found, please ssh and devices reachability")


sys_up_view = sys_up_table([hosts_IOS_XR, hosts_IOS, hosts_NOKIA_SROS])
print(sys_up_view)

print("MIT License")
print("Copyright (c) 2023 ThierryLab.com")
