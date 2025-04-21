"""
Efficient Subnet Calculator
Author: Leeuw
Created: 10/30/22
Updated: 2025-04-21
"""

import argparse
import ipaddress
import csv
from tabulate import tabulate
from math import log2, ceil

def parse_args():
    parser = argparse.ArgumentParser(description="Correct Subnet Calculator")
    parser.add_argument('-ip', type=str, default="192.168.0.0/24", help="Base network (CIDR, e.g. 192.168.0.0/24)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--subnets', type=int, help="Number of desired subnets")
    group.add_argument('--hosts', type=int, help="Minimum number of hosts per subnet")
    parser.add_argument('--export', nargs='?', const='subnets', help="Export to CSV file")
    return parser.parse_args()

def calc_new_prefix_by_subnets(base_prefix, num_subnets):
    extra_bits = ceil(log2(num_subnets))
    return base_prefix + extra_bits

def calc_new_prefix_by_hosts(min_hosts):
    needed_host_bits = ceil(log2(min_hosts + 2))  # +2 for network & broadcast
    return 32 - needed_host_bits

def generate_subnets(base_net, new_prefix):
    return list(base_net.subnets(new_prefix=new_prefix))

def format_subnet_data(subnets):
    data = []
    for i, net in enumerate(subnets, 1):
        hosts = list(net.hosts())
        row = {
            "ID": i,
            "Network": str(net.network_address),
            "CIDR": f"/{net.prefixlen}",
            "Usable IP Range": f"{hosts[0]} - {hosts[-1]}" if len(hosts) >= 2 else "N/A",
            "Broadcast": str(net.broadcast_address),
            "Total IPs": net.num_addresses,
            "Usable Hosts": len(hosts)
        }
        data.append(row)
    return data

def export_csv(data, filename):
    with open(f"{filename}.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"[✓] Exported to {filename}.csv")

def main():
    args = parse_args()

    try:
        base_net = ipaddress.ip_network(args.ip, strict=False)
    except ValueError as e:
        print(f"Invalid IP network: {e}")
        return

    if args.subnets:
        new_prefix = calc_new_prefix_by_subnets(base_net.prefixlen, args.subnets)
    else:
        new_prefix = calc_new_prefix_by_hosts(args.hosts)

    if new_prefix > 30:
        print("⚠️ Cannot subnet beyond /30 — not enough usable IPs.")
        return

    subnets = generate_subnets(base_net, new_prefix)
    data = format_subnet_data(subnets)

    print(tabulate(data, headers="keys", tablefmt="grid"))

    if args.export:
        export_csv(data, args.export)

if __name__ == "__main__":
    main()
