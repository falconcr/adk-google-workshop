#!/usr/bin/env python3
# test_simple.py - Prueba simple del agente FIFA con gemini-2.0-flash-exp

import asyncio
from agent import FIFAWorldCupAgentPlus

async def test_basic_queries():
    """Prueba básica del agente FIFA sin function calling"""
    
    agent = FIFAWorldCupAgentPlus()
    context = {}
    
    test_queries = [
        "¿Quién ganó la Copa del Mundo 2022?",
        "¿Cuántas Copas del Mundo ha ganado Brasil?",
        "¿Quién es el máximo goleador en la historia de los Mundiales?",
        "Dame un dato curioso sobre la Copa del Mundo"
    ]
    
    print("🏆 Probando FIFA World Cup Agent con Gemini 2.0 Flash Exp")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Pregunta: {query}")
        print("-" * 40)
        
        try:
            response = await agent.run(query, context)
            print(f"Respuesta: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_basic_queries())