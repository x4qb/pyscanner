import sys
import time
from ping3 import ping, verbose_ping
from ipgeo import geolocate_ip

def simple_ping(host, count=4, delay=1):
    print(f"Sending {count} ICMP packet(s) to {host}:")
    times = []
    for i in range(count):
        rtt = ping(host, timeout=2)
        if rtt is None:
            print(f"Request timed out")
        else:
            ms = round(rtt * 1000, 2)
            print(f"Echo from {host}: time={ms}ms")
            times.append(ms)
        time.sleep(delay)

    print("\nStatistics")
    print(f"Packets: Sent = {count}, Received = {len(times)}, Lost = {count - len(times)} "
          f"({(count - len(times)) / count * 100:.0f}% loss)")

    if times:
        print(f"RTT: Minimum = {min(times)}ms, Maximum = {max(times)}ms, Average = {sum(times)/len(times):.2f}ms")

def main():
    if len(sys.argv) < 2:
        print("\033[1;32mUsage: python icmp.py <host> [packet_count] [delay_between_packet]\033[0m")
        sys.exit(1)

    host = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    delay = float(sys.argv[3]) if len(sys.argv) > 3 else 1
    geo = len(sys.argv) > 4 and sys.argv[4].lower() == "true"

    if geo:
        location = geolocate_ip(host)
        print(location, "\n-------")

    simple_ping(host, count, delay)

if __name__ == "__main__":
    main()
