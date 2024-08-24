import socketpool
import wifi
import board
import pwmio

# Configurar el LED en el pin GP16 usando PWM
led = pwmio.PWMOut(board.GP16, frequency=5000, duty_cycle=0)

# Conexión Wi-Fi
wifi.radio.connect("Ejemplo", "12345678")
pool = socketpool.SocketPool(wifi.radio)

s = pool.socket()
s.bind(('', 80))
s.listen(5)

estado_led = "Apagado"

def get_html():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Control de LED</title>
    </head>
    <body>
        <h1>Control del LED</h1>
        <a href="/?led=1"><button>Encender LED</button></a>
        <br><br>
        <a href="/?led=0"><button>Apagar LED</button></a>
        <p>Estado del LED: {}</p>
    </body>
    </html>
    """.format(estado_led)  
    return html
while True:
    conn, addr = s.accept()
    buffer = bytearray(1024)
    bytes_received, address = conn.recvfrom_into(buffer)
    request = buffer[:bytes_received].decode('utf-8')
    
    if '/?led=1' in request:
        led.duty_cycle = 65535  # Encender LED (PWM a máximo)
        estado_led = "Encendido"
    elif '/?led=0' in request:
        led.duty_cycle = 0  # Apagar LED (PWM a 0)
        estado_led = "Apagado"

    response = get_html()
    conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    conn.send(response)
    conn.close()
