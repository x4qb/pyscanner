print(r"""
                                                                                                              
,-.----.                                                               ,--.         ,--.                      
\    /  \                 .--.--.     ,----..     ,---,              ,--.'|       ,--.'|    ,---,.,-.----.    
|   :    \         ,---, /  /    '.  /   /   \   '  .' \         ,--,:  : |   ,--,:  : |  ,'  .' |\    /  \   
|   |  .\ :       /_ ./||  :  /`. / |   :     : /  ;    '.    ,`--.'`|  ' :,`--.'`|  ' :,---.'   |;   :    \  
.   :  |: | ,---, |  ' :;  |  |--`  .   |  ;. /:  :       \   |   :  :  | ||   :  :  | ||   |   .'|   | .\ :  
|   |   \ :/___/ \.  : ||  :  ;_    .   ; /--` :  |   /\   \  :   |   \ | ::   |   \ | ::   :  |-,.   : |: |  
|   : .   / .  \  \ ,' ' \  \    `. ;   | ;    |  :  ' ;.   : |   : '  '; ||   : '  '; |:   |  ;/||   |  \ :  
;   | |`-'   \  ;  `  ,'  `----.   \|   : |    |  |  ;/  \   \'   ' ;.    ;'   ' ;.    ;|   :   .'|   : .  /  
|   | ;       \  \    '   __ \  \  |.   | '___ '  :  | \  \ ,'|   | | \   ||   | | \   ||   |  |-,;   | |  \  
:   ' |        '  \   |  /  /`--'  /'   ; : .'||  |  '  '--'  '   : |  ; .''   : |  ; .''   :  ;/||   | ;\  \ 
:   : :         \  ;  ; '--'.     / '   | '/  :|  :  :        |   | '`--'  |   | '`--'  |   |    \:   ' | \.' 
|   | :          :  \  \  `--'---'  |   :    / |  | ,'        '   : |      '   : |      |   :   .':   : :-'   
`---'.|           \  ' ;             \   \ .'  `--''          ;   |.'      ;   |.'      |   | ,'  |   |.'     
  `---`            `--`               `---`                   '---'        '---'        `----'    `---'       
                                                                                                              
""")


print("Welcome to PyScanner. It's a tool to scan your network, utilize internet protocols, and use some custom made scripts")
print("As of now, there are five executable commands.")

print("\nicmp.py | It enhances a normal ping command into a way to send more packets than default, add delays to packet sending, and also retrieve geolocation info from the host.")
print("\033[1;32mUsage: python icmp.py <host> [packet_count] [delay_between_packets] [geo] [spoof]\033[0m")
print("spoof: IP address string or 'true' to spoof random IPs each packet")

print("\nipgeo.py | This script is a way to retrieve geolocation information from an ip address or domain. It uses a public provider and is totally allowed. It provides info such as the ISP, which region it's in, etc. Use it only for ethical purposes and don't do dangerous things.")
print("\033[1;32mUsage: python ipgeo.py <ip>\033[0m")

print("\nportscanner.py | This script is essentially an amplified network checker. It scans for ports and checks which ones are open or closed. You can use this to check your own network by inputting localhost as the host argument. Use it ethically.")
print("\033[1;32mUsage: python portscanner.py <host> <port(s)> [json|csv]\033[0m")
print("\033[1;31mOnly use this with permission from your network admin\033[0m")

print("\nspeed.py | This script is a speed checker for your own use on the command line. It tests your download and upload speed and also your latency.")
print("\033[1;32mUsage: python speed.py\033[0m")

print("\ndnslookup.py | This script is a way to look up DNS (Domain Name System) records for a domain or ip address. It retrieves A, AAAA, CNAME, MX, TXT, NS, SOA, and SRV records for domains and PTR records for ip addresses.")
print("\033[1;32mUsage: python dnslookup.py <domain or ip> [uncommon_records|default:false]\033[0m")

print("\nwhoislookup.py | This script is a way to retrieve WHOIS information about a domain name. It includes data such as when it was registered, who registered it, etc.")
print("\033[1;32mUsage: python whoislookup.py <domain>\033[0m")

print("\nwebserver.py | This script is a way to emit a simple web server that shows text entered by the terminal. You can choose any port to emit the server on.")
print("\033[1;32mUsage: python webserver.py <port|default:80> <text_to_show|default:Hello>\033[0m")

print("\npullhttpheaders.py | This script is a tool to pull HTTP headers from a provided url argument.")
print("\033[1;32mUsage: python pullhttpheaders.py <url>\033[0m")

print("\narpscan.py | This script is a tool to see all local devices on your subnet")
print("\033[1;32mUsage: python arpscan.py\033[0m")

print("\nsniffer.py | This script is a network-level packet sniffer. You can see inbound and outbound requests for several protocols such as TCP, UDP, DNS, ICMP.")
print("\033[1;32mUsage: python sniffer.py\033[0m")
print("\033[1;31mOnly use this with permission from your network admin\033[0m")

print("\n\033[1;32mMade by solo on Github\033[0m")
print("https://github.com/s0lotime/pyscanner")