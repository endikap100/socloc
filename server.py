import SocketServer
import mysql.connector
from BaseHTTPServer import BaseHTTPRequestHandler
import codecs
from os import curdir, sep


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin")
        self.end_headers()
    def do_GET(self):
        if self.path == '/' or self.path == '':
            cnx = mysql.connector.connect(user='root', password='soclocapi',host='127.0.0.1',database='socloc')
            cursor = cnx.cursor()
            query = ("SELECT hashtag,location FROM location")
            cursor.execute(query)
            response = {}
            hasht = []
            for (hashtag,location) in cursor:
                if str(hashtag) in hasht:
                    response[str(hashtag)].append(str(location))
                else:
                    response[str(hashtag)] = [str(location)]
                    hasht.append(str(hashtag))

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write((str(response)).replace("'",'"'));
            self.wfile.close()
        else:
            try:
                sendReply = False
                if self.path.endswith(".html"):
                    self.path="/error.html"
                    mimetype='text/html'
                    sendReply = True
                if self.path.endswith(".jpg"):
                    mimetype='image/jpg'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype='image/gif'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype='application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype='text/css'
                    sendReply = True

                if sendReply == True:
                    f = open(curdir + sep + self.path)
                    self.send_response(200)
                    self.send_header('Content-type',mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()

            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)


httpd = SocketServer.TCPServer(("", 9000), MyHandler)
httpd.serve_forever()

