import sys
import socket
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_ports(port_arg):
    if '-' in port_arg:
        try:
            start, end = map(int, port_arg.split('-'))
            if start > end:
                raise ValueError("Start port must be less than or equal to end port")
            return list(range(start, end + 1))
        except ValueError:
            raise ValueError("Invalid port range")
    else:
        try:
            ports = [int(p.strip()) for p in port_arg.split(',')]
            return ports
        except ValueError:
            raise ValueError("Invalid port list")

def scan_port(host, port, timeout=1.0):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return {'port': port, 'status': 'open'}
        except (socket.timeout, ConnectionRefusedError, OSError):
            return {'port': port, 'status': 'closed'}

def output_results(results, format=None):
    if format == 'json':
        with open('scan_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("\nResults saved to scan_results.json")
    elif format == 'csv':
        with open('scan_results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['port', 'status'])
            writer.writeheader()
            writer.writerows(results)
        print("\nResults saved to scan_results.csv")

def main():
    if len(sys.argv) < 3:
        print("\033[1;32mUsage: python portscanner.py <host> <port(s)> [json|csv]\033[0m")
        print("Ports can be a range (20-80) or comma-separated (22,80,443)")
        sys.exit(1)

    host = sys.argv[1]
    ports_arg = sys.argv[2]
    format = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        ports = parse_ports(ports_arg)
    except ValueError as e:
        print("Error parsing ports:", e)
        sys.exit(1)

    print(f"Scanning {host} on ports: {', '.join(map(str, ports))}")

    results = []
    max_threads = min(100, len(ports))

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(scan_port, host, port): port for port in ports}
        for future in as_completed(future_to_port):
            result = future.result()
            results.append(result)
            print(f"Port {result['port']}: {result['status']}")

    print("\nSorted scanned ports")
    for r in sorted(results, key=lambda x: x['port']):
        print(f"Port {r['port']}: {r['status']}")

    if format:
        output_results(results, format)

if __name__ == "__main__":
    main()
