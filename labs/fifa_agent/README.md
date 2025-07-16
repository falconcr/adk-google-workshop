# FIFA World Cup Agent

An intelligent agent built with Google ADK (Agent Development Kit) that specializes in FIFA World Cup information. This agent uses Gemini 2.0 Flash as its language model and provides expert knowledge about World Cup history, statistics, players, and trivia.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Code Structure](#code-structure)
- [Step-by-Step Code Explanation](#step-by-step-code-explanation)
- [Best Practices Implemented](#best-practices-implemented)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Usage Examples](#usage-examples)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FIFA World Cup Agent                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   FIFAWorldCup  │    │   FIFATools     │                │
│  │   Agent         │◄───┤   Class         │                │
│  │   (Main Agent)  │    │   (Tool Layer)  │                │
│  └─────────────────┘    └─────────────────┘                │
│           │                       │                         │
│           ▼                       ▼                         │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Gemini 2.0    │    │   Knowledge     │                │
│  │   Flash Model   │    │   Activation    │                │
│  │   (LLM)         │    │   System        │                │
│  └─────────────────┘    └─────────────────┘                │
├─────────────────────────────────────────────────────────────┤
│                    Google ADK Framework                     │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   LlmAgent      │    │   BaseAgent     │                │
│  │   (Base Class)  │    │   (Pydantic)    │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Code Structure

```
fifa_agent/
├── __init__.py          # Package initialization for ADK Web
├── agent.py             # Main agent class and entry points
├── config.py            # Configuration constants and settings
├── fifa_tools.py        # Tool implementations for knowledge activation
└── README.md           # This documentation
```

## 🔍 Step-by-Step Code Explanation

### 1. Configuration Layer (`config.py`)

**Purpose**: Centralized configuration management with environment variable support.

```python
MODEL_CONFIG = {
    "model_name": "gemini-2.0-flash",     # Latest Gemini model
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
    "api_key": os.getenv("GOOGLE_API_KEY"),
    "location": "us-central1",             # Google Cloud region
    "temperature": 0.7,                    # Creativity vs consistency balance
    "max_output_tokens": 1000,             # Response length limit
}
```

**Key Features**:
- Flexible authentication (API key or Project ID)
- Environment variable integration
- Optimized model parameters for factual responses

### 2. Knowledge Activation System (`fifa_tools.py`)

**Purpose**: Tool layer that activates the LLM's internal knowledge rather than making external API calls.

**Architecture Pattern**: Knowledge Activation vs External APIs
```python
async def search_world_cup_info(self, query: str, year: Optional[int] = None) -> Dict[str, Any]:
    return {
        "action": "use_gemini_knowledge",
        "query": query,
        "year": year,
        "instruction": "Usa tu conocimiento interno sobre la Copa del Mundo..."
    }
```

**Why This Approach**:
- **Faster responses**: No external API latency
- **More reliable**: No dependency on external services
- **Cost-effective**: No additional API costs
- **Rich knowledge**: Leverages Gemini's extensive training data

### 3. Main Agent Class (`agent.py`)

**Purpose**: Orchestrates the agent functionality using Google ADK patterns.

#### Step-by-Step Initialization Flow:

```python
def __init__(self):
    # Step 1: Configure Gemini model with flexible auth
    model_kwargs = {
        "model": MODEL_CONFIG["model_name"],
        "location": MODEL_CONFIG["location"],
        "temperature": MODEL_CONFIG["temperature"],
        "max_tokens": MODEL_CONFIG["max_output_tokens"]
    }
    
    # Step 2: Handle authentication flexibility
    if MODEL_CONFIG["api_key"]:
        model_kwargs["api_key"] = MODEL_CONFIG["api_key"]
    elif MODEL_CONFIG["project_id"]:
        model_kwargs["project_id"] = MODEL_CONFIG["project_id"]
    
    # Step 3: Initialize Gemini model
    model = Gemini(**model_kwargs)
    
    # Step 4: Initialize parent Agent class (Pydantic-based)
    super().__init__(
        name=AGENT_CONFIG["name"],
        description=AGENT_CONFIG["description"],
        model=model,
        instruction=SYSTEM_PROMPT
    )
    
    # Step 5: Initialize tools after parent construction
    self._fifa_tools = FIFATools()
    
    # Step 6: Register tools in the ADK framework
    self.tools.extend([
        self.search_world_cup_info,
        self.get_player_statistics,
        self.get_country_performance,
        self.get_fun_facts
    ])
```

#### Tool Method Pattern:

Each tool method follows this pattern:
```python
async def search_world_cup_info(self, query: str, year: Optional[int] = None) -> Dict[str, Any]:
    """
    Tool description for Gemini to understand when to use it.
    """
    return await self._fifa_tools.search_world_cup_info(query, year)
```

### 4. Dual Execution Modes

#### CLI Mode (Direct Execution):
```python
async def main():
    agent = FIFAWorldCupAgent()
    # Interactive CLI loop with user input
    while True:
        query = input("👤 Tu pregunta: ").strip()
        response = await agent.run(query, context)
        print(f"🏆 Agente: {response}\n")
```

#### ADK Web Mode (Server Deployment):
```python
def get_agent():
    """Required by ADK Web for agent instantiation"""
    return FIFAWorldCupAgent()

# Global agent instance for web server
root_agent = get_agent()
```

## 🚀 Best Practices Implemented

### 1. **Pydantic Compatibility**
- ✅ Proper handling of Pydantic `extra='forbid'` configuration
- ✅ Private attributes (`_fifa_tools`) to avoid field validation errors
- ✅ Tool registration after parent initialization

### 2. **Google ADK Integration**
- ✅ Correct inheritance from `Agent` (which is `LlmAgent`)
- ✅ Proper tool registration using `self.tools.extend()`
- ✅ ADK Web compatibility with `get_agent()` function

### 3. **Configuration Management**
- ✅ Environment variable integration
- ✅ Centralized configuration
- ✅ Flexible authentication methods

### 4. **Async Programming**
- ✅ Proper async/await patterns
- ✅ Async tool methods for consistency
- ✅ Async agent execution

### 5. **Error Handling**
- ✅ Try-catch blocks in main loop
- ✅ Keyboard interrupt handling
- ✅ Graceful degradation

### 6. **Code Organization**
- ✅ Separation of concerns (config, tools, agent)
- ✅ Clear module structure
- ✅ Comprehensive documentation

### 7. **Internationalization**
- ✅ Spanish language support in prompts and responses
- ✅ Bilingual code comments
- ✅ Culturally appropriate interface

## 🛠️ Setup and Installation

### Prerequisites

1. **Python 3.8+**
2. **Google ADK**: `pip install google-adk`
3. **Google Cloud Authentication** (choose one):
   - Google API Key
   - Google Cloud Project with authentication

### Installation

```bash
# 1. Clone or download the agent
cd fifa_agent/

# 2. Install dependencies
pip install google-adk

# 3. Set up authentication (choose one method)

# Method A: Using API Key
export GOOGLE_API_KEY="your-api-key-here"

# Method B: Using Google Cloud Project
export GOOGLE_CLOUD_PROJECT="your-project-id"
# Ensure gcloud auth is configured:
# gcloud auth application-default login
```

## 🎯 How to Run

### Option 1: CLI Mode (Interactive)

```bash
# Run directly
python agent.py

# Or as module
python -m fifa_agent.agent
```

**Expected Output**:
```
🏆 FIFA World Cup Agent - ¡Pregúntame sobre la Copa del Mundo!
Ejemplos: '¿Quién ganó en 2014?', '¿Cuántos goles hizo Messi en 2022?', '¿Qué país tiene más Mundiales?'
Escribe 'salir' para terminar.

👤 Tu pregunta: 
```

### Option 2: ADK Web Mode (Server)

```bash
# Navigate to parent directory
cd /home/falcon/agents/

# Start ADK web server
adk web

# The agent will be available at: http://localhost:8000
# Agent endpoint: http://localhost:8000/fifa_agent
```

### Option 3: Programmatic Usage

```python
import asyncio
from fifa_agent.agent import FIFAWorldCupAgent

async def example():
    agent = FIFAWorldCupAgent()
    
    # Ask questions
    response = await agent.run("¿Quién ganó el Mundial 2014?", {})
    print(response)
    
    response = await agent.run("Estadísticas de Messi en 2022", {})
    print(response)

# Run
asyncio.run(example())
```

## 💡 Usage Examples

### Basic Queries
```
👤 ¿Quién ganó el Mundial de 2018?
🏆 Francia ganó la Copa del Mundo de 2018...

👤 ¿Cuántos goles hizo Pelé en Mundiales?
🏆 Pelé anotó 12 goles en 4 Copas del Mundo...

👤 ¿Qué país tiene más títulos mundiales?
🏆 Brasil lidera con 5 títulos mundiales...
```

### Advanced Queries
```
👤 Cuéntame sobre la final de 2022
🏆 La final de Qatar 2022 entre Argentina y Francia...

👤 ¿Qué records tiene Messi?
🏆 Lionel Messi tiene varios records en Copas del Mundo...

👤 Datos curiosos sobre Brasil
🏆 Brasil es el único país que ha participado en todas...
```

## 🌍 Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GOOGLE_API_KEY` | Optional* | Google API Key for Gemini | `AIza...` |
| `GOOGLE_CLOUD_PROJECT` | Optional* | Google Cloud Project ID | `my-project-123` |

*One of these is required for authentication.

## 🚨 Troubleshooting

### Common Issues

1. **"FIFAWorldCupAgent object has no field 'fifa_tools'"**
   - ✅ **Fixed**: Using `_fifa_tools` private attribute
   - **Cause**: Pydantic doesn't allow arbitrary fields

2. **"'FIFAWorldCupAgent' object has no attribute 'register_tool'"**
   - ✅ **Fixed**: Using `self.tools.extend()` instead
   - **Cause**: Google ADK doesn't have `register_tool` method

3. **Authentication Errors**
   ```bash
   # Check environment variables
   echo $GOOGLE_API_KEY
   echo $GOOGLE_CLOUD_PROJECT
   
   # Test gcloud auth (if using project ID)
   gcloud auth application-default print-access-token
   ```

4. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd /home/falcon/agents/
   
   # Check ADK installation
   pip list | grep google-adk
   ```

### Debug Mode

Add debug logging to `agent.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔧 Customization

### Adding New Tools

1. Add method to `FIFATools` class:
```python
async def new_tool(self, param: str) -> Dict[str, Any]:
    return {
        "action": "use_gemini_knowledge",
        "instruction": "New instruction for Gemini"
    }
```

2. Add corresponding method to `FIFAWorldCupAgent`:
```python
async def new_tool(self, param: str) -> Dict[str, Any]:
    return await self._fifa_tools.new_tool(param)
```

3. Register in `__init__`:
```python
self.tools.extend([
    # ... existing tools
    self.new_tool
])
```

### Modifying System Prompt

Edit `SYSTEM_PROMPT` in `config.py` to change agent behavior, add new capabilities, or adjust response style.

## 📄 License

This project demonstrates Google ADK usage and follows Google Cloud AI best practices.

---

**Built with**: Google ADK, Gemini 2.0 Flash, Python 3.12+