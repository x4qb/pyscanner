import whois
import sys

labels = {
    'domain_name': "Domain name",
    'registrar': "Registrar",
    'registrar_url': "Registrar URL",
    'reseller': "Reseller",
    'whois_server': "WHOIS Server",
    'referral_url': "Referral URL",
    'updated_date': "Updated Date",
    'creation_date': "Creation Date",
    'expiration_date': "Expiration Date",
    'name_servers': "Name Servers",
    'status': "Domain Status",
    'emails': "Emails",
    'dnssec': "DNSSEC",
    'name': "Name",
    'org': "Organization",
    'address': "Address",
    'city': "City",
    'state': "State",
    'registrant_postal_code': "Registrant Postal Code",
    'country': "Country"
}


def lookup(domain):
    try:
        w = whois.whois(domain)
        for key, label in labels.items():
            value = w.get(key)
            if value:
                print(f"\033[1;32m{label}\033[0m: {value}")
            
    except Exception as e:
        print(f"Couldn't get WHOIS info for {domain}. {e}")

def main():
    if len(sys.argv) != 2:
        print("\033[1;32mUsage: python whoislookup.py <domain>\033[0m")
        sys.exit(1)

    domain = sys.argv[1]
    lookup(domain)

if __name__ == "__main__":
    main()
