from socketserver import ThreadingTCPServer
from messenger_server.request_handler import RequestHandler
from messenger_server.database import DatabaseConnection

""" Main application """
ADDRESS = "127.0.0.1"
PORT = 54321

if __name__ == "__main__":
    with ThreadingTCPServer((ADDRESS, PORT), RequestHandler) as server:
        DatabaseConnection().setup()
        try:
            server.serve_forever()
        except:
            server.shutdown()
