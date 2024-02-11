#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = "Jordan Martin"
# __licence__ = "Apache License 2.0"

import serial
import logging
import subprocess
import requests
import paho.mqtt.client as mqtt

MQTT_TOPIC="linky"
MQTT_HOST="mqtt.local.launageek.fr"
MQTT_PORT=1883

mqttc = mqtt.Client()
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Port serial
stty_port = '/dev/ttyUSB1'

def main():

    logging.info('Starting...')

    # Reconfigure le port serial pour eviter
    # l'erreur: termios.error: (22, 'Invalid argument')
    logging.info('Reconfigure stty %s' % stty_port)
    subprocess.call(['stty', '-F',  stty_port, 'iexten'])

    with serial.Serial(port=stty_port, baudrate=9600, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.SEVENBITS, timeout=1) as ser:

        logging.info('Reading on %s' % stty_port)

        while True:
            line = ser.readline()
            arr = line.decode('ascii').split('\t')
            
            if len(arr) != 3:
                continue

            if not verify_checksum(arr):
                continue

            publish(arr)

#EASF01 HC bleu
#EASF02 HP bleu
#EASF03 HC blanc
#EASF04 HP blanc
#EASF05 HC rouge
#EASF06 HP rouge

def publish(arr):
    if arr[0] == 'SINSTS':
        mqttc.publish(MQTT_TOPIC+"/papp", arr[1], retain=False)
    elif arr[0] == 'STGE':
        mqttc.publish(MQTT_TOPIC+"/stge", arr[1], retain=True)
    elif arr[0] == 'ASDC':
        mqttc.publish(MQTT_TOPIC+"/asdc", arr[1], retain=True)
    elif arr[0] == 'LTARF':
        mqttc.publish(MQTT_TOPIC+"/ltarf", strip(arr[1]), retain=False)
    elif arr[0] == 'EASF01':
        mqttc.publish(MQTT_TOPIC+"/hcjb", int(arr[1]), retain=True)
    elif arr[0] == 'EASF02':
        mqttc.publish(MQTT_TOPIC+"/hpjb", int(arr[1]), retain=True)
    elif arr[0] == 'EASF03':
        mqttc.publish(MQTT_TOPIC+"/hcjw", int(arr[1]), retain=True)
    elif arr[0] == 'EASF04':
        mqttc.publish(MQTT_TOPIC+"/hpjw", int(arr[1]), retain=True)
    elif arr[0] == 'EASF05':
        mqttc.publish(MQTT_TOPIC+"/hcjr", int(arr[1]), retain=True)
    elif arr[0] == 'EASF06':
        mqttc.publish(MQTT_TOPIC+"/hpjr", int(arr[1]), retain=True)
    elif arr[0] == 'URMS1':
        mqttc.publish(MQTT_TOPIC+"/urms1", int(arr[1]), retain=True)
    elif arr[0] == 'SINSTI':
        mqttc.publish(MQTT_TOPIC+"/sinsti", int(arr[1]), retain=True)
    elif arr[0] == 'EAIT':
        mqttc.publish(MQTT_TOPIC+"/eait", int(arr[1]), retain=True)
    elif arr[0] == 'SMAXIN':
        mqttc.publish(MQTT_TOPIC+"/smaxin", int(arr[1]), retain=True)
    elif arr[0] == 'SMAXIN-1':
        mqttc.publish(MQTT_TOPIC+"/smaxin-1", int(arr[1]), retain=True)
    else:
        print(arr)

def verify_checksum(arr):
    tag = arr[0]
    data = arr[1]
    checksum = arr[2].replace('\r\n', '')
    checked_data = [ord(c) for c in (tag + '\t' + data + '\t')]
    computed_sum = (sum(checked_data) & 0x3F) + 0x20
    return checksum == chr(computed_sum)

if __name__ == '__main__':
    main()

