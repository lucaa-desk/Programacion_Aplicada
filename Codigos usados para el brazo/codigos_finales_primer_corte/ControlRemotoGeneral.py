import wifi
import socketpool
import pwmio
import board
import re

# Conectar a Wi-Fi
ssid = 'Shi'
password = 'arbr4619'

wifi.radio.connect(ssid, password)
print('Conectado a Wi-Fi')
print('Dirección IP:', wifi.radio.ipv4_address)

# Configurar los servos usando PWM
servo_Principal = pwmio.PWMOut(board.GP14, frequency=50, duty_cycle=0)
servo_Secundario = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

# Función para mapear valores del slider
def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)

# Página HTML para los sliders de los servos (usando triple comillas para facilitar la legibilidad)
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Servo-Brazo</title>
    <style>
        body{font-family:Arial,sans-serif;background-color:#8B4513;margin:0;padding:0;display:flex;justify-content:center;align-items:center;flex-direction:column;height:100vh}
        .control-panel{background-color:white;padding:10px;border-radius:10px;text-align:center;width:200px}
        h1{font-size:20px;margin-bottom:10px;color:#333}
        p{font-size:14px;margin-bottom:10px;color:#555}
        input[type=range]{width:100%;margin-bottom:10px;height:5px;background:#ddd;outline:none;opacity:.8;transition:opacity .2s}
        input[type=range]:hover{opacity:1}
        input[type=range]::-webkit-slider-thumb{width:10px;height:10px;background:#007bff;border-radius:50%;cursor:pointer}
        #canvas-container{width:100%;height:300px}
    </style>
</head>
<body>
    <div class="control-panel">
        <h1>Servo-Brazo</h1>
        <p>Servo Principal:</p>
        <input type="range" id="slider1" min="0" max="100" value="50" step="1" oninput="updateServos()">
        <p>Servo Secundario:</p>
        <input type="range" id="slider2" min="0" max="100" value="50" step="1" oninput="updateServos()">
    </div>
    <div id="canvas-container"></div>
    <script>
        function updateServos() {
            let value1 = document.getElementById('slider1').value;
            let value2 = document.getElementById('slider2').value;
            fetch(/update_servos?value1=${value1}&value2=${value2})
                .then(response => response.text())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

# Función para manejar las solicitudes y enviar el HTML en fragmentos
def handle_request(client, chunk_size=1024):
    buffer = bytearray(1024)
    bytes_received = client.recv_into(buffer)
    request_str = buffer[:bytes_received].decode('utf-8')

    # Si la solicitud es para actualizar los servos
    if 'GET /update_servos' in request_str:
        match = re.search(r'GET /update_servos\?value1=([0-9]+)&value2=([0-9]+)', request_str)
        if match:
            value1 = int(match.group(1))
            value2 = int(match.group(2))

            # Mapeamos los valores de los sliders para los servos
            mapped_value_Principal = map_range(value1, 0, 100, 1500, 8000)
            mapped_value_Secundario = map_range(value2, 0, 100, 1500, 4000)

            servo_Principal.duty_cycle = mapped_value_Principal
            servo_Secundario.duty_cycle = mapped_value_Secundario

        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/plain\r\n")
        client.send("Connection: close\r\n\r\n")
        client.send("OK")
    else:
        # Sirviendo el archivo HTML en fragmentos (chunks) de 1024 bytes
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/html\r\n")
        client.send("Connection: close\r\n\r\n")
        for i in range(0, len(html), chunk_size):
            client.send(html[i:i + chunk_size])

    client.close()

# Iniciar el servidor
def start_server():
    pool = socketpool.SocketPool(wifi.radio)
    server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(1)

    print('Servidor escuchando en 0.0.0.0:80')

    while True:
        client, addr = server_socket.accept()
        print('Cliente conectado desde', addr)
        handle_request(client)

# Iniciar el servidor web
start_server()