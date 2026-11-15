from enum import Enum
from pydantic import BaseModel, Field 

# Basemodel es para los datos de entrada y salida de la API
#field es para ponerle un alias a los campos de la clase, para que no se vea el nombre del campo en la respuesta de la API

# chaside este enum es para los campos de la clase que son de tipo string y tienen un conjunto limitado de valores posibles, en este caso los valores posibles son C, H, A, S, I, D y E.

class Chaside(str, Enum):
    C = "C"  # administrativas y contables   
    H = "H"  # humanas y sociales
    A = "A"  # artísticas y culturales
    S = "S"  # salud y ciencia
    I = "I"  # ingenierías y tecnología
    D = "D"  # defensa y seguridad 
    E = "E"  # exactas y naturales

# datos de entrada 
    
class CasoClinico (BaseModel): 
    paciente_id: str = Field(
        ...,
        pattern=r"^PAC_\d{3,6}$",
        description="Identificador anonimizado del paciente (ej: PAC_101)"
    )
    edad: int = Field(
        ...,
        ge=15,
        le=60,
        description="Edad del consultante dentro del rango permitido"
    )
    notas_admision: str = Field(
        ...,
        min_length=20,
        description="Anotaciones cualitativas de la entrevista inicial"
    )
    puntajes_chaside: dict[str, int] = Field(
        ...,
        description="Puntajes brutos obtenidos en cada área (0 a 98)"
    )


# datos de salida

class InformePreliminar(BaseModel):
    paciente_id: str = Field(
        ...,
        pattern=r"^PAC_\d{3,6}$",
        description="Identificador anonimizado del paciente (debe coincidir con la entrada)"
    )
    estado: str = Field(
        default="BORRADOR_PENDIENTE_AUDITORIA",
        description="Estado de gobernanza clínica del informe"
    )
    motivo_consulta: str = Field(
        ...,
        min_length=10,
        description="Síntesis clínica del motivo de consulta del paciente"
    )
    rasgos_personalidad: str = Field(
    ...,
    min_length=50,
    description="Párrafo narrativo y descriptivo sobre el estilo cognitivo, afectivo y conductual del consultante"
    )
    area_predominante: Chaside = Field(
        ...,
        description="Área vocacional principal inferida del test CHASIDE"
    )
    carreras_sugeridas: list[str] = Field(
        ...,
        min_length=2,
        max_length=5,
        description="Entre 2 y 5 alternativas académicas vinculadas al perfil"
    )
    hipotesis_clinica: str = Field(
        ...,
        min_length=30,
        description="Devolución tentativa en tono de hipótesis de trabajo, no categórica"
    )


