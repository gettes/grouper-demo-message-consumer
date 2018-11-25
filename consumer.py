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
		for event in pj['esbEvent'] :
			eventType = str ( event['eventType'] )
			groupName = ""; other = ""
			seq = event['sequenceNumber']
			crTime = ( event['createdOnMicros'] / 1000 ) / 1000
			timenow = time.time(); diff = int(timenow - crTime)
			print("%s-%s: transit=%s " % ( time.strftime('%Y/%m/%d-%H:%M:%S', time.localtime()), time.strftime('%Y/%m/%d-%H:%M:%S', time.localtime(crTime)), time.strftime('%H:%M:%S', time.gmtime(diff)) ), end='' )
			if eventType.startswith('MEMBERSHIP_') : groupName = event['groupName']
			if eventType.startswith('PRIVILEGE_') : 
				groupName = event['ownerName']
				other = event['privilegeName']
			if eventType.startswith('GROUP_') : groupName = event['name']
			if len(groupName) > 0 :
				createdOnMicros = event["createdOnMicros"]
				if eventType.startswith('MEMBERSHIP_') or eventType.startswith('PRIVILEGE_') : 
					subjectId = event['subjectId']
					print("%s: %s: %s: %s - %s %s" % (q, seq, eventType, groupName, subjectId, other) )
					if subjectId.startswith('whcurry@ufl.edu') : print("%s = %s" % ( q, json.dumps(pj, indent=4) ) )
				else: print("%s: %s: %s: %s" % (q, seq, eventType, groupName) )
			else: print("%s = %s" % (q, json.dumps(pj) ) ) # , sort_keys=True, indent=4)
def q0(ch, method, properties, body):
	displayQ("** Grouper", body);
	ch.basic_ack(delivery_tag = method.delivery_tag)
def q2(ch, method, properties, body):
	displayQ("** G2", body);
	ch.basic_ack(delivery_tag = method.delivery_tag)
def q3(ch, method, properties, body):
	displayQ("** G3", body);
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
	print(' [*] Ready Player One...')
	channel.start_consuming()
except KeyboardInterrupt:
	connection.close()
	print ("keyboard ouch.")
except Exception as e:
	if connection != 0 : connection.close()
	print ("\n", e, "\nouch.")
	sys.exit(1)
