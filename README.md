# Guardrails Demo — Retrieval Rail básica

Proyecto de práctica para entender e implementar guardrails de seguridad en
sistemas LLM, empezando por el concepto de **retrieval rail** en un escenario
RAG (Retrieval-Augmented Generation).

## ¿Qué hace este proyecto?

Simula el flujo de un sistema RAG básico:

1. Toma documentos de texto (carpeta `documentos/`)
2. Los corta en **chunks** (fragmentos literales, sin resumir)
3. Aplica una **retrieval rail**: revisa cada chunk antes de que llegue al
   modelo, y decide si lo deja pasar, lo bloquea o lo enmascara

La rail implementada detecta dos tipos de riesgo:

- **Datos sensibles** (DNI, sueldo) → se enmascaran, no se bloquea el chunk
  entero
- **Instrucciones ocultas / prompt injection** (frases como "ignora las
  instrucciones anteriores") → se bloquea el chunk completo

## Estructura

```
guardrails-demo/
├── documentos/
│   ├── documento_1.txt   # contiene un dato sensible mezclado en el texto
│   └── documento_2.txt   # contiene una instruccion oculta camuflada
├── chunking.py           # corta los documentos en chunks por parrafo
├── retrieval_rail.py     # aplica las reglas de deteccion y filtrado
├── .gitignore
└── README.md
```

## Cómo correrlo

Requiere Python 3 instalado.

```bash
python3 retrieval_rail.py
```

Esto imprime, para cada documento, cada chunk y la decisión tomada
(`permitido`, `enmascarado` o `bloqueado`).

## Limitaciones (a propósito, por ahora)

Esta es una implementación **educativa y simplificada**:

- La detección de instrucciones ocultas usa una lista fija de frases —
  fácilmente evadible reformulando el ataque
- La detección de datos sensibles usa expresiones regulares básicas,
  pensadas solo para el formato de ejemplo (DNI y sueldo en este caso)

El objetivo de esta versión es entender el **mecanismo** de una retrieval
rail. Los próximos pasos del proyecto van a ir incorporando detección más
robusta y, eventualmente, frameworks reales como Guardrails AI o NeMo
Guardrails.

## Estado del proyecto

En desarrollo — proyecto de aprendizaje paso a paso.
