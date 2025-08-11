# Lab 3: FIFA Agent con Herramientas Web - ADK Tools en Acción

## 🎯 Objetivo del Laboratorio

Este laboratorio demuestra cómo los agentes de ADK (Agent Development Kit) pueden usar **herramientas (tools)** para expandir sus capacidades más allá del conocimiento base del modelo de lenguaje. Construiremos sobre el FIFA Agent básico añadiendo herramientas de búsqueda web para acceder a información actualizada.

## 🤔 ¿Por qué un Agente Debe Usar Tools?

### Limitaciones de Solo Conocimiento Base

Los modelos de lenguaje como Gemini tienen limitaciones inherentes:

1. **Fecha de corte de conocimiento**: Su información está limitada a una fecha específica
2. **Información estática**: No pueden acceder a datos que cambian constantemente
3. **Especificidad limitada**: Pueden carecer de detalles muy específicos o recientes
4. **Verificación**: No pueden verificar información en tiempo real

### Ventajas de Usar Tools

Las herramientas permiten a los agentes:

- ✅ **Acceder a información actualizada** en tiempo real
- ✅ **Verificar y contrastar** datos con fuentes externas  
- ✅ **Obtener información específica** que el modelo no posee
- ✅ **Realizar acciones** más allá de generar texto
- ✅ **Adaptar respuestas** basadas en datos dinámicos

## 🛠️ Tools Disponibles en ADK

ADK proporciona varios tipos de herramientas que los agentes pueden usar:

### 1. **Herramientas de Búsqueda**
```python
# Búsqueda web genérica
async def search_web_info(self, query: str) -> Dict[str, Any]:
    # Busca información actualizada en internet
```

### 2. **Herramientas de APIs Externas**
```python
# Integración con APIs especializadas
async def get_weather_data(self, location: str) -> Dict[str, Any]:
    # Obtiene datos meteorológicos actuales
```

### 3. **Herramientas de Bases de Datos**
```python
# Consultas a bases de datos
async def query_database(self, sql: str) -> Dict[str, Any]:
    # Ejecuta consultas en bases de datos
```

### 4. **Herramientas de Análisis**
```python
# Procesamiento de datos
async def analyze_document(self, document: str) -> Dict[str, Any]:
    # Analiza documentos o datos complejos
```

### 5. **Herramientas de Acciones**
```python
# Herramientas que realizan acciones
async def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
    # Envía emails u otras acciones
```

## 📚 Implementación del Caso de Uso: FIFA Agent Plus

### Arquitectura del Agente

```
┌─────────────────────────────────────┐
│         FIFAWorldCupAgentPlus       │
├─────────────────────────────────────┤
│                                     │
│  🧠 Gemini 2.0 Flash (Conocimiento  │
│     base sobre fútbol)              │
│                                     │
│  🛠️ Tools Integradas:                │
│    ├── search_world_cup_info()     │
│    ├── get_player_statistics()     │
│    ├── get_country_performance()   │
│    ├── get_fun_facts()            │
│    ├── 🌐 search_web_info()       │ ← NUEVA
│    ├── 📰 get_current_fifa_news() │ ← NUEVA  
│    └── 👤 verify_player_status()  │ ← NUEVA
│                                     │
└─────────────────────────────────────┘
```

### Estrategia de Respuesta Híbrida

El agente usa una estrategia **híbrida** que combina:

1. **Conocimiento interno** (Gemini) como fuente principal
2. **Herramientas web** para información actualizada o específica
3. **Verificación cruzada** entre ambas fuentes

### Ejemplo de Flujo de Decisión

```python
# Pregunta del usuario: \"¿Qué pasó con Messi después del Mundial 2022?\"

if knowledge_cutoff_sufficient(query):
    # Usar solo conocimiento interno
    response = use_internal_knowledge(query)
else:
    # Combinar conocimiento interno + búsqueda web
    internal_info = use_internal_knowledge(query)
    web_info = await search_web_info(query)
    response = combine_sources(internal_info, web_info)
```

## 🚀 Herramientas Implementadas

### 1. **search_web_info()** - Búsqueda Web General
```python
async def search_web_info(self, query: str, max_results: int = 3) -> Dict[str, Any]:
    \"\"\"
    Busca información actualizada en internet usando DuckDuckGo.
    
    Casos de uso:
    - Información posterior a la fecha de corte del modelo
    - Estadísticas muy específicas o recientes
    - Verificación de información controversial
    \"\"\"
```

**Ejemplo de uso:**
- *Pregunta*: \"¿Cómo va la clasificación para el Mundial 2026?\"  
- *Acción*: Busca información actual sobre eliminatorias

### 2. **get_current_fifa_news()** - Noticias FIFA
```python
async def get_current_fifa_news(self, topic: str = \"world cup\") -> Dict[str, Any]:
    \"\"\"
    Obtiene noticias actuales específicas de FIFA.
    
    Casos de uso:
    - Noticias recientes sobre selecciones
    - Actualizaciones de torneos
    - Cambios en reglamentos FIFA
    \"\"\"
```

**Ejemplo de uso:**
- *Pregunta*: \"¿Cuáles son las últimas noticias de la Copa América?\"
- *Acción*: Busca noticias específicas de FIFA sobre el torneo

