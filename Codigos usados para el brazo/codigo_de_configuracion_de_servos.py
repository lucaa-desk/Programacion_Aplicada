import board
import analogio
import pwmio
import time

potentiometer = analogio.AnalogIn(board.GP26)
servo_Principal = pwmio.PWMOut(board.GP14, frequency=50, duty_cycle=0)
servo_Secundario = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    pot_value = potentiometer.value
    mapped_value_Principal = map_range(pot_value, 0, 65535, 1500, 8000)
    mapped_value_Secundario = map_range(pot_value, 0, 65535, 1500, 8000)

    servo_Principal.duty_cycle = int(mapped_value_Principal)
    servo_Secundario.duty_cycle = int(mapped_value_Secundario)
    
    time.sleep(0.01)
