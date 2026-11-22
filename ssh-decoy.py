import socketserver

MESSAGE = (
    b"================================================\r\n"
    b"          SIKE! THAT'S THE WRONG NUMBER!\r\n"
    b"================================================\r\n"
    b"\r\n"
    b"Erm, what are you doing?\r\n"
    b"Get the fuck away from my server, CLANKER! :(\r\n"
    b"As a punishment, you shall wait forever.....\r\n"
    b"\r\n"
    b"\r\n"
    b"\r\n"
    b"Never gonna give you up\r\n"
    b"Never gonna let you down\r\n"
    b"Never gonna run around and desert you\r\n"
    b"Never gonna make you cry\r\n"
    b"Never gonna tell a lie and hurt you\r\n"
)


class SSHDecoy(socketserver.BaseRequestHandler):
    def handle(self):
        client = self.request

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
                f"[{self.client_address[0]}] "
                f"Found the wrong SSH entrance!",
                flush=True
            )

            client.sendall(MESSAGE)

            # Congratulations. You are now stuck here.
            client.settimeout(None)

            while True:
                data = client.recv(1024)

                if not data:
                    break

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
