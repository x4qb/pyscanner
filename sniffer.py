from scapy.all import sniff, Ether, IP, IPv6, TCP, UDP, ICMP, ARP, DNS, Raw
from colorama import init, Fore, Style

init(autoreset=True)

def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def decode_tcp_flags(flags):
    flags_map = {
        'F': 'FIN',
        'S': 'SYN',
        'R': 'RST',
        'P': 'PSH',
        'A': 'ACK',
        'U': 'URG',
        'E': 'ECE',
        'C': 'CWR',
    }
    return ', '.join(flags_map.get(flag, flag) for flag in flags)

def icmp_type_desc(type_code):
    types = {
        0: "Echo Reply",
        3: "Destination Unreachable",
        4: "Source Quench",
        5: "Redirect",
        8: "Echo Request",
        11: "Time Exceeded",
        12: "Parameter Problem",
        13: "Timestamp Request",
        14: "Timestamp Reply",
        17: "Address Mask Request",
        18: "Address Mask Reply",
    }
    return types.get(type_code, "Unknown")

def print_packet(pkt):
    print("-"*50)
    if pkt.haslayer(Ether):
        ether = pkt[Ether]
        print(f"Ethernet: {ether.src} -> {ether.dst} | Type: {ether.type}")

    if pkt.haslayer(IP):
        ip = pkt[IP]
        ip_src = color_text(ip.src, Fore.GREEN)
        ip_dst = color_text(ip.dst, Fore.GREEN)
        proto_name = {6:"TCP", 17:"UDP", 1:"ICMP"}.get(ip.proto, str(ip.proto))
        print(f"IP: {ip_src} -> {ip_dst} | Protocol: {color_text(proto_name, Fore.MAGENTA)} ({ip.proto})")

    elif pkt.haslayer(IPv6):
        ipv6 = pkt[IPv6]
        ip_src = color_text(ipv6.src, Fore.GREEN)
        ip_dst = color_text(ipv6.dst, Fore.GREEN)
        proto_name = {6:"TCP", 17:"UDP", 58:"ICMPv6"}.get(ipv6.nh, str(ipv6.nh))
        print(f"IPv6: {ip_src} -> {ip_dst} | Next Header: {color_text(proto_name, Fore.MAGENTA)} ({ipv6.nh})")

    if pkt.haslayer(ARP):
        arp = pkt[ARP]
        print(f"ARP: {color_text('who-has', Fore.MAGENTA)} {arp.pdst} tell {arp.psrc} | HWsrc: {arp.hwsrc}")

    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        sport = color_text(str(tcp.sport), Fore.YELLOW)
        dport = color_text(str(tcp.dport), Fore.YELLOW)
        flags_raw = tcp.sprintf("%TCP.flags%")
        flags_decoded = decode_tcp_flags(flags_raw)
        print(f"TCP: {sport} -> {dport} | Flags: {color_text(flags_decoded, Fore.MAGENTA)}")
        print(f"{flags_decoded}")

        if pkt.haslayer(Raw):
            raw_load = pkt[Raw].load.decode(errors="ignore")
            if raw_load.startswith("GET") or raw_load.startswith("POST"):
                print(f"HTTP Request: {raw_load.splitlines()[0]}")
            elif "HTTP/" in raw_load:
                print(f"HTTP Response: {raw_load.splitlines()[0]}")

    if pkt.haslayer(UDP):
        udp = pkt[UDP]
        sport = color_text(str(udp.sport), Fore.YELLOW)
        dport = color_text(str(udp.dport), Fore.YELLOW)
        print(f"UDP: {sport} -> {dport}")

        if udp.sport in [67, 68] or udp.dport in [67, 68]:
            print(f"Dynamic Host Configuration Protocol traffic detected")

        if pkt.haslayer(DNS):
            dns = pkt[DNS]
            qname = dns.qd.qname.decode() if dns.qd else 'N/A'
            print(f"DNS Query for: {qname} | Query/Response flag: {dns.qr}")

    if pkt.haslayer(ICMP):
        icmp = pkt[ICMP]
        type_name = icmp_type_desc(icmp.type)
        print(f"ICMP Type: {color_text(type_name, Fore.MAGENTA)} ({icmp.type}) | Code: {icmp.code}")
        print(f"{type_name}")

    print("\n")

def main():
    print(color_text("Use only with authorization from the network admin", Fore.RED))
    print(color_text("Starting network level packet sniffer. CTRL + C to stop.", Fore.CYAN))
    sniff(prn=print_packet, store=0)

if __name__ == "__main__":
    main()
