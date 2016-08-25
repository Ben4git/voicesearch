from flask import Flask
#from app import app
import socket

app = Flask(__name__)
ipaddress = socket.gethostbyname(socket.gethostname())

@app.route( '/' )
def iPv4():
	#return ('Welcome to the Wetterfrosch search! '
	#+ ' Your local IP address is: ' + ipaddress)
	return '''
<html>
  <head>
    <title>Home Page</title>
  </head>
  <body>
    <h1>Hello, ''' + ipaddress + '''</h1>
  </body>
</html>
'''
