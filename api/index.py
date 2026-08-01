from http.server import BaseHTTPRequestHandler

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feliz Día de la Novia</title>
    <!-- Fuentes bonitas -->
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <!-- Librería para fuegos artificiales -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
            /* Fondo degradado rosa/rojo */
            background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 50%, #e63946 100%);
            font-family: 'Poppins', sans-serif;
            overflow-x: hidden;
            position: relative;
            padding: 20px;
        }

        /* --- Contenedor Principal en Cuadrícula --- */
        .main-container {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            grid-template-rows: repeat(3, auto);
            gap: 20px;
            align-items: center;
            justify-items: center;
            max-width: 1200px;
            z-index: 10;
        }

        /* --- El Mensaje Central Original --- */
        .card-mensaje {
            grid-column: 2;
            grid-row: 2;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.4);
            padding: 40px 30px;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(230, 57, 70, 0.3);
            animation: popIn 1s ease-out forwards;
            min-width: 320px;
            max-width: 500px;
        }

        .card-mensaje h1 {
            font-family: 'Dancing Script', cursive;
            font-size: 3rem;
            color: #ffffff;
            text-shadow: 2px 3px 6px rgba(139, 0, 0, 0.4);
            margin-bottom: 20px;
            line-height: 1.2;
        }

        .card-mensaje p {
            font-size: 1.5rem;
            font-weight: 600;
            color: #fff0f3;
            text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.2);
            letter-spacing: 1px;
        }

        /* --- Estilos de las Tarjetas de Fotos (Flip Cards) --- */
        .flip-card {
            background-color: transparent;
            width: 150px;
            height: 200px;
            perspective: 1000px;
            cursor: pointer;
            animation: fadeIn 1.5s ease-out forwards;
        }

        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
            transform-style: preserve-3d;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            border-radius: 15px;
        }

        .flip-card.flipped .flip-card-inner {
            transform: rotateY(180deg);
        }

        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-radius: 15px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 4px solid white;
        }

        .flip-card-front img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .flip-card-back {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            color: #a71d31;
            transform: rotateY(180deg);
            padding: 15px;
            font-family: 'Dancing Script', cursive;
            font-size: 1.4rem;
            font-weight: bold;
            line-height: 1.3;
        }

        /* Posiciones en la cuadrícula alrededor del mensaje */
        .foto-1 { grid-column: 1; grid-row: 1; }
        .foto-2 { grid-column: 2; grid-row: 1; }
        .foto-3 { grid-column: 3; grid-row: 1; }
        .foto-4 { grid-column: 1; grid-row: 3; }
        .foto-5 { grid-column: 2; grid-row: 3; }
        .foto-6 { grid-column: 3; grid-row: 3; }

        /* Adaptación para pantallas pequeñas / móviles */
        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: repeat(2, 1fr);
                grid-template-rows: auto auto auto auto;
                gap: 15px;
            }
            .card-mensaje {
                grid-column: 1 / -1;
                grid-row: 1;
                padding: 25px 20px;
            }
            .card-mensaje h1 { font-size: 2.3rem; }
            .card-mensaje p { font-size: 1.2rem; }
            .flip-card { width: 130px; height: 170px; }
            
            .foto-1 { grid-column: 1; grid-row: 2; }
            .foto-2 { grid-column: 2; grid-row: 2; }
            .foto-3 { grid-column: 1; grid-row: 3; }
            .foto-4 { grid-column: 2; grid-row: 3; }
            .foto-5 { grid-column: 1; grid-row: 4; }
            .foto-6 { grid-column: 2; grid-row: 4; }
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
            0% { transform: translateY(0) scale(0.8) rotate(0deg); opacity: 1; }
            100% { transform: translateY(-110vh) scale(1.3) rotate(360deg); opacity: 0; }
        }

        @keyframes popIn {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div class="main-container">
        
        <!-- Mensaje Central Restaurado -->
        <div class="card-mensaje">
            <h1>¡Feliz día a la mejor novia del mundo! ❤️</h1>
            <p>te amo muchooooo mi vidaaaaa 💕</p>
        </div>

        <!-- Las 6 fotos con efecto de volteo -->
        <div class="flip-card foto-1" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/436338b9-43c3-4f27-9192-3a56ae23405f.jpg" alt="Foto 1">
                </div>
                <div class="flip-card-back">
                    <p>Eres lo mejor que me ha pasado en la vida. Cada segundo a tu lado es un regalo. ❤️</p>
                </div>
            </div>
        </div>

        <div class="flip-card foto-2" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/d0d3b666-8809-417b-8395-585a9a10af41.jpg" alt="Foto 2">
                </div>
                <div class="flip-card-back">
                    <p>Amo tu sonrisa, tu forma de ser y cómo me haces sentir. ¡Gracias por existir! 🥰</p>
                </div>
            </div>
        </div>

        <div class="flip-card foto-3" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/63f8903c-e0da-4a57-932d-3db9968411d7.jpg" alt="Foto 3">
                </div>
                <div class="flip-card-back">
                    <p>Contigo, todos los días son especiales. Eres mi lugar seguro y mi felicidad completa. 💖</p>
                </div>
            </div>
        </div>

        <div class="flip-card foto-4" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/b81109a1-077a-42c6-947f-8594589d6e27.jpg" alt="Foto 4">
                </div>
                <div class="flip-card-back">
                    <p>Me encantas demasiado. No me canso de decirte lo mucho que te amo, mi vida. 😍</p>
                </div>
            </div>
        </div>

        <div class="flip-card foto-5" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/f233f2da-d4f7-4148-83b3-8555e714660a.jpg" alt="Foto 5">
                </div>
                <div class="flip-card-back">
                    <p>Gracias por cada risa, cada abrazo y por compartir tu vida conmigo. ¡Te adoro! ✨</p>
                </div>
            </div>
        </div>

        <div class="flip-card foto-6" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/3c97805a-5264-42b7-bd20-0063945f9570.jpg" alt="Foto 6">
                </div>
                <div class="flip-card-back">
                    <p>Eres mi presente y mi futuro. ¡Te amo muchooooo, hoy y siempre! ❤️🌹</p>
                </div>
            </div>
        </div>

    </div>

    <script>
        function flipCard(cardElement) {
            cardElement.classList.toggle('flipped');
        }

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

        function launchFireworks() {
            const duration = 5 * 1000;
            const animationEnd = Date.now() + duration;
            const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

            function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
            }

            const interval = setInterval(function() {
                const timeLeft = animationEnd - Date.now();

                if (timeLeft <= 0) {
                    return clearInterval(interval);
                }

                const particleCount = 50 * (timeLeft / duration);
                
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                    colors: ['#ff007f', '#ff4d6d', '#ff758c', '#ffffff', '#e63946']
                }));
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
                    colors: ['#ff007f', '#ff4d6d', '#ff758c', '#ffffff', '#e63946']
                }));
            }, 250);
        }

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