from http.server import BaseHTTPRequestHandler

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feliz Día de la Novia</title>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            height: 100vh;
            width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 50%, #e63946 100%);
            font-family: 'Poppins', sans-serif;
            overflow: hidden;
            position: relative;
        }

        /* Canvas para los fuegos artificiales */
        #fireworks-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 2;
        }

        /* Contenedor principal */
        .card {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.4);
            padding: 40px 30px;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(230, 57, 70, 0.3);
            max-width: 90%;
            width: 500px;
            z-index: 10;
            animation: popIn 1s ease-out forwards;
        }

        h1 {
            font-family: 'Dancing Script', cursive;
            font-size: 3rem;
            color: #ffffff;
            text-shadow: 2px 3px 6px rgba(139, 0, 0, 0.4);
            margin-bottom: 20px;
            line-height: 1.2;
        }

        p {
            font-size: 1.5rem;
            font-weight: 600;
            color: #fff0f3;
            text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.2);
            letter-spacing: 1px;
        }

        /* Corazones flotantes de fondo */
        .heart {
            position: absolute;
            bottom: -50px;
            color: rgba(255, 255, 255, 0.7);
            font-size: 20px;
            animation: floatUp linear infinite;
            z-index: 1;
        }

        @keyframes floatUp {
            0% {
                transform: translateY(0) scale(0.8) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(-105vh) scale(1.3) rotate(360deg);
                opacity: 0;
            }
        }

        @keyframes popIn {
            0% {
                transform: scale(0.5);
                opacity: 0;
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }
    </style>
</head>
<body>

    <canvas id="fireworks-canvas"></canvas>

    <div class="card">
        <h1>¡Feliz día a la mejor novia del mundo! ❤️</h1>
        <p>Te amo muchooooo mi vidaaaaa 💕</p>
    </div>

    <!-- Generador de Corazones Flotantes y Fuegos Artificiales -->
    <script>
        // 1. Crear corazones flotantes de fondo
        function createHeart() {
            const heart = document.createElement('div');
            heart.classList.add('heart');
            heart.innerHTML = '❤️';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.animationDuration = Math.random() * 3 + 4 + 's';
            heart.style.fontSize = Math.random() * 20 + 15 + 'px';
            document.body.appendChild(heart);

            setTimeout(() => {
                heart.remove();
            }, 7000);
        }

        setInterval(createHeart, 300);

        // 2. Fuegos Artificiales al abrir la página
        function launchFireworks() {
            const duration = 5 * 1000;
            const animationEnd = Date.now() + duration;
            const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 3 };

            function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
            }

            const interval = setInterval(function() {
                const timeLeft = animationEnd - Date.now();

                if (timeLeft <= 0) {
                    return clearInterval(interval);
                }

                const particleCount = 50 * (timeLeft / duration);
                
                // Disparos de fuegos artificiales rosa y rojos desde lados aleatorios
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0.1, 0.4), y: Math.random() - 0.2 },
                    colors: ['#ff007f', '#ff4d6d', '#ff758c', '#ffffff', '#e63946']
                }));
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0.6, 0.9), y: Math.random() - 0.2 },
                    colors: ['#ff007f', '#ff4d6d', '#ff758c', '#ffffff', '#e63946']
                }));
            }, 250);
        }

        // Ejecutar los fuegos artificiales apenas cargue la página
        window.onload = launchFireworks;
    </script>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))
        return