from scapy.all import ARP, Ether, srp
import socket
import ipaddress
import platform

def get_subnet():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()

    return str(ipaddress.IPv4Network(local_ip + "/24", strict=False))

def arp_scan(network):
    print(f"Scanning your subnet: {network}")
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append((received.psrc, received.hwsrc))

    if devices:
        for ip, mac in devices:
            print(f"{ip}: {mac}")
        print(f"There are {len(devices)} devices on your subnet.")    
    else:
        print("No communicators or devices could be found.")

if __name__ == "__main__":
    network = get_subnet()
    arp_scan(network)
