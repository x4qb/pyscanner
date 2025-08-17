import socket
import threading
import sys

def get_local_ipv4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def handle_client(client_socket, header_text):
    try:
        request = client_socket.recv(1024).decode()
        print(f"Client connected from:\n{request}")

        http_response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<html>
<head><title>{header_text}</title></head>
<body>
<h1>{header_text}</h1>
</body>
</html>
"""
        client_socket.sendall(http_response.encode())
    except Exception as e:
        print(f"Client handling error: {e}")
    finally:
        client_socket.close()

def run_server(port, header_text):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Serving a HTTP server on 0.0.0.0:{port}")
    print(f"You can show other people on the network by giving them the link: http://{get_local_ipv4()}:{port}")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"{addr} connected")
            thread = threading.Thread(target=handle_client, args=(client_socket, header_text))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\nTerminating emitted web server.")
    finally:
        server.close()

if __name__ == "__main__":
    port = 80
    header_text = "Hello"
    print("\033[1;32mUsage: python webserver.py <port|default:80> <text_to_show|default:Hello>\033[0m")

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}, using default {port}")
    if len(sys.argv) > 2:
        header_text = ' '.join(sys.argv[2:])

    run_server(port, header_text)
