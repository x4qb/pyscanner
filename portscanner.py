import sys
from scapy.all import IP, TCP, sr1

def parse_ports(port_arg):
    ports = []
    for part in port_arg.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

def syn_scan(host, port, timeout=1):
    packet = IP(dst=host)/TCP(dport=port, flags="S")
    response = sr1(packet, timeout=timeout, verbose=0)
    if response is None:
        return {'port': port, 'status': 'filtered/no response'}
    if response.haslayer(TCP):
        if response[TCP].flags == 0x12:
            rst = IP(dst=host)/TCP(dport=port, flags="R")
            sr1(rst, timeout=timeout, verbose=0)
            return {'port': port, 'status': 'open'}
        elif response[TCP].flags == 0x14:
            return {'port': port, 'status': 'closed'}
    return {'port': port, 'status': 'unknown'}

def main():
    if len(sys.argv) < 3:
        print("\033[1;32mUsage: python portscanner.py <host> <ports>\033[0m")
        print("Ports can be a single number, comma-separated, or ranges (example: 22,80,100-110)")
        sys.exit(1)

    host = sys.argv[1]
    ports_arg = sys.argv[2]
    ports = parse_ports(ports_arg)

    print(f"Performing SYN scan on {host} for ports: {', '.join(map(str, ports))}")
    for port in ports:
        result = syn_scan(host, port)
        print(f"Port {port}: {result['status']}")

if __name__ == "__main__":
    main()
