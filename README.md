# PyScanner

**PyScanner** is a fast and easy-to-use CLI tool for scanning network ports and properties using Python

It supports:

- ✅ Scanning common or specific ports
- ✅ Exporting results to **JSON** or **CSV**
- 🚧 ICMP pings, UDP and advanced TCP scanning *(coming soon)*
- ⚙️ Entirely command-line based and cross-platform

## ❓ Things to know
- This tool requires Python to be installed (https://www.python.org/)
- You need to extract the ZIP file of this repository and then set your current directory to it in your device's terminal.
- Then execute pip install -r requirements.txt to load all needed modules.
- Then you can start executing PyScanner commands.
- Here's the full list of internet ports (https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)

---

## 🔧 Port Scanner Usage

```bash
python portscanner.js <host/ip> <ports> <output>
<host/ip> — The hostname or IP address to scan (e.g. localhost, 192.168.1.1)
<ports> - Accepts comma separated and ranges (e.g. 25,80,443, 25-443)
<output> (optional) (e.g. csv, json, or leave blank to just console log)
