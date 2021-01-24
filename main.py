import machine
from machine import Pin
from time import sleep
import socket
import network
import time

host = 'xxx.xxx.xxx.xxx'
port = 10000
SSID = "xxxxxxxxxx"
PASSWORD = "xxxxxxxxxxx"
wlan = None
s = None
check_ld_prg = Pin(5, Pin.IN, Pin.PULL_UP)


def connectwifi(ssid, passwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid, passwd)
    while wlan.ifconfig()[0] == '0.0.0.0':
        time.sleep(1)
    return True


def deep_sleep(msecs):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    rtc.alarm(rtc.ALARM0, msecs)
    # put the device to sleep
    machine.deepsleep()


try:
    if connectwifi(SSID, PASSWORD):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip = wlan.ifconfig()[0]
        print(ip + "<-this is device ID")
        res = s.sendto(b'hello this is esp8266 wake up\r\n', (host, port))
except:
    if s:
        s.close()
    wlan.disconnect()
    wlan.active(False)

sleep(1)
if not check_ld_prg.value():
    while True:
        print("please upload script")
        sleep(1)

# sleep for 10 seconds (10000 milliseconds)
deep_sleep(20 * 60 * 1000)
