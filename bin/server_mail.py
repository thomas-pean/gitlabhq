import time
import BaseHTTPServer
import json
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST_NAME = "localhost"
PORT_NUMBER = 9000
MAIL_TO = "gitserver@jouve.fr"
MAIL_FROM = "gitserver@jouve.fr"

class JsonHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_POST(s):
		content_len = int(s.headers.getheader('content-length', 0))
		post_body = s.rfile.read(content_len)
		error_code = 200
		try:
			event = json.loads(post_body)
			print time.asctime(), "event: %s" % (event["event_name"])
			if event["event_name"] == "project_create" :
				msg = MIMEMultipart('alternative')
				msg["Subject"] = "[GitLab] New project created"
				msg["From"] = MAIL_FROM
				msg["To"] = MAIL_TO
				
				project_name = event["name"]
				owner_name = event["owner_name"] 
				owner_email = event["owner_email"]
				created_at = event["created_at"] if "created_at" in event else ""
				project_visibility = event["project_visibility"] if "project_visibility" in event else ""
				namespace = event["path_with_namespace"] if "path_with_namespace" in event else ""

				message = """
The project <b>"%s"</b> have been created by <b>%s</b> (%s) at %s<br />
Visibility : %s<br />
Namespace : %s
				""" % (project_name, owner_name, owner_email, created_at, project_visibility, namespace)

				data = MIMEText(message, 'html')
				msg.attach(data)
				try:
					smtpServer = smtplib.SMTP("localhost")
					#smtpServer.set_debuglevel(True)
					smtpServer.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
					print time.asctime(), "Sending mail to admin ... (%s)" % (event["name"])
				except Exception, e:
					print "Error sending email. %s" % e
		except ValueError:
			print time.asctime(), "Error parsing JSON."
			error_code = 500

		"""Respond to a POST request."""
		s.send_response(error_code)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write("<html></html>")

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), JsonHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
