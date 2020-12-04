mport subprocess as sp
nmap_f = open("nmap.txt", "w")
nmap_f2 = open("nmap2.txt", "w")
sp.call(['ip', 'a'], stdout=nmap_f)
sp.call(['grep','-E', 'inet.*wlan0', 'nmap.txt'], stdout=nmap_f2)
ip_address = sp.check_output(['awk', '{print $2}', 'nmap2.txt'])
ip_string = ip_address.decode()
print(ip_string)

ip_string = ip_string.rstrip()
ip_list = ip_string.split(".")
print(ip_list)

boundary = ip_list[0]+'.'+ip_list[1]+'.'+ip_list[2]+'.'+'0/24'
print(boundary)

mac_f = open("mac.txt", "w")
sp.call(['sudo', 'nmap', '-sn', boundary ], stdout=mac_f)
MAC = sp.check_output (['awk', '/MAC Address/', 'mac.txt'])

MAC_string = MAC.decode("ascii")
print(MAC_string)
MAC_list = MAC_string.split("\n")
print(MAC_list)

Devices = []
MAC_addresses = []
for x in MAC_list:
        MAC_addresses.append(x[:30])
        Devices.append(x[30:])

print(MAC_addresses)
print(Devices)