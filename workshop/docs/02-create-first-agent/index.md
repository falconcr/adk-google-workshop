# 🏆 Módulo 2: Creando tu Primer Agente con ADK

En este módulo aprenderás a construir tu primer agente conversacional usando Google ADK. Crearemos un agente especializado en responder preguntas sobre la Copa Mundial de la FIFA, utilizando Gemini 2.0 Flash como modelo base.

## 🎯 ¿Qué construiremos?

Un agente inteligente que puede responder preguntas como:

- "¿Quién ganó la Copa del Mundo de 2014?"
- "¿Cuántos goles anotó Messi en 2022?"
- "¿Qué país tiene más Copas del Mundo?"
- "Cuéntame algo interesante sobre Ronaldo" (modo diversión con easter eggs)

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener:

1. **Python 3.9+** instalado
2. **Google ADK** instalado (`pip install google-adk`)
4. **Conocimientos básicos** de Python

# Un poco de teoria

Perfecto. A continuación te presento una **introducción teórica** clara y ordenada que puedes usar al comienzo del episodio para contextualizar el proyecto. Esta sección explica qué es un agente, qué es el modelo **Gemini 2.0 Flash**, y cómo se conecta todo con el framework **Google ADK**.

---

## 🎓 Introducción Teórica: ¿Qué es el FIFA World Cup Agent?

Antes de entrar en la implementación, es importante entender **qué tecnologías hay detrás** de este agente y **por qué fueron elegidas**.

---

### 🤖 ¿Qué es un agente inteligente?

Un **agente inteligente** es un programa que puede recibir información, procesarla, tomar decisiones y responder de forma autónoma, como si tuviera “sentido común” dentro de un dominio específico.

En este caso, el agente está diseñado para ser experto en **todo lo relacionado con la Copa Mundial de la FIFA**, desde datos históricos hasta estadísticas avanzadas y curiosidades.

---

### 🧠 ¿Qué es Gemini 2.0 Flash?

Gemini 2.0 Flash es un modelo de lenguaje desarrollado por Google, parte de la familia Gemini (antes Bard). Estos modelos están entrenados con **billones de datos** y son capaces de:

* Entender preguntas en lenguaje natural
* Generar respuestas coherentes, útiles y detalladas
* Recordar hechos históricos, estadísticas y eventos complejos

La variante **Flash** está optimizada para ser más **rápida y ligera**, ideal para tareas interactivas como las de este agente. Se usa como el "cerebro" del sistema, respondiendo a preguntas como:

* “¿Quién ganó el Mundial de 2014?”
* “¿Cuántos goles hizo Messi en Qatar 2022?”
* “Cuéntame una curiosidad de Brasil en los Mundiales”

---


## ✅ Uso correcto de **Pydantic**

**¿Qué es Pydantic?**
Es una librería de Python que ayuda a definir y validar datos fácilmente usando clases. Se usa mucho cuando quieres que tu código sea **más robusto, predecible y limpio**, especialmente al trabajar con configuraciones o modelos de datos.


**En ADK**, los agentes heredan de una clase que internamente usa Pydantic. Esto quiere decir que:

* Todo lo que definas dentro del agente **debe cumplir con reglas de Pydantic**.
* No puedes agregar atributos al azar después de crear el objeto, a menos que los definas como **privados** (con `_` al inicio) o como **campos válidos**.

**Por eso usamos `_fifa_tools` y no `fifa_tools`**:

```python
self._fifa_tools = FIFATools()  # ✅ correcto (Pydantic no se queja)
self.fifa_tools = FIFATools()   # ❌ da error porque no es un campo válido
```

## 🏗️ Resumen de Arquitectura

```
┌────────────────────────────────────────────────────────────┐
│                 Agente Copa Mundial FIFA                   │
├────────────────────────────────────────────────────────────┤
│  ┌────────────────┐    ┌────────────────┐                 │
│  │ FIFAWorldCup   │    │ FIFATools      │                 │
│  │ Agent (agente) │◄───┤ Herramientas   │                 │
│  └────────────────┘    └────────────────┘                 │
│         │                      │                           │
│         ▼                      ▼                           │
│  ┌────────────────┐    ┌────────────────┐                 │
│  │ Gemini 2.0     │    │ Sistema de     │                 │
│  │ Flash (modelo) │    │ Activación     │                 │
│  │                │    │ de Conocimiento│                 │
│  └────────────────┘    └────────────────┘                 │
├────────────────────────────────────────────────────────────┤
│             Framework de Google ADK                        │
│  ┌────────────────┐    ┌────────────────┐                 │
│  │ LlmAgent       │    │ BaseAgent      │                 │
│  │ (clase base)   │    │ (Pydantic)     │                 │
│  └────────────────┘    └────────────────┘                 │
└────────────────────────────────────────────────────────────┘
```

