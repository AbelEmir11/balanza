from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import random

# Inicializar FastAPI
app = FastAPI(
    title="Balanza del Entretenimiento API",
    description="Una API que devuelve memes y canciones basados en datos del usuario",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos

class CancionModel(BaseModel):
    titulo: str
    youtube_id: str
    url: str

class UserData(BaseModel):
    sexo: str
    edad: int
    altura: float  # en metros
    peso: float    # en kg

class BalanzaResponse(BaseModel):
    imc: float
    categoria_imc: str
    generacion: str
    meme: str
    cancion: CancionModel
    mensaje_motivacional: str

# Base de datos en memoria (luego podemos expandir)
MEMES = {
    "bajo_peso": [
        "¿Seguro que no eres un espagueti con ojos? 🍝",
        "Eres tan delgado que cuando te pones de perfil desapareces",
        "Tu IMC dice que necesitas más pizza en tu vida 🍕"
    ],
    "normal": [
        "Perfectamente balanceado, como todo debería ser - Thanos",
        "Eres el golden retriever de los IMCs ✨",
        "Tu cuerpo: ✅ Tu actitud: esperamos que también ✅"
    ],
    "sobrepeso": [
        "Eres thicc y eso está de moda 💪",
        "Más para abrazar 🤗",
        "Tu personalidad pesa más que tu cuerpo ❤️"
    ],
    "obesidad": [
        "Eres grande en todos los sentidos 👑",
        "Tu corazón es más grande que tu cintura ❤️",
        "Recuerda: eres más que un número en una balanza"
    ]
}

CANCIONES = {
    "gen_z": [
        {
            "titulo": "Bad Bunny - Tití Me Preguntó",
            "youtube_id": "saGYMkzIBXQ",
            "url": "https://www.youtube.com/watch?v=saGYMkzIBXQ"
        },
        {
            "titulo": "Olivia Rodrigo - Good 4 U",
            "youtube_id": "gNi_6U5Pm_o",
            "url": "https://www.youtube.com/watch?v=gNi_6U5Pm_o"
        },
        {
            "titulo": "Dua Lipa - Levitating",
            "youtube_id": "TUVcZfQe-Kw",
            "url": "https://www.youtube.com/watch?v=TUVcZfQe-Kw"
        },
        {
            "titulo": "The Weeknd - Blinding Lights",
            "youtube_id": "4NRXx6U8ABQ",
            "url": "https://www.youtube.com/watch?v=4NRXx6U8ABQ"
        }
    ],
    "millennial": [
        {
            "titulo": "Backstreet Boys - I Want It That Way",
            "youtube_id": "4fndeDfaWCg",
            "url": "https://www.youtube.com/watch?v=4fndeDfaWCg"
        },
        {
            "titulo": "Britney Spears - Toxic",
            "youtube_id": "LOZuxwVk7TU",
            "url": "https://www.youtube.com/watch?v=LOZuxwVk7TU"
        },
        {
            "titulo": "Eminem - Lose Yourself",
            "youtube_id": "_Yhyp-_hX2s",
            "url": "https://www.youtube.com/watch?v=_Yhyp-_hX2s"
        },
        {
            "titulo": "Beyoncé - Crazy In Love",
            "youtube_id": "ViwtNLUqkMY",
            "url": "https://www.youtube.com/watch?v=ViwtNLUqkMY"
        }
    ],
    "gen_x": [
        {
            "titulo": "Nirvana - Smells Like Teen Spirit",
            "youtube_id": "hTWKbfoikeg",
            "url": "https://www.youtube.com/watch?v=hTWKbfoikeg"
        },
        {
            "titulo": "Queen - Bohemian Rhapsody",
            "youtube_id": "fJ9rUzIMcZQ",
            "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"
        },
        {
            "titulo": "Michael Jackson - Billie Jean",
            "youtube_id": "Zi_XLOBDo_Y",
            "url": "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"
        },
        {
            "titulo": "Madonna - Like a Prayer",
            "youtube_id": "79fzeNUqQbQ",
            "url": "https://www.youtube.com/watch?v=79fzeNUqQbQ"
        }
    ],
    "boomer": [
        {
            "titulo": "The Beatles - Hey Jude",
            "youtube_id": "A_MjCqQoLLA",
            "url": "https://www.youtube.com/watch?v=A_MjCqQoLLA"
        },
        {
            "titulo": "Led Zeppelin - Stairway to Heaven",
            "youtube_id": "QkF3oxziUI4",
            "url": "https://www.youtube.com/watch?v=QkF3oxziUI4"
        },
        {
            "titulo": "The Rolling Stones - Paint It Black",
            "youtube_id": "O4irXQhgMqg",
            "url": "https://www.youtube.com/watch?v=O4irXQhgMqg"
        },
        {
            "titulo": "Bob Dylan - Like a Rolling Stone",
            "youtube_id": "IwOfCgkyEj0",
            "url": "https://www.youtube.com/watch?v=IwOfCgkyEj0"
        }
    ]
}

# Funciones auxiliares
def calcular_imc(peso: float, altura: float) -> float:
    return round(peso / (altura ** 2), 2)

def categorizar_imc(imc: float) -> str:
    if imc < 18.5:
        return "bajo_peso"
    elif 18.5 <= imc < 25:
        return "normal"
    elif 25 <= imc < 30:
        return "sobrepeso"
    else:
        return "obesidad"

def determinar_generacion(edad: int) -> str:
    if edad <= 27:
        return "gen_z"
    elif edad <= 43:
        return "millennial"
    elif edad <= 59:
        return "gen_x"
    else:
        return "boomer"

def generar_mensaje_motivacional(categoria_imc: str, edad: int) -> str:
    mensajes = {
        "bajo_peso": f"A los {edad} años, tienes tiempo de sobra para ganar masa muscular. ¡Dale que se puede! 💪",
        "normal": f"¡Felicidades! A los {edad} años mantienes un peso saludable. Sigue así! ⭐",
        "sobrepeso": f"A los {edad} años todavía estás a tiempo de hacer cambios positivos. ¡Ánimo! 🌟",
        "obesidad": f"Cada día es una nueva oportunidad para cuidarte. A los {edad} años, tu salud es lo más importante. ❤️"
    }
    return mensajes.get(categoria_imc, "¡Eres único y eso es lo que importa! ✨")

# Endpoints
@app.get("/")
async def root():
    return {
        "mensaje": "¡Bienvenido a la Balanza del Entretenimiento! 🎵",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.post("/balanza", response_model=BalanzaResponse)
async def calcular_balanza(user_data: UserData):
    try:
        # Validaciones básicas
        if user_data.edad < 1 or user_data.edad > 120:
            raise HTTPException(status_code=400, detail="Edad debe estar entre 1 y 120 años")
        
        if user_data.altura < 0.5 or user_data.altura > 3.0:
            raise HTTPException(status_code=400, detail="Altura debe estar entre 0.5 y 3.0 metros")
        
        if user_data.peso < 10 or user_data.peso > 500:
            raise HTTPException(status_code=400, detail="Peso debe estar entre 10 y 500 kg")
        
        # Cálculos
        imc = calcular_imc(user_data.peso, user_data.altura)
        categoria_imc = categorizar_imc(imc)
        generacion = determinar_generacion(user_data.edad)
        
        # Seleccionar contenido aleatorio
        meme = random.choice(MEMES[categoria_imc])
        cancion = random.choice(CANCIONES[generacion])
        mensaje_motivacional = generar_mensaje_motivacional(categoria_imc, user_data.edad)
        
        return BalanzaResponse(
            imc=imc,
            categoria_imc=categoria_imc.replace("_", " ").title(),
            generacion=generacion.replace("_", " ").upper(),
            meme=meme,
            cancion=cancion,
            mensaje_motivacional=mensaje_motivacional
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Endpoint para obtener estadísticas de la aplicación"""
    return {
        "total_memes": sum(len(memes) for memes in MEMES.values()),
        "total_canciones": sum(len(canciones) for canciones in CANCIONES.values()),
        "categorias_imc": list(MEMES.keys()),
        "generaciones": list(CANCIONES.keys())
    }

# Para ejecutar: uvicorn main:app --reload