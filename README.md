# Motor Base de Orientación Vocacional (PE2)

Núcleo de inferencia y validación estructurada para el sistema de asistencia en **Orientación Vocacional y Ocupacional** (triangulación de puntajes CHASIDE y notas de admisión clínica).

Trabajo práctico correspondiente a la **Pre-entrega 2 (PE2)** del programa *Forward Deployed Engineer*.

---

## 1. Requisitos Previos

- **Python**: 3.10 o superior (recomendado 3.12).
- **Git**.
- Clave de API de **OpenAI** o **Anthropic**.

---

## 2. Guía de Ejecución desde Clon Limpio

Abrí una terminal y ejecutá los siguientes pasos:

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/moka-web/fde-orientacion-vocacional.git
cd fde-orientacion-vocacional
```

### Paso 2: Crear y activar entorno virtual

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno
Copiá el archivo `.env.example` como `.env`:

**En Windows:**
```powershell
copy .env.example .env
```

**En Linux / macOS:**
```bash
cp .env.example .env
```

Editá `.env` con tu editor preferido y cargá tu clave de API:
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

### Paso 5: Ejecutar el motor
```bash
python src/motor.py
```

El script ejecutará el banco de 5 consultas de prueba (incluyendo casos borde y fuera de dominio), imprimirá las trazas de validación en tiempo real y mostrará la tabla consolidada de tokens, costos y latencias.

---

## 3. Arquitectura del Contrato de Datos (Pydantic v2)

### Entrada (`Entrada`)
- `paciente_id` (`str`): Formato anonimizado validado por regex (`^PAC_\d{3,6}$`).
- `edad` (`int`): Rango etario válido entre 15 y 60 años (`ge=15`, `le=60`).
- `notas_admision` (`str`): Anotaciones clínicas iniciales con longitud mínima de 20 caracteres.
- `puntajes_chaside` (`dict[str, int]`): Mapeo de las 7 áreas CHASIDE (`C`, `H`, `A`, `S`, `I`, `D`, `E`) con puntajes en el rango `0..98`.

### Salida (`Salida`)
- `motivo_consulta` (`str`): Síntesis del motivo de consulta (mínimo 10 caracteres).
- `rasgos_personalidad` (`list[str]`): Lista con al menos 2 rasgos predominantes inferidos.
- `area_predominante` (`AreaCHASIDE` Enum): Una de las 7 áreas vocacionales estandarizadas.
- `carreras_sugeridas` (`list[str]`): Entre 2 y 5 alternativas académicas vinculadas.
- `hipotesis_clinica` (`str`): Devolución redactada en tono no categórico ("hipótesis de trabajo"), cumpliendo los guardrails éticos del caso.

---

## 4. Manejo de Errores y Resiliencia

1. **Validación fallida**: Si el modelo retorna un esquema incompleto o fuera de regla, se captura el `ValidationError` de Pydantic, se identifica exactamente qué campo falló y se realiza **1 reintento** inyectando el feedback del error en el prompt.
2. **Excepciones de API**: Se capturan caídas de red, problemas de autenticación o límites de cuota (`RateLimitError`, `APIConnectionError`), retornando un objeto de error estructurado sin romper la ejecución.

---

## 5. Estructura del Repositorio

```text
fde-orientacion-vocacional/
├── .env.example          # Plantilla de variables sin secretos
├── .gitignore            # Ignora .env, .venv y caches
├── README.md             # Instrucciones de ejecución
├── requirements.txt      # Dependencias versionadas
└── src/
    └── motor.py          # Contrato Pydantic, llamadas al LLM y mediciones
```
