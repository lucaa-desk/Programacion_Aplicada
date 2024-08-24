import socketpool
import wifi
import board
import pwmio

##luver eduardo lopez ayala ¬ 20231005155

led = pwmio.PWMOut(board.GP16, frequency=5000, duty_cycle=0)

wifi.radio.connect("Ejemplo", "12345678")
pool = socketpool.SocketPool(wifi.radio)

s = pool.socket()
s.bind(('', 80))
s.listen(5)

estado_led = "Apagado"

def get_html():
    with open('estado.html', 'r') as file:
        html = file.read()
    html = html.replace('<!--estado-->', estado_led)
    return html

while True:
    conn, addr = s.accept()
    buffer = bytearray(1024)
    bytes_received, address = conn.recvfrom_into(buffer)
    request = buffer[:bytes_received].decode('utf-8')
    
    if '/?led=1' in request:
        led.duty_cycle = 65535  ## Encender LED (PWM a máximo) el pulso maximo segun 2 a la 16 segun el profe
        estado_led = "Encendido"
    elif '/?led=0' in request:
        led.duty_cycle = 0  ## Apagar LED (PWM a 0)
        estado_led = "Apagado"

    response = get_html()
    conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    conn.send(response)
    conn.close()
