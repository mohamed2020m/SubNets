# SubNets

a command-line tool that enable you to find all the SubNetworks: Network IP Usable Host IP Range and IP Broadcast for each subnet.

## command line output
<img width="948" alt="Screenshot 2025-04-21 at 18 48 53" src="https://github.com/user-attachments/assets/bd0c7a56-5844-4dee-ac4f-c9ecdc850e3f" />

## export to a csv file

<img width="931" alt="Screenshot 2025-04-21 at 18 52 13" src="https://github.com/user-attachments/assets/95caa864-fdff-498b-aa6b-eaf8808c7b92" />
<img width="704" alt="Screenshot 2025-04-21 at 18 52 24" src="https://github.com/user-attachments/assets/836e0a08-848c-481c-a71f-675094ff6ccd" />


## Examples
# Generate 4 subnets
```bash
python3 subnetwork.py -ip 192.168.0.0/24 --subnets 4
```

# Minimum 50 hosts per subnet
```bash
python3 subnetwork.py -ip 10.0.0.0/16 --hosts 50
```

# Export results to CSV
```bash
python3 subnetwork.py -ip 10.0.0.0/16 --subnets 8 --export my_subnets
```
