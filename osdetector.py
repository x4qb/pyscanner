import platform
import subprocess
from scapy.all import IP, TCP, sr1

def get_ttl(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(["ping", param, "1", host], universal_newlines=True)
        for line in output.splitlines():
            if "ttl=" in line.lower():
                ttl = int(line.lower().split("ttl=")[1].split()[0])
                return ttl
    except Exception as e:
        return None

def get_tcp_window(host, port=80):
    try:
        pkt = IP(dst=host)/TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=2, verbose=0)
        if resp and resp.haslayer(TCP):
            return resp[TCP].window
    except Exception as e:
        return None

def detect_os(host):
    ttl = get_ttl(host)
    window = get_tcp_window(host)

    os_guess = []

    if ttl:
        if ttl <= 64:
            os_guess.append("Linux or Unix")
        elif ttl <= 128:
            os_guess.append("Windows")
        elif ttl <= 255:
            os_guess.append("Router/Network Device")

    if window:
        if window == 65535:
            os_guess.append("Windows")
        elif window == 8192:
            os_guess.append("Linux")
    
    if os_guess:
        return ", ".join(os_guess)
    return "Unknown"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"\033[1;32mUsage: python osdetector.py <host>\033[0m")
        sys.exit(1)

    host = sys.argv[1]
    result = detect_os(host)
    print(f"\033[1;32mHost: {host}\033[0m")
    print(f"\033[1;32mLikely OS: \033[0m{result}")
