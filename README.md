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
  4. Copia la key (la usarás en el paso de configuración de Secrets, más abajo)
- Navegador **Chrome o Edge** (el reconocimiento de voz usa la Web Speech API, que Firefox/Safari no soportan bien).
- Micrófono y permisos de audio habilitados en el navegador.

La app está configurada para usar **una sola key compartida** (la tuya) para todos los usuarios — nadie más tiene que crear su propia cuenta ni pegar ninguna key.

## Instalación local

```bash
pip install -r requirements.txt
```

Crea un archivo `.streamlit/secrets.toml` en la carpeta del proyecto con:

```toml
GOOGLE_API_KEY = "tu_api_key_aqui"
```

Luego:

```bash
streamlit run app.py
```

Se abrirá en `http://localhost:8501` y funcionará automáticamente, sin pedir ninguna key al usuario.

## Desplegar gratis en Streamlit Cloud (con key compartida)

1. Sube esta carpeta a un repositorio de GitHub (el archivo `.streamlit/secrets.toml`, si lo creaste local, **no lo subas** — agrégalo a `.gitignore`).
2. Ve a https://share.streamlit.io, conecta el repo y selecciona `app.py`.
3. Una vez desplegada, entra a tu app → botón **"⋮" (tres puntos) → Settings → Secrets**.
4. Pega esto en el cuadro de texto:
   ```toml
   GOOGLE_API_KEY = "tu_api_key_aqui"
   ```
5. Guarda. Streamlit reiniciará la app sola y ya quedará funcionando para todos los usuarios sin pedirles ninguna key.

⚠️ **Importante:** como todos los usuarios comparten tu misma key, comparten también tu cuota gratis de Google (peticiones por minuto/día). Si mucha gente usa la app al mismo tiempo, es posible que alguien vea un error temporal por límite alcanzado — simplemente hay que esperar un poco y reintentar.

## Cómo usar

1. Abre la app (ya no pide ninguna key).
2. Presiona el botón de micrófono (🎙️ Habla), di algo en inglés, y presiona de nuevo (⏹️ Detener) para enviar.
3. Escucha la respuesta de la IA (se reproduce sola) y lee el feedback debajo.
4. Sigue conversando — la IA seguirá el hilo, a veces te propondrá un roleplay, y tu nivel estimado se muestra en la barra lateral.
5. "Reiniciar conversación" borra el historial y empieza de cero.

## Notas técnicas

- El modelo usado es `gemini-flash-latest`, un alias que Google mantiene apuntando siempre a la versión Flash vigente (dentro del nivel gratis de Google AI Studio, sin tarjeta, sin vencimiento). Usar el alias evita que la app se rompa cuando Google retira una versión específica (ej. `gemini-2.5-flash`).
- La transcripción de voz a texto es 100% del navegador (gratis, sin llamadas a API externas para eso).
- La síntesis de voz (texto a voz) también es del navegador.
- Nota: en el nivel gratis, Google puede usar tus prompts para mejorar sus productos. Si te preocupa la privacidad, revisa la política de Google AI Studio.
