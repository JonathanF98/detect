import subprocess as sp
nmap_f = open("nmap.txt", "w")
sp.call(['ip', 'a'], stdout=nmap_f)
ip_address = sp.check_output(['awk', 'FNR == 2 {print $2}', 'nmap.txt'])
