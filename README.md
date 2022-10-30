# SubNets

a command-line tool that enable you to find all the subnetworks, ip intervals and address broadcast for each subnet.

## command line output
[screenshot](C:/Users/TOSHIBA2018/Desktop/subnet.png)

## export to a csv file
[screenshot_of_export_command](C:/Users/TOSHIBA2018/Desktop/subnet_export_to_csv.png)

by default the name of file is SubNet, if you want to choose a different name just add it next to the export option. example

```bash
python subnetwork.py -ip 10.0.0.0 -bit 3 --export CustomisedName
```