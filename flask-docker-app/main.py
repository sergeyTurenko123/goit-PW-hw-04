from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import socket
from datetime import datetime
import json
from multiprocessing import Process

class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = ("127.0.0.1", 6000)
        sock.sendto(json.dumps(data_dict).encode("utf-8"), server)
        sock.close()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    

def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()



def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            # data_dict = {f"{datetime.now()}": json.loads(data)}
            with open("./storage/data.json", "r", encoding="utf-8") as f:
                dict = json.load(f)
            dict[f"{datetime.now()}"]= json.loads(data)
            with open("./storage/data.json", "w", encoding="utf-8") as f:
               json.dump(dict, f, indent = 4)
    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


if __name__ == '__main__':

    
    
    HTTP = Process(target=run)
    Socket = Process(target=run_server, args=("127.0.0.1", 6000), daemon=True)
    
    Socket.start()
    HTTP.start()
    
    # Socket_client.start()
    
    HTTP.join()
    Socket.join()
    # Socket_client.join()
    