---


## 🧩 ¿Cómo se conectan todas estas piezas?

Aquí está el resumen simple:

| Componente                                 | Rol en el agente                                        |
| ------------------------------------------ | ------------------------------------------------------- |
| **Gemini 2.0 Flash**                       | Provee el conocimiento (modelo de lenguaje)             |
| **Google ADK**                             | Orquesta todo (framework de desarrollo)                 |
| **Herramientas internas (`FIFATools`)**    | Activan conocimiento específico sin APIs externas       |
| **Clase del agente (`FIFAWorldCupAgent`)** | Define cómo responde el sistema y qué herramientas usar |

---



## 🚀 Paso 1: Configuración del Entorno

### 1.1 Crear el entorno virtual

```bash
# Crear entorno virtual
python -m venv venv-fifa-agent

# Activar entorno (Linux/Mac)
source venv-fifa-agent/bin/activate

# Activar entorno (Windows)
venv-fifa-agent\Scripts\activate
```

### 1.2 Instalar dependencias

```bash
pip install google-adk
pip install google-cloud-aiplatform
```

### 1.3 Configurar autenticación

Tienes dos opciones para autenticarte:

**Opción A: Usar API Key (Recomendado para desarrollo)**

```bash
# Configurar tu API key como variable de entorno
export GOOGLE_API_KEY="<key>"

# Para Windows
set GOOGLE_API_KEY=<key>
```

**Opción B: Usar Google Cloud SDK**

```bash
# Configurar credenciales de Google Cloud
gcloud auth application-default login

# Verificar proyecto
gcloud config get-value project
```


## 📁 Estructura del Código

```
fifa_agent/
├── __init__.py          # Inicialización del paquete para ADK Web
├── agent.py             # Clase principal del agente
├── config.py            # Configuraciones y constantes
├── fifa_tools.py        # Herramientas para activar conocimiento
└── README.md            # Documentación del proyecto
```

---

## 🔍 Explicación Paso a Paso

### 1. Capa de Configuración (`config.py`)

Administra centralmente todas las configuraciones, soportando variables de entorno:

```python
MODEL_CONFIG = {
    "model_name": "gemini-2.0-flash",
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
    "api_key": os.getenv("GOOGLE_API_KEY"),
    "location": "us-central1",
    "temperature": 0.7,
    "max_output_tokens": 1000,
}
```

* Compatible con API key o Project ID
* Parámetros ajustados para respuestas fiables

---

### 2. Sistema de Activación de Conocimiento (`fifa_tools.py`)

Este módulo no hace peticiones externas. En su lugar, activa el conocimiento interno del modelo Gemini:

```python
async def search_world_cup_info(self, query: str, year: Optional[int] = None) -> Dict[str, Any]:
    return {
        "action": "use_gemini_knowledge",
        "query": query,
        "year": year,
        "instruction": "Usa tu conocimiento interno sobre la Copa del Mundo..."
    }
```

**Ventajas**:

* Respuestas más rápidas
* Sin dependencia externa
* Sin costos adicionales de APIs
* Basado en el entrenamiento de Gemini

---

### 3. Clase Principal del Agente (`agent.py`)

Orquesta toda la funcionalidad del agente. El flujo de inicialización es:

1. Configura el modelo Gemini
2. Aplica autenticación flexible
3. Inicializa el modelo
4. Llama al constructor de la clase padre (`LlmAgent`)
5. Carga las herramientas (`FIFATools`)
6. Registra las herramientas en el framework

Cada herramienta se define así:

```python
async def search_world_cup_info(self, query: str, year: Optional[int] = None) -> Dict[str, Any]:
    return await self._fifa_tools.search_world_cup_info(query, year)
```

---

### 4. Modos de Ejecución

#### a. Modo CLI (interactivo por consola)

