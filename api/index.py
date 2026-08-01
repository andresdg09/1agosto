from http.server import BaseHTTPRequestHandler

# Definimos el contenido HTML, CSS y JS en una constante
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
            overflow-x: hidden; /* Evita scroll horizontal */
            position: relative;
            padding: 20px;
        }

        /* --- Contenedor Principal en Cuadrícula --- */
        .main-container {
            display: grid;
            /* 3 columnas: fotos laterales y mensaje central */
            grid-template-columns: 1fr auto 1fr;
            /* 3 filas */
            grid-template-rows: repeat(3, auto);
            gap: 20px;
            align-items: center;
            justify-items: center;
            max-width: 1200px;
            z-index: 10; /* Por encima de los corazones */
        }

        /* --- El Mensaje Central --- */
        .card-mensaje {
            grid-column: 2; /* Columna central */
            grid-row: 2;    /* Fila central */
            background: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 255, 255, 0.5);
            padding: 40px 30px;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(230, 57, 70, 0.4);
            animation: popIn 1s ease-out forwards;
            min-width: 300px;
        }

        .card-mensaje h1 {
            font-family: 'Dancing Script', cursive;
            font-size: 3.5rem;
            color: #ffffff;
            text-shadow: 2px 3px 6px rgba(139, 0, 0, 0.5);
            margin-bottom: 15px;
            line-height: 1.2;
        }

        .card-mensaje p {
            font-size: 1.6rem;
            font-weight: 600;
            color: #fff0f3;
            text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.2);
        }

        /* --- Estilos de las Tarjetas de Fotos (Flip Cards) --- */
        .flip-card {
            background-color: transparent;
            width: 150px;
            height: 200px;
            perspective: 1000px; /* Necesario para el efecto 3D */
            cursor: pointer;
            animation: fadeIn 1.5s ease-out forwards;
        }

        /* Contenedor interior que hace el giro */
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

        /* Clase que aplicaremos con JS al hacer clic */
        .flip-card.flipped .flip-card-inner {
            transform: rotateY(180deg);
        }

        /* Estilos para la parte delantera y trasera */
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden; /* Oculta la parte trasera al girar */
            backface-visibility: hidden;
            border-radius: 15px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 4px solid white;
        }

        /* Parte delantera: La Foto */
        .flip-card-front img {
            width: 100%;
            height: 100%;
            object-fit: cover; /* Ajusta la foto sin deformarla */
        }

        /* Parte trasera: El Mensaje Bonito */
        .flip-card-back {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            color: #a71d31;
            transform: rotateY(180deg); /* Ya está girada por defecto */
            padding: 15px;
            font-family: 'Dancing Script', cursive;
            font-size: 1.4rem;
            font-weight: bold;
            line-height: 1.3;
        }

        /* --- Posicionamiento de las Fotos en la Cuadrícula --- */
        .foto-1 { grid-column: 1; grid-row: 1; }
        .foto-2 { grid-column: 2; grid-row: 1; }
        .foto-3 { grid-column: 3; grid-row: 1; }
        .foto-4 { grid-column: 1; grid-row: 3; }
        .foto-5 { grid-column: 2; grid-row: 3; }
        .foto-6 { grid-column: 3; grid-row: 3; }

        /* Ajustes para móviles */
        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: repeat(2, 1fr);
                grid-template-rows: auto auto auto auto;
                gap: 15px;
            }
            .card-mensaje {
                grid-column: 1 / -1; /* Ocupa todo el ancho */
                grid-row: 1;
                padding: 25px 20px;
            }
            .card-mensaje h1 { font-size: 2.5rem; }
            .card-mensaje p { font-size: 1.2rem; }
            .flip-card { width: 130px; height: 170px; }
            
            /* Re-posicionar fotos en móvil */
            .foto-1 { grid-column: 1; grid-row: 2; }
            .foto-2 { grid-column: 2; grid-row: 2; }
            .foto-3 { grid-column: 1; grid-row: 3; }
            .foto-4 { grid-column: 2; grid-row: 3; }
            .foto-5 { grid-column: 1; grid-row: 4; }
            .foto-6 { grid-column: 2; grid-row: 4; }
        }

        /* --- Elementos Decorativos de Fondo (Corazones) --- */
        .heart {
            position: absolute;
            bottom: -50px;
            color: rgba(255, 255, 255, 0.6);
            font-size: 20px;
            animation: floatUp linear infinite;
            z-index: 1;
        }

        /* --- Animaciones --- */
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

    <!-- Contenedor de la cuadrícula -->
    <div class="main-container">
        
        <!-- Mensaje Central -->
        <div class="card-mensaje">
            <h1>¡Feliz día mi amor! ❤️</h1>
            <p>Toca nuestras fotos para una sorpresa...</p>
        </div>

        <!-- --- LAS 6 TARJETAS DE FOTOS --- -->
        
        <!-- Foto 1 -->
        <div class="flip-card foto-1" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/436338b9-43c3-4f27-9192-3a56ae23405f.jpg" alt="Nuestra foto 1">
                </div>
                <div class="flip-card-back">
                    <p>Eres lo mejor que me ha pasado en la vida. Cada segundo a tu lado es un regalo. ❤️</p>
                </div>
            </div>
        </div>

        <!-- Foto 2 -->
        <div class="flip-card foto-2" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/d0d3b666-8809-417b-8395-585a9a10af41.jpg" alt="Nuestra foto 2">
                </div>
                <div class="flip-card-back">
                    <p>Amo tu sonrisa, tu forma de ser y cómo me haces sentir. ¡Gracias por existir! 🥰</p>
                </div>
            </div>
        </div>

        <!-- Foto 3 -->
        <div class="flip-card foto-3" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/63f8903c-e0da-4a57-932d-3db9968411d7.jpg" alt="Nuestra foto 3">
                </div>
                <div class="flip-card-back">
                    <p>Contigo, todos los días son especiales. Eres mi lugar seguro y mi felicidad completa. 💖</p>
                </div>
            </div>
        </div>

        <!-- Foto 4 -->
        <div class="flip-card foto-4" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/b81109a1-077a-42c6-947f-8594589d6e27.jpg" alt="Nuestra foto 4">
                </div>
                <div class="flip-card-back">
                    <p>Me encantas demasiado. No me canso de decirte lo mucho que te amo, mi vida. 😍</p>
                </div>
            </div>
        </div>

        <!-- Foto 5 -->
        <div class="flip-card foto-5" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/f233f2da-d4f7-4148-83b3-8555e714660a.jpg" alt="Nuestra foto 5">
                </div>
                <div class="flip-card-back">
                    <p>Gracias por cada risa, cada abrazo y por compartir tu vida conmigo. ¡Te adoro! ✨</p>
                </div>
            </div>
        </div>

        <!-- Foto 6 -->
        <div class="flip-card foto-6" onclick="flipCard(this)">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="https://images.mirror-ai.net/p/3c97805a-5264-42b7-bd20-0063945f9570.jpg" alt="Nuestra foto 6">
                </div>
                <div class="flip-card-back">
                    <p>Eres mi presente y mi futuro. ¡Te amo muchooooo, hoy y siempre! ❤️🌹</p>
                </div>
            </div>
        </div>

    </div>

    <!-- --- JAVASCRIPT --- -->
    <script>
        // 1. Función para voltear la tarjeta al hacer clic
        function flipCard(cardElement) {
            cardElement.classList.toggle('flipped');
        }

        // 2. Crear corazones flotantes de fondo
        function createHeart() {
            const heart = document.createElement('div');
            heart.classList.add('heart');
            heart.innerHTML = '❤️';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.animationDuration = Math.random() * 3 + 4 + 's'; // Entre 4 y 7s
            heart.style.fontSize = Math.random() * 20 + 15 + 'px'; // Entre 15 y 35px
            document.body.appendChild(heart);

            // Borrar el corazón después de que termine la animación
            setTimeout(() => {
                heart.remove();
            }, 7000);
        }

        // Crear corazones continuamente
        setInterval(createHeart, 300);

        // 3. Fuegos Artificiales al abrir la página
        function launchFireworks() {
            const duration = 5 * 1000; // 5 segundos
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
                
                // Disparos desde lados aleatorios
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                    colors: ['#ff007f', '#ff4d6d', '#ff758c', '#ffffff', '#e63946'] // Rosas y rojos
                }));
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
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
        # 1. Configurar encabezados de respuesta
        self.send_response(200)
        # Especificamos que la respuesta es HTML
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # 2. Enviar el contenido HTML completo
        self.wfile.write(HTML_CONTENT.encode('utf-8'))
        return