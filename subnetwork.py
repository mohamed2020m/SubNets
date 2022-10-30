## Author: Leeuw
## 10/30/22
## find in at: 

import argparse
from tabulate import tabulate
import csv

# Initialize parser
parser = argparse.ArgumentParser(prog="SubNets")

# Adding optional argument
parser.add_argument('-v', '--version', action="version", version="%(prog)s 0.1", help = "Show current version")
parser.add_argument('-ip', nargs='?', const='192.168.0.0', default='192.168.0.0', help = "IP4 Address of a Network")
parser.add_argument('-bit', '--BitsToBorrow', nargs='?', const='3', default='3', help= 'How many bits to borrow from hosts part in IP')
parser.add_argument('--export', nargs='?', const='SubNet', help= 'Export to a csv file, default name of the file is SubNet')

# Read arguments from command line
args = parser.parse_args()

def ValidIP(ip):
    '''Return True if ip is a valid IP4 address, False in the other case'''
    
    ip_list = ip.split('.')

    # Checking that there are four field in the ip
    if len(ip_list) != 4:
        return False

    # Check that all the ip field are type int
    if not all([field.isnumeric() for field in ip_list]):
        return False

    if not all([0 <= int(field) <= 255 for field in ip_list]):
        return False

    return True

def ValidIPNetwork(ip):
    '''Check if the ip given is a network ip. for example 192.168.0.1 isn't a valid ip network. However, 192.168.0.0 is it.'''
    if ValidIP(ip):
        ip_list = [int(f) for f in ip.split(".")]
        if DetectIPClass(ip) == 'A':
            f2, f3, f4 = ip_list[1], ip_list[2], ip_list[-1]
            if f2 == f3 == f4 == 0:
                return True
            return False
        elif DetectIPClass(ip) == 'B':
            f3, f4 = ip_list[2], ip_list[-1]
            if f3 == f4 == 0:
                return True
            return False
        elif DetectIPClass(ip) == 'C':
            last_ip_field = ip_list[-1]
            if last_ip_field == 0:
                return True
            return False            
    return False

def DetectIPClass(ip):
    '''Detect which class ip belong to'''
    if ValidIP(ip):
        first_ip_field = int(ip.split(".")[0])
        if first_ip_field <= 127:
            return 'A'
        elif first_ip_field <= 191:
            return 'B'
        elif first_ip_field <= 223:
            return 'C'
    return -1

def SubMask(ip):
    '''Generating the Submask depend on the bits borrowed and the type of IP4 class'''
    
    ip_class = DetectIPClass(ip) 
    
    if ip_class == 'A':
        return '255.0.0.0'
    elif ip_class == 'B':
        return '255.255.0.0'
    elif ip_class == 'C' :
        return '255.255.255.0'
    return -1 
    
def numSubNetworks(n):
    '''Calculating the number of subnetworks'''
    if n.isnumeric():
        return 2**int(n)
    return -1

def numHosts(ip, n):
    '''Calculating the number of hosts for each subnetwork'''
    
    if not n.isnumeric(): 
        return -1
    
    host_bits = 0

    if DetectIPClass(ip) == 'A':
        host_bits = 24
    elif DetectIPClass(ip) == 'B':
        host_bits = 16
    elif DetectIPClass(ip) == 'C':
        host_bits = 8

    m = host_bits - int(n)

    return 2**m - 2