```python
async def main():
    agent = FIFAWorldCupAgent()
    while True:
        query = input("👤 Tu pregunta: ").strip()
        response = await agent.run(query, context)
        print(f"🏆 Agente: {response}\n")
```

#### b. Modo Web con ADK

```python
def get_agent():
    return FIFAWorldCupAgent()

root_agent = get_agent()
```

---

## 🚀 Buenas Prácticas Aplicadas

* ✅ Uso correcto de `Pydantic`
* ✅ Registro de herramientas con `self.tools.extend()`
* ✅ Separación clara entre configuración, lógica y herramientas
* ✅ Métodos asíncronos para consistencia
* ✅ Soporte bilingüe (respuestas en español)
* ✅ Código organizado y documentado


## 💡 Ejemplos de Uso

### Preguntas Básicas

```
👤 ¿Quién ganó el Mundial de 2018?
🏆 Francia ganó la Copa del Mundo de 2018...

👤 ¿Cuántos goles hizo Pelé en Mundiales?
🏆 Pelé anotó 12 goles en 4 Copas del Mundo...

👤 ¿Qué país tiene más títulos?
🏆 Brasil lidera con 5 títulos mundiales...
```

### Consultas Avanzadas

```
👤 Cuéntame sobre la final de 2022
🏆 La final entre Argentina y Francia fue histórica...

👤 ¿Qué records tiene Messi?
🏆 Lionel Messi ha logrado varios récords en Copas...

👤 Datos curiosos sobre Brasil
🏆 Brasil es el único país que ha jugado todos los mundiales...
```

---

## 🌍 Variables de Entorno

| Variable               | Obligatoria | Descripción                     | Ejemplo           |
| ---------------------- | ----------- | ------------------------------- | ----------------- |
| `GOOGLE_API_KEY`       | Opcional\*  | Clave API para Gemini           | `AIza...`         |
| `GOOGLE_CLOUD_PROJECT` | Opcional\*  | ID del proyecto en Google Cloud | `mi-proyecto-123` |

\*Una de las dos es requerida.



## 🔧 Personalización

### Agregar nuevas herramientas

1. En `FIFATools`:

```python
async def nueva_funcion(self, parametro: str) -> Dict[str, Any]:
    return {
        "action": "use_gemini_knowledge",
        "instruction": "Instrucción personalizada para Gemini"
    }
```

2. En `FIFAWorldCupAgent`:

```python
async def nueva_funcion(self, parametro: str) -> Dict[str, Any]:
    return await self._fifa_tools.nueva_funcion(parametro)
```

3. Registra la nueva herramienta:

```python
self.tools.extend([
    self.nueva_funcion
])
```

### Cambiar el comportamiento del agente

Edita `SYSTEM_PROMPT` en `config.py` para modificar el tono, objetivos o restricciones del agente.

---

## 📄 Licencia

Este proyecto es una demostración del uso del Google Agent Development Kit (ADK) y sigue las buenas prácticas recomendadas por Google Cloud AI.

---

¿Deseas que convierta este contenido en un script narrativo listo para grabación?

## 🧠 Paso 3: Configurar Herramientas para Gemini

En lugar de usar datos hardcodeados, vamos a crear herramientas que **Gemini Flash 2.0** usará para obtener información dinámica. Gemini será quien decida cuándo y cómo usar estas herramientas:

