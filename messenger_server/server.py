from socketserver import ThreadingTCPServer
from request_handler import RequestHandler

""" Main application """
ADDRESS = "127.0.0.1"
PORT = 54321

if __name__ == "__main__":
    server = ThreadingTCPServer((ADDRESS, PORT), RequestHandler)
    server.serve_forever()
