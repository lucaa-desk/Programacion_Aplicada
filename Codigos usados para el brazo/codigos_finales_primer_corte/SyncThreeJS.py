import wifi
import socketpool
import pwmio
import board
import re

ssid = 'Shi'
password = 'arbr4619'

wifi.radio.connect(ssid, password)
print('Conectado a Wi-Fi')
print('Dirección IP:', wifi.radio.ipv4_address)

servo_Principal = pwmio.PWMOut(board.GP14, frequency=50, duty_cycle=0)
servo_Secundario = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brazo Mecánico en 3D</title>
    <style>
        body{font-family:Arial,sans-serif;background-color:#8B4513;margin:0;padding:0;display:flex;justify-content:center;align-items:center;flex-direction:column;height:100vh}
        .control-panel{background-color:white;padding:10px;border-radius:10px;text-align:center;width:200px}
        h1{font-size:20px;margin-bottom:10px;color:#333}
        p{font-size:14px;margin-bottom:10px;color:#555}
        input[type=range]{width:100%;margin-bottom:10px;height:5px;background:#ddd;outline:none;opacity:.8;transition:opacity .2s}
        input[type=range]:hover{opacity:1}
        input[type=range]::-webkit-slider-thumb{width:10px;height:10px;background:#007bff;border-radius:50%;cursor:pointer}
        #canvas-container{width:100%;height:300px;margin-top:10px;background-color:#deb887}
    </style>
</head>
<body>
    <div class="control-panel">
        <h1>Servo-Brazo</h1>
        <p>Rotación Brazo Inferior:</p>
        <input type="range" id="lowerArmSlider" min="0" max="180" value="45"><br><br>
        <p>Rotación Brazo Superior:</p>
        <input type="range" id="upperArmSlider" min="0" max="70" value="70">
    </div>
    <div id="canvas-container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Escena y cámara para el brazo virtual
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 300, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, 300);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        // Luces
        const light = new THREE.AmbientLight(0xffffff);
        scene.add(light);

        // Material del brazo virtual (color naranja)
        const materialOrange = new THREE.MeshBasicMaterial({ color: 0xffa500 });

        // Base
        const geometryBase = new THREE.BoxGeometry(5, 3, 2); 
        const base = new THREE.Mesh(geometryBase, materialOrange);
        base.position.set(0, -1.5, 0); 
        scene.add(base);

        // Brazo inferior
        const geometryLowerArm = new THREE.BoxGeometry(4, 0.4, 0.4);
        const lowerArm = new THREE.Mesh(geometryLowerArm, materialOrange);
        lowerArm.position.set(0, -0.2, 0);
        lowerArm.geometry.translate(2, 0, 0);
        scene.add(lowerArm);

        // Brazo superior
        const geometryUpperArm = new THREE.BoxGeometry(4, 0.4, 0.4);
        const upperArm = new THREE.Mesh(geometryUpperArm, materialOrange);
        upperArm.position.set(4, 1, 0);
        upperArm.geometry.translate(2, 0, 0);
        scene.add(upperArm);

        // Control deslizante para el brazo inferior (sincronizado con el servo físico)
        const lowerArmSlider = document.getElementById('lowerArmSlider');
        lowerArmSlider.addEventListener('input', () => {
            const angle = THREE.MathUtils.degToRad(180 - parseInt(lowerArmSlider.value)); // Invertir el ángulo
            lowerArm.rotation.z = angle;
            updateUpperArmPosition();
            updateServos();
        });

        // Control deslizante para el brazo superior (sincronizado con el servo físico)
        const upperArmSlider = document.getElementById('upperArmSlider');
        upperArmSlider.addEventListener('input', () => {
            const sliderValue = parseInt(upperArmSlider.value);
            const angle = THREE.MathUtils.degToRad(290 + sliderValue);
            upperArm.rotation.z = angle;
            updateServos();
        });

        // Función para actualizar la posición del brazo superior
        function updateUpperArmPosition() {
            const lowerArmEndX = lowerArm.position.x + Math.cos(lowerArm.rotation.z) * 4;
            const lowerArmEndY = lowerArm.position.y + Math.sin(lowerArm.rotation.z) * 4;
            upperArm.position.set(lowerArmEndX, lowerArmEndY, 0);
        }

        // Función para enviar los valores de los sliders a los servos físicos
        function updateServos() {
            const value1 = document.getElementById('lowerArmSlider').value;
            const value2 = document.getElementById('upperArmSlider').value;
            fetch(`/update_servos?value1=${value1}&value2=${value2}`)
                .then(response => response.text())
                .then(data => console.log('Servos actualizados:', data))
                .catch(error => console.error('Error:', error));
        }

        // Posicionar correctamente al iniciar
        updateUpperArmPosition();

        // Cámara
        camera.position.z = 10;

        // Animación del brazo virtual
        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }

        animate();
    </script>
</body>
</html>
"""

def handle_request(client, chunk_size=1024):
    buffer = bytearray(1024)
    bytes_received = client.recv_into(buffer)
    request_str = buffer[:bytes_received].decode('utf-8')

    if 'GET /update_servos' in request_str:
        match = re.search(r'GET /update_servos\?value1=([0-9]+)&value2=([0-9]+)', request_str)
        if match:
            value1 = int(match.group(1))
            value2 = int(match.group(2))

            mapped_value_Principal = map_range(value1, 0, 100, 1500, 8000)
            mapped_value_Secundario = map_range(value2, 0, 70, 1000, 3000)

            servo_Principal.duty_cycle = mapped_value_Principal
            servo_Secundario.duty_cycle = mapped_value_Secundario

        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/plain\r\n")
        client.send("Connection: close\r\n\r\n")
        client.send("OK")
    else:
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/html\r\n")
        client.send("Connection: close\r\n\r\n")
        for i in range(0, len(html), chunk_size):
            client.send(html[i:i + chunk_size])

    client.close()

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
        
start_server()
