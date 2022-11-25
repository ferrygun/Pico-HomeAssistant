import netman
import time
from umqttsimple import MQTTClient
from time import sleep
from machine import Pin, PWM
import utime

country = 'SG'
ssid = 'YOUR_SSID'
password = 'YOUR_PWD'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = 'HOMEASSISTANT_IP_ADDRESS'
client_id = 'PicoW'
user_t = 'MQTT_USERID'
password_t = 'MQTT_PASSWORD'
topic_pub = 'hello'

last_message = 0
message_interval = 5
counter = 0

MID = 1500000
MIN = 1000000
MAX = 2000000

led = Pin(25,Pin.OUT)
pwm = PWM(Pin(15))

pwm.freq(50)
pwm.duty_ns(MID)

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def callback(topic, msg): 
    print((topic, msg))
    msg = msg.decode('UTF-8')
    if msg == 'on':
        pwm.duty_ns(MIN)
        utime.sleep(1)
        pwm.duty_ns(MID)
    if msg == 'off':
        pwm.duty_ns(MAX)
        utime.sleep(1)
        pwm.duty_ns(MID)
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.set_callback(callback)
    client.subscribe(topic_pub)
    time.sleep(1)


