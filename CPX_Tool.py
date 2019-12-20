#This is an excercise based on an interview challenge provided by a London-based company operating in the financial services sector
#It did not pass, though delivers functional code for a CLI tool.
#I have added the code to my repo on GitHub as I wish to leverage it for an AWS tool set later down the line.

import subprocess
import pandas as pd
import statistics
import time
LIST_OF_SERVICES_BY_IP = list()



#1. return a printout of all running hosts and corresponding health status, running services, CPU and memory usage stats
def run_services():
    print(running_services())

def status_maker(list):
    status = []
    for item in list:
        newItem = str(item)
        x =newItem.split(',')
        matching = [s for s in x if "cpu" in s]
        for i in matching:
            n = str(i)
            y = n.replace(" ","").replace("%","").replace("cpu:",'')
            num = int(y)
            if num >= 80:
                status.append('unhealthy')
            else: status.append('healthy')
    return status

def running_services():
    df = pd.DataFrame({'IP':[],
                       'Service':[],
                       'Status':[],
                       'CPU':[],
                       'Memory':[]})
    IPs = []
    print("Working on providing your running services now")
    x = subprocess.run("curl localhost:8081/servers", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    y = str(x)
    newString = y.replace('"',' ')
    newString = newString.replace("[","").replace("]","").replace("]","").replace(" ","").replace(","," ")
    l= list(newString.split(" "))
    for ip in l:
        n = subprocess.run("curl localhost:8081/"+ip, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        xString = str(n)
        resultStringPerIP = xString.replace("{"," ").replace('"','').replace("}","")
        resultStringPerIP = ip+","+resultStringPerIP
        LIST_OF_SERVICES_BY_IP.append(resultStringPerIP)
    #below calls for status
    status = status_maker(LIST_OF_SERVICES_BY_IP)
    count = 0
    for item in LIST_OF_SERVICES_BY_IP:
        service_married_to_ip = item
        splitService = service_married_to_ip.split(",")
        df3 = pd.DataFrame({'IP':[splitService[0]],
                           'Service':[splitService[3]],
                           'Status': [status[count]],
                           'CPU':[splitService[1]],
                           'Memory': [splitService[2]]})
        df = df.append(df3)
        count= count+1
    pd.set_option('display.max_rows', None)
    return(df)

#2. take a service and return average usage of memory and CPU
def Average_Use_of_Service(service):
    cpu_list=[]
    mem_list=[]
    print ("Working on "+ service)
    df = pd.DataFrame()
    df = df.append(running_services())
    print('\nThe following instances were found to be running the '+service+' service\n')
    print(df[df.Service.str.contains(service)])
    df2 = df[df.Service.str.contains(service)]
    for row, index in df2.iterrows():
        cpu = str(df2.CPU)
        cpu2 = cpu.replace('%','').replace('cpu: ','').replace(" ",'').replace('\n',',').replace('Name:CPU,dtype:object','')
    cpu_list = list(cpu2.split(','))
    del cpu_list[-1]
    cpu_list2 =[]
    for item in cpu_list:
        num = int(item)
        cpu_list2.append(num)
    print('\n'+ '\033[95m'+'\033[1m' + 'Average CPU usage for '+service+' = ', statistics.mean(cpu_list2))
    for row, index in df2.iterrows():
        mem = str(df2.Memory)
        mem2 = mem.replace('%','').replace('memory: ','').replace(" ",'').replace('\n',',').replace('Name:Memory,dtype:object','')
    mem_list = list(mem2.split(','))
    del mem_list[-1]
    mem_list2 = []
    for item in mem_list:
        num1 = int(item)
        mem_list2.append(num1)
    print('\n'+ '\033[95m'+'\033[1m' + 'Average memory usage for '+service+' = ', statistics.mean(mem_list2))

#3. Flag services with fewer that 2 healthy instances running
def Flag_Services_With_Less_That_Two_Healthy_Instances():
    services = ['PermissionsService','AuthService','MLService','TimeService','GeoService','IdService','StorageService','UserService','RoleService','TicketService']
    df = running_services()
    for service in services:
        df2 = df[df.Service.str.contains(service)]
        df3 = df2[df2.Status.str.contains('healthy')]
        if len(df3.index) < 2:
            print('\033[91m'+"Warning - there are only two healthy instances for "+service)
        else: print("Nothing to flag - services are all operating with > 2 healthy instances")
    pd.set_option('display.max_rows', None)

#4 Have the ability to track and print CPU/Memory of all instances of a given service over time (until the command is stopped, e.g. ctrl + c).
def cpu_memory_tracker(service):
    print("Tracking "+service+' now. Press Ctrl+c to stop')
    while True:
        df = running_services()
        df2 = df[df.Service.str.contains(service)]
        print(df2)
        time.sleep(10)


#Start of Script: basic selection of which API service to use. The assumption here is that the required keys/secrets (for example, access keys and secrets in AWS)
#are provided already in the CLI tool configuration - elsewise I would write an initial configuration that takes kesy and secrets as the input and pumps those out
# in order to bash to configure the CLI tool to have the proper permissions to make those requests. I am also assuming that this script will run on keys that have
# admin rights, and I have not included "unauthorized" returns.
def main():
    print("Please choose the service you would like \n"
      "1. a view of all running services \n2. A view of the average CPU/memory usage of a particular service \n3. Flag services with fewer than 2 healthy services running\n4. track and print CPU/Memory of all instances of a given service over time (until the command is stopped, e.g. ctrl + c)")

    selection = input("Make your selection by typing a number: ")
    print("you selected " + selection)
    if selection == "1":
        run_services()
    elif selection == "2":
        print("Choose from the following services: \n1. PermissionsService\n2. AuthService\n3. MLService\n4. StorageService\n5. GeoService\n6. TimeService\n7. IdService\n8. UserService\n9. RoleService\n10. TicketService")
        selection = input("Please type the number of the service: ")
        if selection == "1":
            service = "PermissionsService"
        elif selection == "2":
            service = "AuthService"
        elif selection == "3":
            service = "MLService"
        elif selection == '4':
            service = 'StorageService'
        elif selection == '5':
            service = 'GeoService'
        elif selection == '6':
            service = 'TimeService'
        elif selection == '7':
            service = 'IdService'
        elif selection == '8':
            service = 'UserService'
        elif selection == '9':
            service = 'RoleService'
        elif selection == '10':
            service = 'TicketService'
        Average_Use_of_Service(service)
    elif selection == "3":
        Flag_Services_With_Less_That_Two_Healthy_Instances()
    elif selection == '4':
        print("Choose from the following services: \n1. PermissionsService\n2. AuthService\n3. MLService\n4. StorageService\n5. GeoService\n6. TimeService\n7. IdService\n8. UserService\n9. RoleService\n10. TicketService")
        selection = input("Please type the number of the service: ")
        if selection == "1":
            service = "PermissionsService"
        elif selection == "2":
            service = "AuthService"
        elif selection == "3":
            service = "MLService"
        elif selection == '4':
            service = 'StorageService'
        elif selection == '5':
            service = 'GeoService'
        elif selection == '6':
            service = 'TimeService'
        elif selection == '7':
            service = 'IdService'
        elif selection == '8':
            service = 'UserService'
        elif selection == '9':
            service = 'RoleService'
        elif selection == '10':
            service = 'TicketService'
        cpu_memory_tracker(service)
    else:
        print('Incorrect selection - try again')
        main()

if __name__ == "__main__":
    main()


