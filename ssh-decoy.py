import socketserver
import json
import urllib.request
from functools import lru_cache

MESSAGE = (
    b"================================================\r\n"
    b"          SIKE! THAT'S THE WRONG NUMBER!\r\n"
    b"================================================\r\n"
    b"\r\n"
    b"Erm, what are you doing?\r\n"
    b"Get the fuck away from my server, CLANKER! :(\r\n"
    b"\r\n"
    b"\r\n"
    b"\r\n"
    b"\r\n"
    b"Never gonna give you up\r\n"
    b"Never gonna let you down\r\n"
    b"Never gonna run around and desert you\r\n"
    b"Never gonna make you cry\r\n"
    b"Never gonna say goodbye\r\n"
    b"Never gonna tell a lie and hurt you\r\n"
)

@lru_cache(maxsize=1024)
def get_location(ip):
    try:
        url = f"https://ipwho.is/{ip}"

        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read())

        if data.get("success"):
            city = data.get("city", "Unknown")
            country = data.get("country", "Unknown")

            return f"{city}, {country}"

    except Exception:
        pass

    return "Unknown"

class SSHDecoy(socketserver.BaseRequestHandler):
    def handle(self):
        client = self.request

        ip = self.client_address[0]
        location = get_location(ip)

        try:
            client.settimeout(5)

            identification = b""

            while not identification.endswith(b"\n"):
                chunk = client.recv(1)

                if not chunk:
                    return

                identification += chunk

                if len(identification) > 255:
                    return

            if not identification.startswith(b"SSH-"):
                return

            print(
                f"[{ip}] Someone from {location} found the wrong SSH entrance!",
                flush=True
            )

            client.sendall(MESSAGE)

        except (OSError, TimeoutError):
            pass

        finally:
            client.close()


class SSHDecoyServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 22

    with SSHDecoyServer((HOST, PORT), SSHDecoy) as server:
        print(f"[*] SSH decoy listening on {HOST}:{PORT}", flush=True)
        server.serve_forever()
