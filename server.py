def run_r(expression):

    return exec('Rscript -e ' + expression)

from http.server import BaseHTTPRequestHandler,HTTPServer

import os
import json

def getPredictions(days):
    result = []
    for i in range(days):
        result.append({ 'index': i, 'prediction': {'cloudy':0.4, 'rainy': 0.3} })
    return result

# Create custom HTTPRequestHandler class
class HTTPRequestHandler(BaseHTTPRequestHandler):
    # handle GET command
    def do_GET(self):
        rootdir = 'c:/server/'  # file location

        try:
            print(self.path)

            if 'ajax=' in self.path:
                function_call = str(self.path).replace('/ajax=','')

                prediction = eval(function_call)

                predictionJson = json.dumps(prediction)

                self.wfile.write(predictionJson.encode())
                return

            if self.path.endswith('.html'):
                f = open(rootdir + self.path)  # open requested file

                # send code 200 response
                self.send_response(200)

                # send header first
                self.send_header('Content-type', 'text-html')
                self.end_headers()

                # send file content to client
                self.wfile.write(f.read().encode())
                f.close()
                return
            else:
                f = open(rootdir + self.path, 'rb')  # open requested file

                # send code 200 response
                self.send_response(200)

                # send header first
                default_type = 'image/jpg'
            
                # specify type of file being sent
                content_type = default_type
                if '.png' in self.path: content_type = 'image/png'
                if '.ico' in self.path: content_type = 'image/ico'
                if '.js'  in self.path: content_type = 'text/javascript'

                self.send_header('Content-type', content_type)
                self.end_headers()

                # send file content to client
                self.wfile.write(f.read())
                f.close()
                return
            
        except IOError:
            self.send_error(404, 'File not found')

def run():
    print('http server is starting...')

    # ip and port of servr
    # by default http server port is 80
    server_address = ('127.0.0.1', 80)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()