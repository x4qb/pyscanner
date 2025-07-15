import sys
import requests

def geolocate_ip(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['status'] == 'success':
            print(f"\033[1;32mIP address\033[0m: {data['query']}")
            print(f"\033[1;32mCountry\033[0m: {data['country']} ({data['countryCode']})")
            print(f"\033[1;32mRegion\033[0m: {data['regionName']}")
            print(f"\033[1;32mCity\033[0m: {data['city']}")
            print(f"\033[1;32mZIP\033[0m: {data['zip']}")
            print(f"\033[1;32mInternet Service Provider\033[0m: {data['isp']}")
            print(f"\033[1;32mOrganization\033[0m: {data['org']}")
            print(f"\033[1;32mAutonomous system\033[0m: {data['as']}")
            print(f"\033[1;32mTimezone\033[0m: {data['timezone']}")
            print(f"\033[1;32mApproximate latitude\033[0m: {data['lat']}")
            print(f"\033[1;32mApproximate longitude\033[0m: {data['lon']}")
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
