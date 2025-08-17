import sys
import dns.resolver
import dns.reversename

def lookup_records(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        for rdata in answers:
            if record_type == 'A' or record_type == 'AAAA':
                print(f"{record_type} record: {rdata.address}")
            elif record_type == 'CNAME':
                print(f"CNAME record: {rdata.target}")
            elif record_type == 'MX':
                print(f"MX record: preference={rdata.preference}, exchange={rdata.exchange}")
            elif record_type == 'TXT':
                txt = ''.join([part.decode('utf-8') for part in rdata.strings])
                print(f"TXT record: {txt}")
            elif record_type == 'NS':
                print(f"NS record: {rdata.target}")
            elif record_type == 'SOA':
                print(f"SOA record: mname={rdata.mname}, rname={rdata.rname}, serial={rdata.serial}, refresh={rdata.refresh}, retry={rdata.retry}, expire={rdata.expire}, minimum={rdata.minimum}")
            elif record_type == 'SRV':
                print(f"SRV RECORD: priority={rdata.priority}, weight={rdata.weight}, port={rdata.port}, target={rdata.target}")
            elif record_type == 'PTR':
                print(f"PTR record: {rdata.target}")
            else:
                print(f"{record_type} record: {rdata}")
    except dns.resolver.NXDOMAIN:
        print(f"Domain does not exist for {record_type} record.")
    except dns.resolver.NoAnswer:
        print(f"No {record_type} records found.")
    except dns.resolver.Timeout:
        print(f"Query timed out for {record_type} record.")
    except Exception as e:
        print(f"Error fetching {record_type} records: {e}")

def main():
    if len(sys.argv) < 2:
        print("\033[1;32mUsage: python dnslookup.py <domain or ip> [uncommon_records|default:false]\033[0m")
        print(f"Meaning of each record:\nA and AAAA records are ip address records.\nCNAME records are Canonical Names\nMXs are Mail Exchange records\nTXT records are Text\nNS are Name Server Records\nSOA records are Start Of Authority Records\nSRVs are Service Records\nPTRs are records on an ip address that connects it to a hostname typically for Reverse DNS\nFull list: https://en.wikipedia.org/wiki/List_of_DNS_record_types (not all dns records are supported in this command)")
        sys.exit(1)

    target = sys.argv[1]
    uncommon = sys.argv[2].lower() == "true" if len(sys.argv) > 2 else False

    try:
        import ipaddress
        ip = ipaddress.ip_address(target)
        reverse_name = dns.reversename.from_address(target)
        print(f"Looking up pointer record for IP: {target}")
        lookup_records(str(reverse_name), 'PTR')
    except ValueError:
        print(f"Looking up internet records for domain: {target}")

        common_records = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA", "SRV"]
        uncommon_records = [
        "RP", "MD", "MF", "MB", "MG", "WKS", "HINFO", "MINFO", "AFSDB", "NSAP", "NSAP-PTR", "SIG", "KEY",
        "PX", "GPOS", "LOC", "NXT", "NAPTR", "KX", "CERT", "A6", "DNAME", "OPT", "APL", "DS", "SSHFP",
        "IPSECKEY", "RRSIG", "NSEC", "DNSKEY", "DHCID", "NSEC3", "NSEC3PARAM", "TLSA", "SMIMEA", "HIP",
        "NINFO", "CDS", "CDNSKEY", "OPENPGPKEY", "CSYNC", "ZONEMD", "SVCB", "HTTPS", "SPF", "UNSPEC",
        "NID", "L32", "L64", "LP", "EUI48", "EUI64", "TKEY", "TSIG", "IXFR", "AXFR", "MAILB", "MAILA",
        "ANY", "URI", "CAA", "AVC", "AMTRELAY", "RESINFO", "WALLET", "TA", "DLV"
        ]
    for record in common_records + (uncommon_records if uncommon else []):
        lookup_records(target, record)
        print()

if __name__ == "__main__":
    main()
