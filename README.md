# Speak English with AI 🗣️

*by Juan Pablo Villegas*

App de Streamlit para practicar **speaking en inglés** con IA, para cualquier nivel (A1 a C2).

## Qué hace

- Escuchas tu voz en inglés a través del micrófono del navegador (gratis, sin costo de transcripción).
- La IA responde en voz (texto a voz del navegador) y por escrito.
- Detecta tu nivel automáticamente y ajusta la dificultad de sus respuestas.
- Mezcla conversación libre, roleplay (pedir café, entrevista de trabajo, hotel, etc.) y feedback breve de gramática/vocabulario después de cada turno tuyo.

## Requisitos

- Una API key de **Google AI Studio** (Gemini) — **100% gratis, sin tarjeta de crédito**. Solo necesitas una cuenta de Google.
  1. Ve a https://aistudio.google.com/apikey
  2. Inicia sesión con tu cuenta de Google
  3. Haz clic en "Create API key"
  4. Copia la key y pégala en la barra lateral de la app
- Navegador **Chrome o Edge** (el reconocimiento de voz usa la Web Speech API, que Firefox/Safari no soportan bien).
- Micrófono y permisos de audio habilitados en el navegador.

## Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá en `http://localhost:8501`. Pega tu API key en la barra lateral.

## Desplegar gratis en Streamlit Cloud

1. Sube esta carpeta a un repositorio de GitHub.
2. Ve a https://share.streamlit.io, conecta el repo y selecciona `app.py`.
3. Streamlit Cloud sirve la app por HTTPS automáticamente, así que el micrófono funcionará igual.
4. Puedes dejar el campo de API key vacío en el código y que cada usuario pegue la suya, o guardar tu key como "Secret" en la configuración de la app (variable `GOOGLE_API_KEY`) si solo la vas a usar tú.

## Cómo usar

1. Abre la app, pega tu API key de Google AI Studio.
2. Presiona el botón de micrófono (🎙️ Habla), di algo en inglés, y presiona de nuevo (⏹️ Detener) para enviar.
3. Escucha la respuesta de la IA (se reproduce sola) y lee el feedback debajo.
4. Sigue conversando — la IA seguirá el hilo, a veces te propondrá un roleplay, y tu nivel estimado se muestra en la barra lateral.
5. "Reiniciar conversación" borra el historial y empieza de cero.

## Notas técnicas

- El modelo usado es `gemini-2.5-flash`, que está dentro del nivel gratis de Google AI Studio (sin tarjeta, sin vencimiento).
- La transcripción de voz a texto es 100% del navegador (gratis, sin llamadas a API externas para eso).
- La síntesis de voz (texto a voz) también es del navegador.
- Nota: en el nivel gratis, Google puede usar tus prompts para mejorar sus productos. Si te preocupa la privacidad, revisa la política de Google AI Studio.
