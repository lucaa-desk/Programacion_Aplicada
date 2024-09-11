import board
import pwmio
import wifi
import socketpool

# Configuración de los servos
servo_Principal = pwmio.PWMOut(board.GP14, frequency=50, duty_cycle=0)
servo_Secundario = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)

# Conectar a la red Wi-Fi
try:
    wifi.radio.connect("pad", "rasberry")
    print(f"Conectado a la Wi-Fi, IP: {wifi.radio.ipv4_address}")
except Exception as e:
    print(f"Error al conectar a la Wi-Fi: {e}")
    raise

# Configuración del servidor
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

# Obtener la dirección IP como una cadena
ip_address = str(wifi.radio.ipv4_address)

# Enlazar y escuchar en el puerto 80
server.bind((ip_address, 80))
server.listen(1)
server.settimeout(10)  # Añadido timeout para evitar bloqueos

print(f"Servidor iniciado en http://{ip_address}")

def handle_request(request):
    try:
        if '/update_servos' in request:
            params = request.split(" ")[1].split("?")[1].split("&")
            request_dict = {param.split("=")[0]: param.split("=")[1] for param in params}
            value = float(request_dict.get('value', 0))

            # Mapear el valor del slider al rango de los servos
            mapped_value_Principal = map_range(value, 0, 100, 1500, 6000)
            mapped_value_Secundario = mapped_value_Principal


            # Ajustar los servos
            servo_Principal.duty_cycle = mapped_value_Principal
            servo_Secundario.duty_cycle = mapped_value_Secundario

            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
        else:
            # Leer el archivo HTML
            try:
                with open("movimiento.html", 'r') as file:
                    response = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response}"
            except OSError:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found"
    except Exception as e:
        response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError: {str(e)}"

    return response

# Ciclo principal del servidor
while True:
    try:
        client_socket, client_address = server.accept()
        print(f"Conexión desde {client_address}")

        # Usar un buffer para leer los datos entrantes
        buffer = bytearray(1024)
        client_socket.recv_into(buffer)
        request = buffer.decode("utf-8").strip()

        # Procesar la solicitud
        response = handle_request(request)

        # Enviar la respuesta
        client_socket.send(response.encode("utf-8"))

        # Cerrar el socket del cliente
        client_socket.close()
    except OSError as e:
        print(f"Error en el servidor: {e}")
        continue
