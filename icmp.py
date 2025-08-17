import sys
import time
import random
from ping3 import ping
from ipgeo import geolocate_ip
from scapy.all import IP, ICMP, send

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

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def spoofed_ping(target_ip, spoof_ip, count=4, delay=1, randomize=False):
    print(f"Sending {count} spoofed ICMP packet(s) to {target_ip} from "
          f"{'random IPs' if randomize else spoof_ip}:")
    for _ in range(count):
        src_ip = random_ip() if randomize else spoof_ip
        packet = IP(src=src_ip, dst=target_ip)/ICMP()/("X"*1000)
        send(packet, verbose=0)
        print(f"Sent spoofed ICMP packet from {src_ip} to {target_ip}")
        time.sleep(delay)

def main():
    if len(sys.argv) < 2:
        print("\033[1;32mUsage: python icmp.py <host> [packet_count] [delay_between_packets] [geo] [spoof]\033[0m")
        print("spoof: IP address string or 'true' to spoof random IPs each packet")
        sys.exit(1)

    host = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    delay = float(sys.argv[3]) if len(sys.argv) > 3 else 1
    geo = len(sys.argv) > 4 and sys.argv[4].lower() == "true"
    spoof = sys.argv[5].lower() if len(sys.argv) > 5 else None

    if geo:
        location = geolocate_ip(host)
        print(location, "\n-------")

    if spoof:
        if spoof == "true":
            spoofed_ping(host, spoof_ip=None, count=count, delay=delay, randomize=True)
        elif spoof == "false":
            simple_ping(host, count, delay)
        else:
            spoofed_ping(host, spoof_ip=spoof, count=count, delay=delay)
    else:
        simple_ping(host, count, delay)



if __name__ == "__main__":
    main()
