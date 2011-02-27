#! /usr/bin/env python
# encoding=UTF-8
import xmpp
import sys
class  gtalk:
	def __init__(self):
		pass
	def send_to_gtalk(self,message):
		userID   = 'wliment.bak@gmail.com' 
		password = 'ZHENGTAO5655327'
		ressource = 'Script'

		jid  = xmpp.protocol.JID(userID)
		jabber     = xmpp.Client(jid.getDomain(), debug=[])

		connection = jabber.connect(('talk.google.com',5222))
		if not connection:
		    sys.stderr.write('Could not connect\n')
		else:
		    sys.stderr.write('Connected with %s\n' % connection)

		auth = jabber.auth(jid.getNode(), password, ressource)
		if not auth:
		    sys.stderr.write("Could not authenticate\n")
		else:
		    sys.stderr.write('Authenticate using %s\n' % auth)

		jabber.sendInitPresence(requestRoster=1)
		jabber.send(xmpp.Message( "wliment@gmail.com" ,message))
		jabber.disconnect()