```python
# fifa_tools.py

import requests
from typing import Dict, Any, Optional
import json

class FIFATools:
    """Herramientas que Gemini usa para obtener información de la Copa del Mundo"""
    
    def __init__(self):
        # Gemini usará su conocimiento interno combinado con estas herramientas
        pass
    
    async def search_world_cup_info(self, query: str, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Permite a Gemini buscar información específica sobre Mundiales.
        
        Args:
            query: Consulta específica (ej: "ganador", "goleador", "final")
            year: Año del Mundial (opcional)
            
        Returns:
            Instrucción para que Gemini use su conocimiento interno
        """
        return {
            "action": "use_gemini_knowledge",
            "query": query,
            "year": year,
            "instruction": "Usa tu conocimiento interno sobre la Copa del Mundo para responder esta consulta específica"
        }
    
    async def get_player_statistics(self, player_name: str, context: str = "world_cup") -> Dict[str, Any]:
        """
        Permite a Gemini proporcionar estadísticas de jugadores.
        
        Args:
            player_name: Nombre del jugador
            context: Contexto (ej: "world_cup", "career", "specific_year")
            
        Returns:
            Instrucción para que Gemini use su conocimiento interno
        """
        return {
            "action": "use_gemini_knowledge",
            "player": player_name,
            "context": context,
            "instruction": "Proporciona estadísticas detalladas de este jugador en Copas del Mundo usando tu conocimiento interno"
        }
    
    async def get_country_performance(self, country: str) -> Dict[str, Any]:
        """
        Permite a Gemini proporcionar información sobre el rendimiento de países.
        
        Args:
            country: Nombre del país
            
        Returns:
            Instrucción para que Gemini use su conocimiento interno
        """
        return {
            "action": "use_gemini_knowledge",
            "country": country,
            "instruction": "Proporciona información completa sobre el rendimiento de este país en Copas del Mundo"
        }
    
    async def get_fun_facts(self, topic: str = "general") -> Dict[str, Any]:
        """
        Permite a Gemini compartir datos curiosos sobre la Copa del Mundo.
        
        Args:
            topic: Tema específico (ej: "records", "history", "players")
            
        Returns:
            Instrucción para que Gemini use su conocimiento interno
        """
        return {
            "action": "use_gemini_knowledge",
            "topic": topic,
            "instruction": "Comparte datos curiosos e interesantes sobre la Copa del Mundo relacionados con este tema"
        }
```

## ⚙️ Paso 4: Configuración del Agente

Crea el archivo de configuración:

```python
# config.py

import os

# Configuración del modelo
MODEL_CONFIG = {
    "model_name": "gemini-2.0-flash-exp",
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),  # Solo si usas gcloud
    "api_key": os.getenv("GOOGLE_API_KEY"),          # Para API key
    "location": "us-central1",
    "temperature": 0.7,
    "max_output_tokens": 1000,
}

# Configuración del agente
AGENT_CONFIG = {
    "name": "FIFA World Cup Expert",
    "description": "Experto en Copa Mundial de la FIFA con conocimientos actualizados y datos curiosos",
    "version": "1.0.0",
}

# Prompt del sistema
SYSTEM_PROMPT = """
Eres un experto en la Copa Mundial de la FIFA con acceso a herramientas especializadas.

HERRAMIENTAS DISPONIBLES:
- search_world_cup_info(query, year): Busca información específica sobre Mundiales
- get_player_statistics(player, context): Obtiene estadísticas de jugadores
- get_country_performance(country): Información sobre rendimiento por país
- get_fun_facts(topic): Datos curiosos sobre temas específicos

INSTRUCCIONES IMPORTANTES:
1. **TU CONOCIMIENTO ES LA FUENTE PRINCIPAL**: Usa tu conocimiento interno sobre la Copa del Mundo como fuente principal de información
2. **Las herramientas son activadores**: Cuando se llame a una herramienta, úsala como señal para activar tu conocimiento interno sobre ese tema
3. **Respuestas completas y precisas**: Proporciona información detallada, estadísticas exactas y contexto histórico
4. **Combina información**: Mezcla datos específicos con contexto histórico y datos curiosos
5. **Respuestas conversacionales**: Mantén un tono amigable y educativo

EJEMPLOS DE USO:
- "¿Quién ganó en 2014?" → usar search_world_cup_info("ganador", 2014) + proporcionar contexto completo
- "¿Cuántos goles hizo Messi en 2022?" → usar get_player_statistics("Messi", "world_cup") + detalles del torneo
- "¿Qué país tiene más Mundiales?" → usar get_country_performance() + ranking histórico
- "Cuéntame sobre Ronaldo" → usar get_player_statistics("Ronaldo") + get_fun_facts("players")

¡Proporciona información rica y detallada usando tu conocimiento interno!
"""
```

## 🤖 Paso 5: Implementar el Agente

Ahora vamos a crear el agente principal. **La clave está en que Gemini es quien decide cuándo y cómo usar las herramientas**:

### 🔑 Diferencia Clave: Gemini Flash 2.0 como Fuente Principal

❌ **Enfoque incorrecto**: Hardcodear respuestas y limitar a Gemini
✅ **Enfoque correcto**: Gemini Flash 2.0 usa su conocimiento interno + herramientas como activadores

