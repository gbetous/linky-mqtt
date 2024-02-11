#!/usr/bin/env python2

from teleinfo import Parser
from teleinfo.hw_vendors import UTInfo2
from time import sleep
import paho.mqtt.client as mqtt

MQTT_TOPIC="linky"
MQTT_HOST="mqtt.local.launageek.fr"
MQTT_PORT=1883

mqttc = mqtt.Client()
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)

while True:
  ti = Parser(UTInfo2(port="/dev/ttyUSB1"))

  # Typical frame in BASE :
  # {'IINST': '007', 'MOTDETAT': '000000', 'OPTARIF': 'BASE', 'ADCO': '031861449339', 'ISOUSC': '30', 'BASE': '034868815', 'IMAX': '090', 'PTEC': 'TH..', 'PAPP': '01590', 'HHPHC': 'A'}
  # Typical frame in TEMPO :
  # {'IINST': '004', 'MOTDETAT': '000000', 'OPTARIF': 'BBR(', 'DEMAIN': '----', 'ADCO': '031861449339', 'BBRHCJR': '000000000', 'ISOUSC': '45', 'BBRHPJB': '000000549', 'BBRHCJW': '000000000', 'PAPP': '00860', 'IMAX': '090', 'BBRHPJW': '000000000', 'BBRHCJB': '042684646', 'PTEC': 'HPJB', 'BBRHPJR': '000000000', 'HHPHC': 'A'}
  frame = ti.get_frame()
  print(frame)

  if 'BASE' in frame:
    base = frame['BASE']
    base = int(base)/1000.0
    print(base)
    mqttc.publish(MQTT_TOPIC+"/cpt", base, retain=True)

  # BLEU
  if 'BBRHCJB' in frame:
    base = frame['BBRHCJB']
    base = int(base)/1000.0
    print(base)
    mqttc.publish(MQTT_TOPIC+"/hcjb", base, retain=True)
  if 'BBRHPJB' in frame:
    val = frame['BBRHPJB']
    val = int(val)/1000.0
    print(val)
    mqttc.publish(MQTT_TOPIC+"/hpjb", val, retain=True)

  # BLANC
  if 'BBRHCJW' in frame:
    base = frame['BBRHCJW']
    base = int(base)/1000.0
    print(base)
    mqttc.publish(MQTT_TOPIC+"/hcjw", base, retain=True)
  if 'BBRHPJW' in frame:
    val = frame['BBRHPJW']
    val = int(val)/1000.0
    print(val)
    mqttc.publish(MQTT_TOPIC+"/hpjw", val, retain=True)

  # ROUGE
  if 'BBRHCJR' in frame:
    base = frame['BBRHCJR']
    base = int(base)/1000.0
    print(base)
    mqttc.publish(MQTT_TOPIC+"/hcjr", base, retain=True)
  if 'BBRHPJR' in frame:
    val = frame['BBRHPJR']
    val = int(val)/1000.0
    print(val)
    mqttc.publish(MQTT_TOPIC+"/hpjr", val, retain=True)

  if 'PAPP' in frame:
    papp = int(frame['PAPP'])
    print(papp)
    mqttc.publish(MQTT_TOPIC+"/papp", papp)

  # TARIF en cours
  if 'PTEC' in frame:
    val = frame['PTEC']
    print(val)
    mqttc.publish(MQTT_TOPIC+"/ptec", val)


  # Couleur de demain
  if 'PTEC' in frame:
    val = frame['DEMAIN']
    print(val)
    mqttc.publish(MQTT_TOPIC+"/demain", val)


  sleep(5)
