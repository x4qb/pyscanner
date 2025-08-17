import sys
import requests

def mac_lookup(mac):
    url = f"https://api.macvendors.com/{mac}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"\033[1;32mMAC Address:\033[0m {mac}")
            print(f"\033[1;32mVendor:\033[0m {response.text}")
        else:
            print(f"\033[1;31mLookup failed:\033[0m HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"\033[1;31mError:\033[0m {e}")

def main():
    if len(sys.argv) != 2:
        print(f"\033[1;32mUsage: python maclookup.py <mac_address>\033[0m")
        print("Example: python maclookup.py 44:38:39:ff:ef:57")
        print("Info is pulled from an API and may be rate limited.")
        sys.exit(1)

    mac_lookup(sys.argv[1])

if __name__ == "__main__":
    main()