Nuestro agente funciona así:
1. **Usuario hace pregunta** → Gemini Flash 2.0 recibe la pregunta
2. **Gemini analiza** → Decide si necesita activar herramientas específicas
3. **Herramientas como activadores** → Señalan a Gemini qué tipo de información proporcionar
4. **Gemini responde** → Usa su conocimiento interno para dar respuestas completas y precisas

```python
# agent.py

import asyncio
from typing import Dict, Any, Optional
from google.adk import Agent, AgentConfig, Model
from google.adk.core import Context
from fifa_tools import FIFATools
from config import MODEL_CONFIG, AGENT_CONFIG, SYSTEM_PROMPT

class FIFAWorldCupAgent(Agent):
    """Agente especializado en Copa Mundial de la FIFA que usa Gemini Flash 2.0 como fuente principal"""
    
    def __init__(self):
        # Configurar el modelo
        model_kwargs = {
            "model_name": MODEL_CONFIG["model_name"],
            "location": MODEL_CONFIG["location"],
            "temperature": MODEL_CONFIG["temperature"],
            "max_output_tokens": MODEL_CONFIG["max_output_tokens"]
        }
        
        # Usar API key o project_id según lo disponible
        if MODEL_CONFIG["api_key"]:
            model_kwargs["api_key"] = MODEL_CONFIG["api_key"]
        elif MODEL_CONFIG["project_id"]:
            model_kwargs["project_id"] = MODEL_CONFIG["project_id"]
        
        model = Model(**model_kwargs)
        
        # Configurar el agente
        config = AgentConfig(
            name=AGENT_CONFIG["name"],
            description=AGENT_CONFIG["description"],
            version=AGENT_CONFIG["version"],
            system_prompt=SYSTEM_PROMPT
        )
        
        super().__init__(config=config, model=model)
        
        # Inicializar herramientas
        self.fifa_tools = FIFATools()
        
        # Registrar herramientas que Gemini puede usar
        self.register_tool(self.search_world_cup_info)
        self.register_tool(self.get_player_statistics)
        self.register_tool(self.get_country_performance)
        self.register_tool(self.get_fun_facts)
    
    async def search_world_cup_info(self, query: str, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Permite a Gemini buscar información específica sobre Mundiales.
        
        Args:
            query: Consulta específica (ej: "ganador", "goleador", "final")
            year: Año del Mundial (opcional)
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self.fifa_tools.search_world_cup_info(query, year)
    
    async def get_player_statistics(self, player_name: str, context: str = "world_cup") -> Dict[str, Any]:
        """
        Permite a Gemini proporcionar estadísticas de jugadores.
        
        Args:
            player_name: Nombre del jugador
            context: Contexto (ej: "world_cup", "career", "specific_year")
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self.fifa_tools.get_player_statistics(player_name, context)
    
    async def get_country_performance(self, country: str) -> Dict[str, Any]:
        """
        Permite a Gemini proporcionar información sobre el rendimiento de países.
        
        Args:
            country: Nombre del país
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self.fifa_tools.get_country_performance(country)
    
    async def get_fun_facts(self, topic: str = "general") -> Dict[str, Any]:
        """
        Permite a Gemini compartir datos curiosos sobre la Copa del Mundo.
        
        Args:
            topic: Tema específico (ej: "records", "history", "players")
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self.fifa_tools.get_fun_facts(topic)

async def main():
    """Función principal para probar el agente"""
    agent = FIFAWorldCupAgent()
    
    # Contexto básico
    context = Context()
    
    print("🏆 FIFA World Cup Agent - ¡Pregúntame sobre la Copa del Mundo!")
    print("Ejemplos: '¿Quién ganó en 2014?', '¿Cuántos goles hizo Messi en 2022?', '¿Qué país tiene más Mundiales?'")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            query = input("👤 Tu pregunta: ").strip()
            
            if query.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if not query:
                continue
            
            print("🤖 Gemini está procesando tu pregunta...")
            # Ahora Gemini decide si usar herramientas y cómo responder
            response = await agent.run(query, context)
            print(f"🏆 Agente: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Paso 6: Archivo de Dependencias

Crea el archivo `requirements.txt`:

```txt
google-adk>=0.1.0
google-cloud-aiplatform>=1.38.0
```

## 🚀 Paso 7: Ejecutar el Agente


### 7.1 Opción A: Ejecutar con ADK Web (Recomendado)

ADK Web proporciona una interfaz visual para probar agentes de forma más cómoda:

```bash
# Ejecutar ADK Web
adk web

