# nodescanner
nodescanner is an fast and easy-to-use tool to scan a network and it's properties.

You can scan common or specific ports then export to JSON or CSV.
You can do ICMP pings, UDP and TCP scans. (coming soon)
It's entirely a CLI tool for NodeJS.

Port scanner usage:
node portscanner.js <host/ip> <ports (can be comma separated like 80,443 or ranged 80-443)> <output (csv, json, or leave blank for just a console log)>
Examples: 
node portscanner.js localhost 80,443
node portscanner.js localhost 80-443
node portscanner.js localhost 25-80 csv
node portscanner.js localhost 25,80,2015,135 json

Setup:
First have NodeJS,
Download the ZIP folder,
Extract it,
Go to the main folder and get it's file location,
Go to your device's terminal,
Execute this command: cd C:\Users\Example\Downloads\nodescanner,
Then execute whatever command you want to, usage help is stated.

List of ports (https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)
Requires NodeJS to use. Easy setup (https://nodejs.org)

# Be ethical 🔒
