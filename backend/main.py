from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from fastapi.staticfiles import StaticFiles
import random

# Inicializar FastAPI
app = FastAPI(
    title="Balanza del Entretenimiento API",
    description="Una API que devuelve memes y canciones basados en datos del usuario",
    version="1.0.0"
)

app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")


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

class MemeModel(BaseModel):
    url: str
    alt: str

class BalanzaResponse(BaseModel):
    imc: float
    categoria_imc: str
    generacion: str
    meme: MemeModel
    cancion: CancionModel
    mensaje_motivacional: str

class UserData(BaseModel):
    sexo: str
    edad: int
    altura: float  # en metros
    peso: float    # en kg


# Base de datos en memoria (luego podemos expandir)
MEMES = {
    "bajo_peso": [
       {
            "url":"https://www.bing.com/images/search?view=detailV2&ccid=DRSXLYH%2f&id=49F4F9618BD90B07D64E936EA1702F28DF82A5E4&thid=OIP.DRSXLYH_M7X8pcyU9sccaAHaH5&mediaurl=https%3a%2f%2fi.pinimg.com%2foriginals%2f12%2fc4%2f85%2f12c485bc197d4108091d532ecb632177.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.0d14972d81ff33b5fca5cc94f6c71c68%3frik%3d5KWC3ygvcKFukw%26pid%3dImgRaw%26r%3d0&exph=1494&expw=1400&q=personaje+alto+y+flaco&FORM=IRPRST&ck=270E2E7EDEC647B7C9A6D26FAA15ABFB&selectedIndex=0&itb=0",
            "alt": "Meme de persona delgada"
        },
        {
            "url": "https://tse4.mm.bing.net/th/id/OIP.8Ej3XE6J_9eYHRULYGRg5QHaMb?r=0&cb=thfvnext&rs=1&pid=ImgDetMain&o=7&rm=3",
            "alt": "Meme skinny person"
        },
        
    ],
    "normal": [
        {
            "url": "https://i.imgflip.com/2/1bij.jpg",
            "alt": "Meme perfectamente balanceado como todo debería ser"
        },
        {
            "url": "/imagenes/peso_normal.jpg",
            "alt": "Meme peso saludable"
        },
     
    ],
   "sobrepeso": [
        {
            "url": "https://i.imgflip.com/2/5c7lwq.jpg",
            "alt": "Meme thicc"
        },
        {
            "url": "/imagenes/no gordas.webp",
            "alt": "Meme motivacional sobrepeso"
        },
        {
            "url": "https://i.imgflip.com/2/1otk96.jpg",
            "alt": "Meme body positive"
        }
    ],
    "obesidad": [
        {
            "url": "https://i.imgflip.com/2/2y3ez.jpg",
            "alt": "Meme motivacional obesidad"
        },
        {
            "url": "/imagenes/no gordas.webp",
            "alt": "Meme corazón grande"
        },
        {
            "url": "https://i.imgflip.com/2/1g8my4.jpg",
            "alt": "Meme más que un número"
        }
    ]
}

# Easter eggs - Combinaciones específicas de género + IMC + generación
COMBINACION_CANCIONES = {
    "femenino_bajo_peso": [
        {
            "titulo": "Jarabe de Palo - La Flaca",
            "youtube_id": "HhZaHf8RP6g",
            "url": "https://www.youtube.com/watch?v=HhZaHf8RP6g"
        },
        {
            "titulo": "Luis Alberto Spinetta - Flaca",
            "youtube_id": "tZkouut-9RQ",
            "url": "https://www.youtube.com/watch?v=tZkouut-9RQ"
        }
    ],
    "masculino_obesidad_millennial": [
        {
            "titulo": "Wisin & Yandel - Oye Gelda",
            "youtube_id": "9Z0hmnHnRR8",
            "url": "https://www.youtube.com/watch?v=9Z0hmnHnRR8"
        }
    ],
    "femenino_obesidad_gen_z": [
        {
            "titulo": "Lizzo - About Damn Time",
            "youtube_id": "nQwuakxYUR4",
            "url": "https://www.youtube.com/watch?v=nQwuakxYUR4"
        },
        {
            "titulo": "Meghan Trainor - All About That Bass",
            "youtube_id": "7PCkvCPvDXk",
            "url": "https://www.youtube.com/watch?v=7PCkvCPvDXk"
        }
    ],
    "masculino_bajo_peso_gen_z": [
        {
            "titulo": "Bruno Mars - Count On Me",
            "youtube_id": "CRsXwuuQbao",
            "url": "https://www.youtube.com/watch?v=CRsXwuuQbao"
        },
        {
            "titulo": "Ed Sheeran - Shape of You",
            "youtube_id": "JGwWNGJdvx8",
            "url": "https://www.youtube.com/watch?v=JGwWNGJdvx8"
        }
    ],
    "femenino_normal_millennial": [
        {
            "titulo": "Alanis Morissette - You Oughta Know",
            "youtube_id": "NPcyTyilmYY",
            "url": "https://www.youtube.com/watch?v=NPcyTyilmYY"
        },
        {
            "titulo": "No Doubt - Just a Girl",
            "youtube_id": "PHzOOQfhPFg",
            "url": "https://www.youtube.com/watch?v=PHzOOQfhPFg"
        }
    ]
}