# O especificar el archivo del agente
adk web agent.py
```

Esto abrirá una interfaz web en `http://localhost:8080` donde podrás:
- 🗨️ Chatear con tu agente en tiempo real
- 🔍 Ver las llamadas a herramientas en detalle
- 📊 Monitorear el rendimiento del agente
- 🐛 Debuggear problemas fácilmente

### 7.2 Opción B: Ejecutar en línea de comandos

```bash
python agent.py
```


## 🧪 Paso 8: Pruebas de Ejemplo

Prueba tu agente con estas preguntas y observa cómo **Gemini decide usar las herramientas**:

### 🔍 Qué observar durante las pruebas (en ADK Web):

1. **"¿Quién ganó la Copa del Mundo de 2014?"**
   - En ADK Web verás: Gemini llama a `search_world_cup_info("ganador", 2014)`
   - Respuesta: Gemini proporciona información completa sobre Alemania vs Argentina, detalles del torneo, estadísticas y contexto histórico

2. **"¿Cuántos goles anotó Messi en 2022?"**
   - En ADK Web verás: Gemini llama a `get_player_statistics("Messi", "world_cup")`
   - Respuesta: Gemini proporciona estadísticas detalladas de Messi en Qatar 2022, incluyendo goles, asistencias, partidos y logros

3. **"¿Qué país tiene más Copas del Mundo?"**
   - En ADK Web verás: Gemini llama a `get_country_performance()` para varios países
   - Respuesta: Gemini proporciona ranking completo con Brasil (5), Alemania (4), Italia (4), etc., con contexto histórico

4. **"Cuéntame algo interesante sobre Ronaldo"**
   - En ADK Web verás: Gemini llama a `get_player_statistics("Ronaldo")` Y `get_fun_facts("players")`
   - Respuesta: Gemini proporciona estadísticas completas de Ronaldo en Mundiales + datos curiosos sobre su carrera

### 🎯 Ventajas de probar con ADK Web:

- **Visualización de herramientas** → Ves exactamente qué función llama Gemini
- **Tiempo de respuesta** → Monitor del rendimiento en tiempo real
- **Debugging visual** → Identificar problemas fácilmente
- **Interfaz amigable** → Mejor experiencia que la línea de comandos
- **Logs detallados** → Historial completo de conversaciones

### 🎯 Comportamiento esperado:

- **Gemini lee la pregunta** → Decide qué herramientas usar como activadores
- **Respuestas naturales** → Información completa y conversación fluida
- **Conocimiento interno** → Gemini usa su amplio conocimiento sobre fútbol y Mundiales
- **Información dinámica** → Respuestas actualizadas y precisas sin limitaciones de datos hardcodeados

## 🎯 Paso 9: Mejoras Opcionales

### 9.1 Agregar más datos

Expande `fifa_knowledge.py` con:
- Más años de Mundiales
- Estadísticas de más jugadores
- Récords adicionales

### 9.2 Mejorar el procesamiento

- Usar NLP para mejor comprensión de consultas
- Implementar búsqueda difusa para nombres
- Agregar soporte para múltiples idiomas

### 9.3 Tips para usar ADK Web eficientemente

**🔧 Configuración recomendada:**

```python
# Para mejor debugging en ADK Web, añade logging
import logging

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class FIFAWorldCupAgent(Agent):
    def __init__(self):
        super().__init__(config=config, model=model)
        self.logger = logging.getLogger(__name__)
        
    async def get_world_cup_info(self, year: int) -> Dict[str, Any]:
        self.logger.info(f"Buscando información del Mundial {year}")
        # ... resto del código
```

**🎯 Funcionalidades avanzadas en ADK Web:**

- **Modo debug**: Activa para ver logs detallados
- **Historial de herramientas**: Revisa qué funciones se llamaron
- **Métricas de rendimiento**: Tiempo de respuesta por herramienta
- **Export de conversaciones**: Guarda sesiones para análisis

## 🎉 ¡Felicitaciones!

Has creado tu primer agente con Google ADK. Este agente puede:

✅ Responder preguntas específicas sobre Mundiales
✅ Proporcionar estadísticas de jugadores famosos
✅ Mostrar datos curiosos y easter eggs
✅ Usar herramientas personalizadas para acceder a datos
✅ Procesar consultas en lenguaje natural