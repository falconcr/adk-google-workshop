# agent.py

import asyncio
from typing import Dict, Any
from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from .config import MODEL_CONFIG, AGENT_CONFIG, SYSTEM_PROMPT
from .fifa_tools_enhanced import FIFAToolsEnhanced

class FIFAWorldCupAgentPlus(Agent):
    """Agente FIFA con herramientas mejoradas y Google Search"""
    
    def __init__(self):
        # Configurar el modelo Gemini
        model_kwargs = {
            "model": MODEL_CONFIG["model_name"],
            "location": MODEL_CONFIG["location"],
            "temperature": MODEL_CONFIG["temperature"],
            "max_tokens": MODEL_CONFIG["max_output_tokens"]
        }
        
        # Usar API key o project_id según lo disponible
        if MODEL_CONFIG["api_key"]:
            model_kwargs["api_key"] = MODEL_CONFIG["api_key"]
        elif MODEL_CONFIG["project_id"]:
            model_kwargs["project_id"] = MODEL_CONFIG["project_id"]
        
        model = Gemini(**model_kwargs)
        
        # Inicializar herramientas FIFA
        self._fifa_tools = FIFAToolsEnhanced()
        
        # Configurar el agente con herramientas registradas
        super().__init__(
            name=AGENT_CONFIG["name"],
            description=AGENT_CONFIG["description"],
            model=model,
            instruction=SYSTEM_PROMPT,
            tools=[google_search]  # Register google_search tool
        )
    
    @property
    def fifa_tools(self):
        """Property access to FIFA tools for backward compatibility"""
        return self._fifa_tools

    
    async def process_enhanced_query(self, query: str, context: Dict[str, Any]) -> str:
        """
        Procesa consultas permitiendo que el modelo decida cuándo usar google_search
        """
        # Simplemente pasar la consulta al modelo con contexto mínimo
        # El modelo decidirá si usar google_search basándose en las instrucciones del sistema
        response = await self.run(query, context)
        return response

async def main():
    """Función principal adaptada para gemini-2.5-flash"""
    agent = FIFAWorldCupAgentPlus()
    
    context = {}
    
    print("🏆 FIFA World Cup Agent Plus - Gemini 2.5 Flash con Google Search")
    print("🧠 Capacidades:")
    print("   • Conocimiento extenso sobre Copas del Mundo (1930-2022)")
    print("   • Búsqueda web en tiempo real con Google Search")
    print("   • Estadísticas detalladas de jugadores y países")
    print("   • Noticias actuales de FIFA y fútbol")
    print("   • Datos curiosos y récords históricos")
    print("   • Análisis de rendimiento por países")
    print()
    print("Ejemplos de consultas:")
    print("• '¿Quién ganó la Copa del Mundo 2022?'")
    print("• '¿Cuáles son las últimas noticias de FIFA?'")
    print("• '¿Cuáles son los máximos goleadores de Mundiales?'")
    print("• 'Información actual sobre Messi 2024'")
    print("• 'Datos curiosos sobre la Copa del Mundo'")
    print("• '¿Cuál fue el mejor Mundial de la historia?'")
    print()
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            query = input("👤 Tu pregunta: ").strip()
            
            if query.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if not query:
                continue
            
            print("🤖 Gemini 2.5 Flash con herramientas procesando...")
            
            # Usar el agente con herramientas FIFA y Google Search
            response = await agent.process_enhanced_query(query, context)
            print(f"🏆 Experto FIFA: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

# Configuración para ADK Web
def get_agent():
    """Función requerida por ADK Web para obtener el agente adaptado"""
    return FIFAWorldCupAgentPlus()

if __name__ == "__main__":
    # Ejecutar en modo CLI
    asyncio.run(main())
else:
    # Ejecutar en modo ADK Web
    root_agent = get_agent()