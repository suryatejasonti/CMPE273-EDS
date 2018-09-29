import paho.mqtt.client as mqtt #import the client1

#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("P1") #create new instance
client.connect('iot.eclipse.org', 1883, 60) #connect to broker
client.publish("sjsu-cmpe273/quizz1","Hi from william")#publish