import ipaddress
import sys
from ipwhois import IPWhois

GREEN = "\033[1;32m"
RESET = "\033[0m"

def lookup_ip(ip):
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap()

        print("Autonomous System Info:")
        print("ASN:", results.get("asn"))
        print("ASN Description:", results.get("asn_description"))
        print("ASN Country Code:", results.get("asn_country_code"))
        print("ASN CIDR:", results.get("asn_cidr"))
        print()

        print("Network Info:")
        network = results.get("network", {})
        print("Network Name:", network.get("name"))
        print("CIDR:", network.get("cidr"))
        print("Start Address:", network.get("start_address"))
        print("End Address:", network.get("end_address"))
        print("Country:", network.get("country"))
        print("Type:", network.get("type"))
        print("Status:", network.get("status"))
        print()

        print("Contact Info:")
        objects = results.get("objects", {})
        for handle, obj_data in objects.items():
            roles = obj_data.get("roles", [])
            contact = obj_data.get("contact", {})
            emails = contact.get("email", [])
            name = contact.get("name")
            if roles:
                print()
                print(f"\033[1m{', '.join(roles).title()}\033[0m: {name}")
                if isinstance(emails, list):
                    for email in emails:
                        print(f"Email: {email}")
                else:
                    print(f"Email: {emails}")

    except Exception as e:
        print(f"\033[1;31mRDAP lookup failed:\033[0m {e}")

def ipv4_details(network):
    print(f"{GREEN}Network Address:{RESET} {network.network_address}")
    print(f"{GREEN}Subnet Mask:{RESET} {network.netmask}")
    print(f"{GREEN}Wildcard Mask:{RESET} {network.hostmask}")
    print(f"{GREEN}Total Addresses:{RESET} {network.num_addresses}")
    
    if network.prefixlen < 31:
        print(f"{GREEN}Usable Hosts:{RESET} {network.num_addresses - 2}")
        hosts = list(network.hosts())
        print(f"{GREEN}First Usable:{RESET} {hosts[0]}")
        print(f"{GREEN}Last Usable:{RESET} {hosts[-1]}")
    else:
        print(f"{GREEN}Usable Hosts:{RESET} 0 (point-to-point network)")

    print(f"{GREEN}Broadcast Address:{RESET} {network.broadcast_address}")
    print(f"{GREEN}Reverse DNS Zone:{RESET} {network.reverse_pointer}")

def ipv6_details(network):
    print(f"{GREEN}Network Address:{RESET} {network.network_address}")
    print(f"{GREEN}Prefix Length:{RESET} /{network.prefixlen}")
    print(f"{GREEN}Total Addresses:{RESET} {network.num_addresses}")
    print(f"{GREEN}Reverse DNS Zone:{RESET} {network.reverse_pointer}")
    print(f"{GREEN}Is Multicast?:{RESET} {network.is_multicast}")
    print(f"{GREEN}Is Link Local?:{RESET} {network.is_link_local}")
    print(f"{GREEN}Is Global?:{RESET} {network.is_global}")

def main():
    if len(sys.argv) != 2:
        print(f"\033[1;32mUsage: python subnetcalc.py <cidr>\033[0m")
        print("Example: python subnetcalc.py 192.168.1.0/24")
        print("Example: python subnetcalc.py 2001:db8::/48")
        sys.exit(1)

    cidr = sys.argv[1]
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if isinstance(net, ipaddress.IPv4Network):
        ipv4_details(net)
        print()
        lookup_ip(str(net.network_address))
    else:
        ipv6_details(net)
        print()
        lookup_ip(str(net.network_address))

if __name__ == "__main__":
    main()