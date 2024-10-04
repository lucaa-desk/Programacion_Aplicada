import wifi
import socketpool
import pwmio
import board
import analogio
import time

ssid = 'Shi'
password = 'arbr4619'

wifi.radio.connect(ssid, password)
print('Conectado a Wi-Fi')
print('Dirección IP:', wifi.radio.ipv4_address)

servo_Principal = pwmio.PWMOut(board.GP14, frequency=50, duty_cycle=0)
servo_Secundario = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

joystick_X = analogio.AnalogIn(board.A0)
joystick_Y = analogio.AnalogIn(board.A1)

def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)

def update_servos_from_joystick():

    value_X = joystick_X.value
    value_Y = joystick_Y.value

    mapped_value_Principal = map_range(value_X, 0, 65535, 1500, 8000)
    mapped_value_Secundario = map_range(value_Y, 0, 65535, 1000, 4000)

    servo_Principal.duty_cycle = mapped_value_Principal
    servo_Secundario.duty_cycle = mapped_value_Secundario

while True:
    update_servos_from_joystick()
    time.sleep(0.1)