def SubNetorks(ip, n):
    '''Return a list of dic objects that contains all the subnetworks of the IP given'''
    
    if not ValidIPNetwork(ip):
        return -1
    
    arr = []
    dicData = dict()
    f1, f2, f3, f4 = ip.split(".")

    if DetectIPClass(ip) == 'A':
        f2 = int(f2)
        f3 = int(f3)
        f4 = int(f4)
        for i in range(numSubNetworks(n)):
            if int(n) < 8:
                min = f2
                dicData["id"] = i + 1
                dicData["Network IP"] = f'{f1}.{f2}.{f3}.{f4}'
                f2 += int(((numHosts(ip, n) + 2) * 2**(-16)))
                max = f2 - 2
                dicData["Usable Host IP Range"] = f"[{f1}.{min}.0.1 - {f1}.{max}.255.254]"
                dicData["IP Broadcast"] = f"{f1}.{max + 1}.255.255"
            elif int(n) < 16:
                if f3 == 256 :
                    f2 += 1
                    f3 = 0
                min = f3
                dicData["id"] = i + 1
                dicData["Network IP"] = f'{f1}.{f2}.{f3}.{f4}/{8 + int(n)}'
                f3 += int(((numHosts(ip, n) + 2) * 2**(-8)))
                max = f3 - 1
                dicData["Usable Host IP Range"] = f"[{f1}.{f2}.{min}.1 - {f1}.{f2}.{max}.254]"
                dicData["IP Broadcast"] = f"{f1}.{f2}.{max}.255"
            else:
                if f4 == 256 :
                    f3 += 1
                    f4 = 0
                if f3 == 256 :
                    f2 += 1
                    f3 = 0
                min = f4 + 1
                dicData["id"] = i + 1
                dicData["Network IP"] = f'{f1}.{f2}.{f3}.{f4}'
                f4 += (numHosts(ip, n) + 2)
                max = f4 - 2
                dicData["Usable Host IP Range"] = f"[{f1}.{f2}.{f3}.{min} - {f1}.{f2}.{f3}.{max}]"
                dicData["IP Broadcast"] = f"{f1}.{f2}.{f3}.{max + 1}"
            arr.append(dicData)
            dicData = {}
        return arr
    elif DetectIPClass(ip) == 'B':
        f3 = int(f3)
        f4 = int(f4)
        for i in range(numSubNetworks(n)):
            if int(n) >= 8:
                if f4 == 256 :
                    f3 += 1
                    f4 = 0
                min = f4 + 1
                dicData["id"] = i + 1
                dicData["Network IP"] = f'{f1}.{f2}.{f3}.{f4}'
                f4 += (numHosts(ip, n) + 2)
                max = f4 - 2
                dicData["Usable Host IP Range"] = f"[{f1}.{f2}.{f3}.{min} - {f1}.{f2}.{f3}.{max}]"
                dicData["IP Broadcast"] = f"{f1}.{f2}.{f3}.{max + 1}"
            else:
                min = f3
                dicData["id"] = i + 1
                dicData["Network IP"] = f'{f1}.{f2}.{f3}.{f4}'
                f3 += int(((numHosts(ip, n) + 2) * 2**(-8)))
                max = f3 - 2
                dicData["Usable Host IP Range"] = f"[{f1}.{f2}.{min}.1 - {f1}.{f2}.{max}.254]"
                dicData["IP Broadcast"] = f"{f1}.{f2}.{max + 1}.255"
            arr.append(dicData)
            dicData = {}
        return arr
    elif DetectIPClass(ip) == 'C':
        f4 = int(f4) 
        for i in range(numSubNetworks(n)):
            min = f4 + 1
            dicData["id"] = i + 1
            dicData["Network IP"] = f'{f1}.{f2}.{f3}.{f4}'
            f4 += (numHosts(ip, n) + 2)
            max = f4 - 2
            dicData["IP interval"] = f"[{f1}.{f2}.{f3}.{min} - {f1}.{f2}.{f3}.{max}]"
            dicData["IP Broadcast"] = f"{f1}.{f2}.{f3}.{max + 1}"
            arr.append(dicData)
            dicData = {}
        return arr
    return -1

def DisplayTable(iterable):
    '''Display a Table that shows all the SubNetworks exist'''
    if(iterable == -1):
        print("Error!")
        return -1
    print(tabulate(iterable, headers="keys", tablefmt="orgtbl"))


try:
    if args.export:
        with open(f"{args.export}.csv", 'w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'Network IP', 'Usable Host IP Range', 'IP Broadcast'])
            writer.writeheader()
            for dic in SubNetorks(args.ip, args.BitsToBorrow):
                writer.writerow(dic)
        print("Exported Successfully")
    else:
        DisplayTable(SubNetorks(args.ip, args.BitsToBorrow))
    
except argparse.ArgumentError as err:
    print(err)
