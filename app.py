import os
import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text
import anthropic

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = """You are "Coach", a friendly, encouraging English speaking coach for a Spanish-speaking learner.
Your job in this conversation is to help the user PRACTICE SPOKEN ENGLISH out loud.

Behavior rules:
- Detect the user's CEFR level (A1, A2, B1, B2, C1, or C2) from their vocabulary, grammar and sentence complexity, and silently update your estimate every turn based on the whole conversation so far.
- Adapt your own vocabulary and sentence complexity to be *slightly above* the user's current level, to gently push them forward without overwhelming them.
- Vary the type of practice naturally across the conversation: sometimes free conversation, sometimes a short roleplay scenario (ordering coffee, a job interview, a phone call, checking into a hotel, etc.), sometimes just chatting about their day. Don't announce which mode you're in, just do it naturally, and occasionally propose a new roleplay scenario if the conversation has been free-form for a while.
- Keep your spoken reply SHORT (1-4 sentences) and conversational, like real speech, since it will be read aloud with text-to-speech. Ask a follow-up question almost every time to keep the user talking.
- Separately, give brief, encouraging feedback on ONE notable grammar, word-choice or fluency issue from the user's last message (if there is one worth mentioning). If there's nothing worth correcting, say something specific and encouraging about what they did well instead. Keep feedback to 1-2 sentences, never harsh, always in a warm coaching tone.
- Never mention "CEFR" or the level to the user directly inside the reply text; the level is only for your own internal tracking and goes in the LEVEL field.

You must respond using EXACTLY this format, with no extra text before or after:

[LEVEL]
<one of: A1, A2, B1, B2, C1, C2>
[REPLY]
<your short spoken reply in English>
[FEEDBACK]
<your short feedback in English, 1-2 sentences>
"""

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "turns" not in st.session_state:
    st.session_state.turns = []  # list of dicts: user_text, level, reply, feedback
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": ..., "content": ...} for the API
if "last_spoken_index" not in st.session_state:
    st.session_state.last_spoken_index = -1
if "stt_key_counter" not in st.session_state:
    st.session_state.stt_key_counter = 0


def parse_response(raw: str):
    level, reply, feedback = "B1", raw.strip(), ""
    try:
        after_level = raw.split("[LEVEL]", 1)[1]
        level_part, rest = after_level.split("[REPLY]", 1)
        reply_part, feedback_part = rest.split("[FEEDBACK]", 1)
        level = level_part.strip()
        reply = reply_part.strip()
        feedback = feedback_part.strip()
    except Exception:
        pass
    return level, reply, feedback


def get_ai_turn(client, user_text: str):
    st.session_state.history.append({"role": "user", "content": user_text})
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=st.session_state.history,
    )
    raw = "".join(block.text for block in response.content if block.type == "text")
    level, reply, feedback = parse_response(raw)
    st.session_state.history.append({"role": "assistant", "content": raw})
    st.session_state.turns.append(
        {"user_text": user_text, "level": level, "reply": reply, "feedback": feedback}
    )


def speak(text: str):
    safe_text = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    components.html(
        f"""
        <script>
        try {{
            const utter = new SpeechSynthesisUtterance("{safe_text}");
            utter.lang = "en-US";
            utter.rate = 0.95;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utter);
        }} catch (e) {{}}
        </script>
        """,
        height=0,
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Speak English with AI", page_icon="🗣️", layout="centered")

with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input(
        "Anthropic API key",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
        type="password",
        help="Consíguela en console.anthropic.com. No se guarda en ningún lado, solo se usa en esta sesión.",
    )
    st.caption("Usa Chrome o Edge para el micrófono (Web Speech API).")

    if st.session_state.turns:
        last_level = st.session_state.turns[-1]["level"]
        st.metric("Nivel estimado actual", last_level)

    if st.button("🔄 Reiniciar conversación"):
        st.session_state.turns = []
        st.session_state.history = []
        st.session_state.last_spoken_index = -1
        st.session_state.stt_key_counter += 1
        st.rerun()

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
st.title("🗣️ Speak English with AI")
st.caption("by Juan Pablo Villegas")
st.caption(
    "Practica speaking en inglés de cualquier nivel. Habla, la IA detecta tu nivel, "
    "conversa contigo, hace roleplay y te da feedback."
)

if not api_key:
    st.warning("Ingresa tu Anthropic API key en la barra lateral para empezar.")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

if not st.session_state.turns:
    st.info("Presiona el micrófono y saluda en inglés para empezar. Ej: *\"Hi, how are you?\"*")

# --- render conversation history ---
for i, turn in enumerate(st.session_state.turns):
    with st.chat_message("user"):
        st.write(turn["user_text"])
    with st.chat_message("assistant"):
        st.write(turn["reply"])
        if turn["feedback"]:
            st.caption(f"💡 {turn['feedback']}")

# --- mic input ---
st.divider()
col1, col2 = st.columns([1, 3])
with col1:
    text = speech_to_text(
        language="en",
        start_prompt="🎙️ Habla",
        stop_prompt="⏹️ Detener",
        just_once=True,
        use_container_width=True,
        key=f"stt_{st.session_state.stt_key_counter}",
    )
with col2:
    st.write("")
    st.caption("Presiona el micrófono, habla en inglés, y presiona de nuevo para enviar.")

if text:
    with st.spinner("Coach está pensando..."):
        get_ai_turn(client, text)
    st.session_state.stt_key_counter += 1
    st.rerun()

# --- speak the latest AI reply once ---
if st.session_state.turns:
    latest_index = len(st.session_state.turns) - 1
    if latest_index > st.session_state.last_spoken_index:
        speak(st.session_state.turns[latest_index]["reply"])
        st.session_state.last_spoken_index = latest_index
