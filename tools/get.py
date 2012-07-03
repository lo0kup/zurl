import sys
import uuid
import tnetstring
import zmq

if len(sys.argv) < 2:
	print "usage: %s [url]" % sys.argv[0]
	sys.exit(1)

ctx = zmq.Context()
sock = ctx.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5552")

req = dict()
req["id"] = str(uuid.uuid4())
req["method"] = "GET"
req["url"] = sys.argv[1]
sock.send(tnetstring.dumps(req))

resp = tnetstring.loads(sock.recv())
if "error" in resp:
	print "error: %s" % resp["condition"]
	sys.exit(1)

print "code=%d status=[%s]" % (resp["code"], resp["status"])
for h in resp["headers"]:
	print h

print "\n%s" % resp["body"]