### 3. **verify_player_current_status()** - Estado de Jugadores  
```python
async def verify_player_current_status(self, player_name: str) -> Dict[str, Any]:
    \"\"\"
    Verifica el estado actual de un jugador específico.
    
    Casos de uso:
    - Club actual del jugador
    - Estado de lesiones
    - Transferencias recientes
    \"\"\"
```

**Ejemplo de uso:**
- *Pregunta*: \"¿En qué club juega actualmente Haaland?\"
- *Acción*: Verifica su club actual y estado

## 🔧 Configuración Técnica

### Dependencias Principales
```txt
google-adk>=0.1.0        # Framework ADK con Google Search nativo
```

### Configuración de Búsqueda Web
```python
WEB_SEARCH_CONFIG = {
    \"search_engine\": \"duckduckgo\",  # Motor sin API key requerida
    \"max_results\": 5,
    \"timeout\": 10,
    \"user_agent\": \"FIFA-Agent-ADK/2.0\",
}
```

## 📊 Comparación: Agente Básico vs Agente Plus

| Característica | FIFA Agent Básico | FIFA Agent Plus |
|---|---|---|
| **Fuente de información** | Solo Gemini | Gemini + Web |
| **Información actualizada** | ❌ Limitada por fecha de corte | ✅ Tiempo real |
| **Verificación de datos** | ❌ No disponible | ✅ Verificación cruzada |
| **Noticias recientes** | ❌ No accesibles | ✅ Búsqueda activa |
| **Estado de jugadores** | ❌ Solo histórico | ✅ Estado actual |
| **Precisión en datos específicos** | ⚠️ Puede ser limitada | ✅ Altamente precisa |

## 🎮 Ejemplos de Casos de Uso

### Caso 1: Información Histórica
**Pregunta**: \"¿Quién ganó la Copa del Mundo de 1998?\"
- **Estrategia**: Usar conocimiento interno (Gemini es suficiente)
- **Tools usadas**: `search_world_cup_info(\"ganador\", 1998)`

### Caso 2: Información Reciente  
**Pregunta**: \"¿Qué equipos se clasificaron para el Mundial 2026?\"
- **Estrategia**: Combinar conocimiento + búsqueda web
- **Tools usadas**: `search_web_info(\"clasificados Mundial 2026\")`

### Caso 3: Estado Actual de Jugador
**Pregunta**: \"¿Messi sigue jugando en el PSG?\"
- **Estrategia**: Verificar estado actual
- **Tools usadas**: `verify_player_current_status(\"Lionel Messi\")`

### Caso 4: Noticias Específicas
**Pregunta**: \"¿Hay novedades sobre el próximo Mundial?\"
- **Estrategia**: Buscar noticias actuales
- **Tools usadas**: `get_current_fifa_news(\"Mundial 2026\")`

## 🚦 Cómo Ejecutar el Lab

### 1. Instalar Dependencias
```bash
cd labs/lab-3-fifa-tools
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
export GOOGLE_API_KEY=\"tu_api_key_aqui\"
# O alternativamente:
# export GOOGLE_CLOUD_PROJECT=\"tu_project_id\"
```

### 3. Ejecutar el Agente
```bash
python agent.py
```

### 4. Probar Diferentes Tipos de Consultas

**Consultas históricas:**
- \"¿Quién ganó en 2018?\"
- \"¿Cuántos goles hizo Pelé en Mundiales?\"

**Consultas actuales:**  
- \"¿Cómo va la clasificación para 2026?\"
- \"¿Qué noticias hay de la FIFA?\"

**Verificación de jugadores:**
- \"¿En qué club juega Mbappé actualmente?\"
- \"¿Cristiano está lesionado?\"

## 🎯 Beneficios Clave del Enfoque con Tools

### 1. **Respuestas Más Precisas**
- Combinación de conocimiento base + datos actuales
- Verificación cruzada de información

### 2. **Mayor Confiabilidad**  
- Fuentes verificables y actualizadas
- Transparencia en el origen de los datos

### 3. **Flexibilidad Adaptativa**
- El agente decide cuándo usar cada herramienta
- Respuesta apropiada según el tipo de consulta

### 4. **Experiencia de Usuario Superior**
- Información siempre actualizada
- Respuestas más completas y contextualizadas

## 🔮 Extensiones Futuras

Este lab puede expandirse con:

- **Herramientas de análisis de video** (highlights, estadísticas visuales)
- **Integración con APIs oficiales** (FIFA, UEFA)
- **Herramientas de predicción** (usando machine learning)
- **Notificaciones push** (actualizaciones automáticas)
- **Herramientas multilingües** (soporte para múltiples idiomas)

## 💡 Conclusión

Este laboratorio demuestra que los agentes ADK son más poderosos cuando combinan:

1. **Conocimiento base sólido** (modelo de lenguaje)
2. **Herramientas especializadas** (acceso a datos externos)  
3. **Lógica de decisión inteligente** (cuándo usar qué herramienta)

El resultado es un agente que no solo \"sabe\" sobre fútbol, sino que puede mantenerse actualizado y verificar información en tiempo real, ofreciendo una experiencia mucho más rica y confiable al usuario.