# Canciones especiales por categoría de IMC (tienen prioridad intermedia)
CANCIONES_ESPECIALES_IMC = {
    "obesidad": [
        {
            "titulo": "Wisin & Yandel - Oye Gelda",
            "youtube_id": "9Z0hmnHnRR8",
            "url": "https://www.youtube.com/watch?v=9Z0hmnHnRR8"
        },
        {
            "titulo": "Violeta Parra - Mazúrquica Modérnica",
            "youtube_id": "5F4wZWfSdD8",
            "url": "https://www.youtube.com/watch?v=5F4wZWfSdD8"
        },
        {
            "titulo": "La Sonora Dinamita - El Gordito Bonito",
            "youtube_id": "kpSFE88dCQ8",
            "url": "https://www.youtube.com/watch?v=kpSFE88dCQ8"
        }
    ],
    "bajo_peso": [
        {
            "titulo": "Daddy Yankee - Gasolina",
            "youtube_id": "qGKrc3A6HHM",
            "url": "https://www.youtube.com/watch?v=qGKrc3A6HHM"
        },
        {
            "titulo": "Alvaro Soler - El Mismo Sol",
            "youtube_id": "1juts-h7VzU",
            "url": "https://www.youtube.com/watch?v=1juts-h7VzU"
        },
        {
            "titulo": "Manu Chao - Me Gustas Tu",
            "youtube_id": "rs6Y4kZ8qtw",
            "url": "https://www.youtube.com/watch?v=rs6Y4kZ8qtw"
        }
    ]
    # "normal" y "sobrepeso" usarán las canciones normales por generación
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
        
        # Lógica de selección de canción:
        # 1. PRIORIDAD MÁXIMA: Combinaciones específicas (género + IMC o género + IMC + generación)
        # 2. PRIORIDAD BAJA: Canciones normales por generación
        
        cancion = None
        
        # 1. Buscar combinación específica con generación
        combinacion_key = f"{user_data.sexo}_{categoria_imc}_{generacion}"
        if combinacion_key in COMBINACION_CANCIONES:
            cancion = random.choice(COMBINACION_CANCIONES[combinacion_key])
        
        # Si no hay combinación específica, buscar por género + IMC
        if not cancion:
            combinacion_key_simple = f"{user_data.sexo}_{categoria_imc}"
            if combinacion_key_simple in COMBINACION_CANCIONES:
                cancion = random.choice(COMBINACION_CANCIONES[combinacion_key_simple])
        
        # 2. Si no hay combinación, usar canción normal por generación
        if not cancion:
            cancion = random.choice(CANCIONES[generacion])
            
        mensaje_motivacional = generar_mensaje_motivacional(categoria_imc, user_data.edad)
        
        return BalanzaResponse(
            imc=imc,
            categoria_imc=categoria_imc.replace("_", " ").title(),
            generacion=generacion.replace("_", " ").upper(),
            meme=meme,
            cancion=CancionModel(**cancion),  # Convertimos el dict en el modelo
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

@app.get("/test-memes")
async def test_memes():
    """Endpoint para probar que los memes se están sirviendo correctamente"""
    return MEMES
# Para ejecutar: uvicorn main:app --reload