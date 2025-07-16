# agent.py

import asyncio
from typing import Dict, Any, Optional
from google.adk import Agent
from google.adk.models.google_llm import Gemini
from .fifa_tools import FIFATools
from .config import MODEL_CONFIG, AGENT_CONFIG, SYSTEM_PROMPT

class FIFAWorldCupAgent(Agent):
    """Agente especializado en Copa Mundial de la FIFA que usa Gemini Flash 2.0 como fuente principal"""
    
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
        
        # Configurar el agente directamente
        super().__init__(
            name=AGENT_CONFIG["name"],
            description=AGENT_CONFIG["description"],
            model=model,
            instruction=SYSTEM_PROMPT
        )
        
        # Inicializar herramientas después de super().__init__()
        self._fifa_tools = FIFATools()
        
        # Registrar herramientas directamente en la lista tools
        self.tools.extend([
            self.search_world_cup_info,
            self.get_player_statistics,
            self.get_country_performance,
            self.get_fun_facts
        ])
    
    async def search_world_cup_info(self, query: str, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Permite a Gemini buscar información específica sobre Mundiales.
        
        Args:
            query: Consulta específica (ej: "ganador", "goleador", "final")
            year: Año del Mundial (opcional)
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self._fifa_tools.search_world_cup_info(query, year)
    
    async def get_player_statistics(self, player_name: str, context: str = "world_cup") -> Dict[str, Any]:
        """
        Permite a Gemini proporcionar estadísticas de jugadores.
        
        Args:
            player_name: Nombre del jugador
            context: Contexto (ej: "world_cup", "career", "specific_year")
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self._fifa_tools.get_player_statistics(player_name, context)
    
    async def get_country_performance(self, country: str) -> Dict[str, Any]:
        """
        Permite a Gemini proporcionar información sobre el rendimiento de países.
        
        Args:
            country: Nombre del país
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self._fifa_tools.get_country_performance(country)
    
    async def get_fun_facts(self, topic: str = "general") -> Dict[str, Any]:
        """
        Permite a Gemini compartir datos curiosos sobre la Copa del Mundo.
        
        Args:
            topic: Tema específico (ej: "records", "history", "players")
            
        Returns:
            Información que activa el conocimiento interno de Gemini
        """
        return await self._fifa_tools.get_fun_facts(topic)

async def main():
    """Función principal para probar el agente"""
    agent = FIFAWorldCupAgent()
    
    # Contexto básico
    context = {}
    
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

# Configuración para ADK Web
def get_agent():
    """Función requerida por ADK Web para obtener el agente"""
    return FIFAWorldCupAgent()

if __name__ == "__main__":
    # Ejecutar en modo CLI
    asyncio.run(main())
else:
    # Ejecutar en modo ADK Web
    root_agent = get_agent()