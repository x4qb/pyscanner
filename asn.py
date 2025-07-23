import sys
from ipwhois import IPWhois

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

def main():
    if len(sys.argv) != 2:
        print("\033[1;32mUsage: python asn.py <ip>\033[0m")
        sys.exit(1)

    ip = sys.argv[1]
    lookup_ip(ip)

if __name__ == "__main__":
    main()
