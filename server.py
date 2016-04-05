import SocketServer
import mysql.connector
from BaseHTTPServer import BaseHTTPRequestHandler

def some_function():
	pass
   	#print "some_function got called"

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        #self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin")
	self.end_headers()
    def do_GET(self):
        #cnx = mysql.connector.connect(user='root', database='socloc',password='socloc',
	cnx = mysql.connector.connect(user='root', password='soclocapi',
                              host='127.0.0.1',
                              database='socloc')
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
        #print(self.wfile)
        #self.wfile.write("<html><head><title>Title goes here.</title></head>")
        self.wfile.write((str(response)).replace("'",'"'));
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        #self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        #self.wfile.write("</body></html>")
        self.wfile.close()

httpd = SocketServer.TCPServer(("", 9000), MyHandler)
httpd.serve_forever()

