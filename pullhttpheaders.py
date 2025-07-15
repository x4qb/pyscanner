import sys
import requests

def analyze_headers(domain, headers):
    print(f"HTTP headers for {domain}:\n")
    for header, value in headers.items():
        print(f"{header}: {value}")
    print()

def main():
    if len(sys.argv) < 2:
        print("\033[1;32mUsage: python pullhttpheaders.py <url>\033[0m")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith("http"):
        url = "http://" + url

    try:
        resp = requests.get(url, timeout=5)
        analyze_headers(url, resp.headers)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    main()
