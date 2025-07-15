import sys
import requests

def geolocate_ip(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['status'] == 'success':
            print(f"IP address: {data['query']}")
            print(f"Country: {data['country']} ({data['countryCode']})")
            print(f"Region: {data['regionName']}")
            print(f"City: {data['city']}")
            print(f"ZIP: {data['zip']}")
            print(f"Internet Service Provider: {data['isp']}")
            print(f"Organization: {data['org']}")
            print(f"Autonomus system: {data['as']}")
            print(f"Timezone: {data['timezone']}")
            print(f"Approximate latitude: {data['lat']}")
            print(f"Approximate longitude: {data['lon']}")
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"Error fetching geolocation: {e}")

def main():
    if len(sys.argv) != 2:
        print("\033[1;32mUsage: python ipgeo.py <ip>\033[0m")
        print("Geolocation info may be rate limited by the provider after too many requests")
        sys.exit(1)
    ip = sys.argv[1]
    geolocate_ip(ip)

if __name__ == "__main__":
    main()
