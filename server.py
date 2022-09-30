#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        get_data = self.data.decode('utf-8')

        #get command
        command = get_data.split(' ')[0]
        
        #if command is POST, PUT, or DELETE --> 405 error
        if ((command == "POST") or (command == "PUT") or (command == "DELETE")):
             self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed", 'utf-8'))
             return 0
        
        #make sure command is GET
        elif command == "GET":
            #get URI
            uri = get_data.split(' ')[1]
            #css and html not is uri
            if (("css" not in uri) and ("html" not in uri)):
                #last character in uri is /
                if uri[-1] == "/":
                    uri += "index.html"
                else:
                    #301 error
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:" + uri +'/' +"\r\n\r\n301 Moved Permanently",'utf-8'))
                    return 0

            destination = "./www" + uri
            html_desc = "text/html"
            css_desc = "text/css"

            if ".css" in uri:
                print(".css IN URI")
                #check if destination exists
                if os.path.exists(destination):
                    #open to read
                    f = open(destination, 'r')
                    file_contents = f.read()
                    #OK 200 response
                    self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" + css_desc +"\r\n"  +"\r\n\r\n"+file_contents,'utf-8'))
                    return 0
                #404 error
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n404 Not Found",'utf-8'))
                    return 0
            
            if ".html" in uri:
                #check if destination exists
                if os.path.exists(destination):
                    #open to read
                    f = open(destination, 'r')
                    file_contents = f.read()
                    #OK 200 response
                    self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" + html_desc +"\r\n"  +"\r\n\r\n"+file_contents,'utf-8'))
                    return 0
                #404 error
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n404 Not Found",'utf-8'))
                    return 0

        #self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
