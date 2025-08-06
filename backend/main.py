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

class memeModel(BaseModel):
    id: str
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
    meme: memeModel
    cancion: CancionModel
    mensaje_motivacional: str

# Base de datos en memoria (luego podemos expandir)
MEMES = {
    "bajo_peso": [
        {"id": "1", "url": "https://tse1.explicit.bing.net/th/id/OIP.Y4HQsmmx7hFO0wg6nxBndAHaEK?r=0&cb=thfvnext&rs=1&pid=ImgDetMain&o=7&rm=3"},
        {"id": "2", "url": "https://images3.memedroid.com/images/UPLOADED67/5f32e45c441cb.jpeg"},
        {"id": "3", "url": "https://th.bing.com/th/id/R.086dbb7aac296f9ef116edca95085571?rik=QGPtsPerVMAxhg&riu=http%3a%2f%2fimg.desmotivaciones.es%2f201104%2fflaco.jpg&ehk=yS7Jc5tXGiwmaCShKh%2fFRXC1Z4dDAc2pUjarG1%2fbf2A%3d&risl=&pid=ImgRaw&r=0"},
        {"id": "4", "url": "https://i.pinimg.com/originals/12/c4/85/12c485bc197d4108091d532ecb632177.jpg"},
        {"id": "5", "url": "https://de.toonpool.com/user/30065/files/angel_1440585.jpg"},
        {"id": "6", "url": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3dc557ad-2f57-47ae-af44-9b5be08f9618/d6t5x0y-642c30f1-ddfa-4ca5-9c20-4cd6f4f4f0ed.png/v1/fill/w_1600,h_2682/gotenks_flaco_by_edicionesz3000_d6t5x0y-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MjY4MiIsInBhdGgiOiJcL2ZcLzNkYzU1N2FkLTJmNTctNDdhZS1hZjQ0LTliNWJlMDhmOTYxOFwvZDZ0NXgweS02NDJjMzBmMS1kZGZhLTRjYTUtOWMyMC00Y2Q2ZjRmNGYwZWQucG5nIiwid2lkdGgiOiI8PTE2MDAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.Wu05f67eFD-1H7fOa9bugxWVqaL1VYlLhMyar0iH3k0"},
        {"id": "7", "url": "https://editorialtelevisa.brightspotcdn.com/dims4/default/f449c94/2147483647/strip/true/crop/1300x732+0+123/resize/2000x1126!/quality/90/?url=https:%2F%2Fk2-prod-editorial-televisa.s3.us-east-1.amazonaws.com%2Fbrightspot%2F66%2Fd1%2Fc3730328464389c185e9f7aa66ba%2Fdon-ramon.jpg"}
       
    ],
    "normal": [
        {"id": "1", "url": "https://www.descargarstickers.com/src_img/2021/06/229092.png"},
        {"id": "2", "url": "https://content.imageresizer.com/images/memes/giga-chad-meme-2.jpg"},
        {"id": "3", "url": "https://i.ytimg.com/vi/44Ys70LUoaY/hqdefault.jpg"},
        
    ],
    "sobrepeso": [
        {"id": "1", "url": "https://i.pinimg.com/originals/4a/ff/24/4aff24d54648d111811896ae08789b37.jpg"},
        {"id": "2", "url": "https://elcomercio.pe/resizer/NAsXKTfR1BLDRcmQGtyAPn-kM7g=/1200x900/smart/filters:format(jpeg):quality(75)/arc-anglerfish-arc2-prod-elcomercio.s3.amazonaws.com/public/ORV5KBDO7NCSFJJCR6N6SFH46Y.jpg"},
        {"id": "3", "url": "https://i.pinimg.com/originals/7a/93/72/7a9372bdb0eb16936230eec6d3d4fc2f.jpg"},
        {"id": "4", "url": "https://cdn.verbub.com/images/y-como-vas-con-la-dieta-97779.jpg"},
        {"id": "5", "url": "https://cdn.memegenerator.es/imagenes/memes/full/31/78/31781146.jpg"},
        {"id": "6", "url": "https://cdn2.actitudfem.com/media/files/media/files/meme-comida-1.jpg"},
    ],
    "obesidad": [
        {"id": "1", "url": "https://http2.mlstatic.com/D_NQ_NP_994628-MLM76997310240_062024-O.webp"},
        {"id": "2", "url": "https://i.pinimg.com/originals/8b/1c/4d/8b1c4d3f4f4f4f4f4f4f4f4f4f4f4f4f.jpg"},
        {"id": "3", "url": "https://i.pinimg.com/originals/9c/2d/5e/9c2d5e6f7f8f9fa0b0b0b0b0b0b0b0b0.jpg"},
        {"id": "4", "url": "https://i.pinimg.com/originals/ad/3e/1f/ad3e1f2f3f4f5f6f7f8f9fa0b0b0b0b0.jpg"},
        {"id": "5", "url": "https://i.pinimg.com/originals/bd/4e/2c/bd4e2c3d4e5f6f7f8f9fa0b0b0b0b0b0.jpg"},
        {"id": "6", "url": "https://i.pinimg.com/originals/cd/5f/3d/cd5f3d4e5f6f7f8f9fa0b0b0b0b0b0b.jpg"},
    ]
}

COMBINACION_CANCIONES = {
    "femenino_bajo_peso": [
        {
            "titulo": "Jarabe de Palo - La Flaca",
            "youtube_id": "HhZaHf8RP6g",
            "url": "https://youtu.be/r2g0pM3PMNQ?t=21"
        },
        {
            "titulo": "Luis Alberto Spinetta - Flaca",
            "youtube_id": "tZkouut-9RQ",
            "url": "https://youtu.be/UCF9oHXhDMU?t=26"
        }
    ],

    "femenino_obesidad": [
        {
             "titulo": "Oye Gelda",
            "youtube_id": "9Z0hmnHnRR8",
            "url": "https://youtu.be/KhnqGEPyBUg?t=8"
            
        },
    ],
    "femenino_sobrepeso": [
         {
            "titulo": "Meghan Trainor - All About That Bass",
            "youtube_id": "7PCkvCPvDXk",
            "url": "https://www.youtube.com/watch?v=7PCkvCPvDXk"
        }

    ],

    "masculino_obesidad": [
        {
            "titulo": "megapanza - i love roquefort",
            "youtube_id": "9Z0hmnHnRR8",
            "url": "https://youtu.be/UW1DjRSuU4g?t=102"
        },
        {
            "titulo": "Megapanza - yo como lechon",
            "youtube_id": "wnJ6LuUFoAw",  
            "url": "https://youtu.be/UW1DjRSuU4g?t=124"
        }


    ],
    
    "masculino_bajo_peso": [
        {
            "titulo": "Mon Laferte - flaco",
            "youtube_id": "CRsXwuuQbao",
            "url": "https://youtu.be/BtZlp9V7Woc?t=68"
        }],
    "masculino_bajo_peso_boomer":[
        {
            "titulo": "Luis Aguile - amor de flacos",
            "youtube_id": "JGwWNGJdvx8",
            "url": "https://youtu.be/2a4OK5M1B_c?t=14"
        }
    ],
    "masculino_sobrepeso": [
       {
            "titulo": "Somewhere over the Rainbow - Israel IZ Kamakawiwoole",
            "youtube_id": "kpSFE88dCQ8",
            "url": "https://youtu.be/V1bFr2SWP1I?t=17"
        },
        {
            "titulo": "skibidi doo",
            "youtube_id": "5F4wZWfSdD8",
            "url": "https://youtu.be/s4wTiYJeA68"
        },
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

         # Lógica de selección de canción con sistema de prioridades:
        # 1. MÁXIMA PRIORIDAD: Easter eggs (género + IMC + generación)
        
        # 2. PRIORIDAD BAJA: Canciones normales por generación
        
        cancion = None
        
        # 1. Buscar combinacion específica
        easter_egg_key = f"{user_data.sexo}_{categoria_imc}_{generacion}"
        if easter_egg_key in COMBINACION_CANCIONES:
            cancion = random.choice(COMBINACION_CANCIONES[easter_egg_key])
          
        
        # Si no hay combinacion específica, buscar por generacion
        
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

# Para ejecutar: uvicorn main:app --reload