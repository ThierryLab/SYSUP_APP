# SYSUP_APP
I am pretty sure that at least one time in your career you wanted to check the uptime of a list of devices, perhaps just to determine if the root cause of an issue was actually a device reload, in the network infrastructure, or just for a sanity check. 

SYSUP_APP is a basic CLI tool that can be used to check the Device's uptime from a list of Cisco (ios, ios-xe, xr) routers and switches (and nokia - new feature).        

Before running the app, please make sure you’ve installed all the libraries/dependencies found in the requirements.txt file.
Next , update the host_info.yaml file with your current devices IP list and credentials.  for Example:

![image](https://github.com/ThierryLab/SYSUP_APP/assets/81940840/42765618-4987-4b0c-a64b-204eba96058c)




After doing that, go to your terminal (windows/linux/mac), go to directory SYSUP_APP, and execute the command: python SYS_UP.py         
You should see an output almost similar to this one:

![image](https://github.com/ThierryLab/SYSUP_APP/assets/81940840/a59a4f46-6d01-4205-9cdb-e8e547589884)



MIT License
Copyright (c) 2023 ThierryLab.com 




Enjoy it !!!
 
