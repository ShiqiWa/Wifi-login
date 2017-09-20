#-*- coding:utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
import sqlite3
conn = sqlite3.connect('test.db')
c = conn.cursor()

class LoginHandler(BaseHTTPRequestHandler):
	def do_OPTIONS(self):           
		self.send_response(200, "ok")       
		self.send_header('Access-Control-Allow-Origin', '*')                
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", 'Content-Type')
# 接受POST请求，获取用户名和密码，然后查数据库，看是否有效
	def do_POST(self):
		print "in"
		# 获取用户名和密码
		content_type = cgi.parse_header(self.headers['content-type'])[0]
		print content_type;
		if content_type == "application/json":
			length = int(self.headers['content-length'])
			post_values = json.loads(self.rfile.read(length))
			print post_values['username'], post_values['password']
			username = "'" + post_values['username'] + "'"
			password = "'" + post_values['password'] + "'"	
			cursor = c.execute("SELECT password  from USER where username=" + "'" + post_values['username'] + "'")
			for row in cursor:
			   print row[0]
			   print row[0] == post_values['password']
			print self.headers



if __name__ == '__main__':
	try:
		c.execute('''CREATE TABLE USER
		       (ID	INT	PRIMARY KEY 	NOT NULL,
		       USERNAME	TEXT	NOT NULL,
		       PASSWORD	TEXT	NOT NULL
		       );''')

		print "Table created successfully";

		c.execute("INSERT INTO USER (ID, USERNAME,PASSWORD) VALUES (1, 'wat', '123')");
		c.execute("INSERT INTO USER (ID, USERNAME,PASSWORD) VALUES (2, 'wsq', '456')");
		c.execute("INSERT INTO USER (ID, USERNAME,PASSWORD) VALUES (3, 'wxf', '789')");
		conn.commit();

		print "Insert successfully";
	except:
		print "table already exist"	

	# Start a simple server, and loop forever
	server = HTTPServer(('localhost', 8888), LoginHandler)
	print("Starting server, use <Ctrl-C> to stop")
	server.serve_forever()