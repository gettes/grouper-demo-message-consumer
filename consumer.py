#!/usr/local/bin/python3.7
import pika
import time
import json
import sys

parameters = pika.URLParameters('amqp://readerG2:readerG2@rabbitmq:5672/%2F')

def displayQ(q, body):
	try:
		pj = json.loads(body)
	except:
		print ("Unexpected error: ", sys.exc_info()[0], "\n", body)
	else:
		eventType = str ( pj['esbEvent'][0]['eventType'] )
		groupName = ""
		other = ""
		seq = pj['esbEvent'][0]['sequenceNumber']
		if eventType.startswith('MEMBERSHIP_') : groupName = pj['esbEvent'][0]['groupName']
		if eventType.startswith('PRIVILEGE_') : 
			groupName = pj['esbEvent'][0]['ownerName']
			other = pj['esbEvent'][0]['privilegeName']
		if eventType.startswith('GROUP_') : groupName = pj['esbEvent'][0]['name']
		if len(groupName) > 0 :
			createdOnMicros = pj["esbEvent"][0]["createdOnMicros"]
			if eventType.startswith('MEMBERSHIP_') or eventType.startswith('PRIVILEGE_') : 
				subjectId = pj['esbEvent'][0]['subjectId']
				print(" %s: %s %s: %s - %s %s" % (q, seq, eventType, groupName, subjectId, other) )
				if subjectId.startswith('whcurry@ufl.edu') : print(" %s = %s" % ( q, json.dumps(pj, indent=4) ) )
			else: print(" %s: %s: %s: %s" % (q, seq, eventType, groupName) )
		else: print(" %s = %s" % (q, json.dumps(pj) ) ) # , sort_keys=True, indent=4)
def q0(ch, method, properties, body):
	displayQ(" ** Grouper", body);
	ch.basic_ack(delivery_tag = method.delivery_tag)
def q2(ch, method, properties, body):
	displayQ(" ** q1", body);
	ch.basic_ack(delivery_tag = method.delivery_tag)
def q3(ch, method, properties, body):
	displayQ(" ** q2", body);
	ch.basic_ack(delivery_tag = method.delivery_tag)
def connectmq(parameters):
	global connection, channel
	while True:
		try:
			connection = pika.BlockingConnection(parameters)
		except:
			print("unable to connect to rabbitmq: ", sys.exc_info()[0])
			time.sleep(5)
		else:
			channel = connection.channel()
			channel.basic_consume(q0, queue='Grouper', no_ack=False)
			channel.basic_consume(q2, queue='G2', no_ack=False)
			channel.basic_consume(q3, queue='G3', no_ack=False)
			break

try:
	connectmq(parameters)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()
except KeyboardInterrupt:
	connection.close()
	print ("keyboard ouch.")
except:
	print ("ouch.", sys.exc_info()[0])
