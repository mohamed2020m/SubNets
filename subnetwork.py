"""
Efficient Subnet Calculator
Author: Leeuw
Created: 10/30/22
Updated: 2025-04-21
"""

import argparse
import ipaddress
from tabulate import tabulate
import csv
import math

def parse_args():
    parser = argparse.ArgumentParser(description="Efficient IPv4 Subnet Calculator")
    parser.add_argument('-ip', type=str, default="192.168.0.0", help="Base network IP (e.g. 192.168.0.0)")
    parser.add_argument('--subnets', type=int, help="Number of subnets desired")
    parser.add_argument('--hosts', type=int, help="Minimum number of usable hosts per subnet")
    parser.add_argument('--export', nargs='?', const='Subnets', help='Export results to CSV (default: Subnets.csv)')
    return parser.parse_args()

def calculate_prefix_for_subnets(base_prefix, num_subnets):
    extra_bits = math.ceil(math.log2(num_subnets))
    return base_prefix + extra_bits

def calculate_prefix_for_hosts(base_prefix, num_hosts):
    needed_bits = math.ceil(math.log2(num_hosts + 2))  # +2 for network & broadcast
    return 32 - needed_bits

def generate_subnets(base_ip, mode, value):
    base_net = ipaddress.ip_network(base_ip, strict=False)
    base_prefix = base_net.prefixlen

    if mode == 'subnets':
        new_prefix = calculate_prefix_for_subnets(base_prefix, value)
    elif mode == 'hosts':
        new_prefix = calculate_prefix_for_hosts(base_prefix, value)
    else:
        raise ValueError("Invalid mode")

    return list(base_net.subnets(new_prefix=new_prefix))

def format_subnet_info(subnets):
    rows = []
    for idx, subnet in enumerate(subnets, 1):
        hosts = list(subnet.hosts())
        row = {
            "ID": idx,
            "Network": str(subnet.network_address),
            "CIDR": f"/{subnet.prefixlen}",
            "Usable Range": f"{hosts[0]} - {hosts[-1]}" if len(hosts) >= 2 else "N/A",
            "Broadcast": str(subnet.broadcast_address),
            "Total Hosts": subnet.num_addresses,
            "Usable Hosts": len(hosts)
        }
        rows.append(row)
    return rows

def export_to_csv(data, filename):
    with open(f"{filename}.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"[✓] Exported to {filename}.csv")

def main():
    args = parse_args()

    if not args.ip:
        print("⚠️ Please specify the ip address with -ip")
        return 
        
    if not args.subnets and not args.hosts:
        print("⚠️ Please specify either --subnets or --hosts")
        return

    mode = 'subnets' if args.subnets else 'hosts'
    value = args.subnets if args.subnets else args.hosts

    try:
        subnets = generate_subnets(args.ip, mode, value)
        rows = format_subnet_info(subnets)
        print(tabulate(rows, headers="keys", tablefmt="fancy_grid"))
        if args.export:
            export_to_csv(rows, args.export)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

