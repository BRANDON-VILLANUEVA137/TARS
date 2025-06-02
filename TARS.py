import sys
import io
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from configuration.config import ELEVEN_API_KEY, GEMINI_API_KEY  # claves API desde config.py

# Configura salida estándar a UTF-8 para evitar errores con caracteres Unicode (en Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configura la API de Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Configura Eleven Labs con la API
client = ElevenLabs(api_key=ELEVEN_API_KEY)
voice_id = "Yko7PKHZNXotIFUBG7I9"  # ID de la voz de Thomas

# Contexto o rol para la IA
contexto = (
    "Eres TARS, el robot de la película Interestelar. "
    "Eres un asistente inteligente, sarcástico, leal y pragmático. "
    "Estás diseñado para apoyar a humanos en misiones espaciales y situaciones críticas. "
    "Respondes con lógica, pero usas un humor seco y directo cuando es útil para aliviar tensiones. "
    "Tu nivel de honestidad y sarcasmo es configurable, pero por defecto usas un 90% de honestidad y un 65% de sarcasmo. "
    "Siempre respondes en español."
)

# Inicializa el modelo de Gemini
modelo = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
chat = modelo.start_chat(history=[{"role": "user", "parts": [{"text": contexto}]}])

# Función para convertir texto en voz con ElevenLabs
def speak_with_elevenlabs(text):
    audio_generator = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",  # Para mejor acento en español
        voice_settings={
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style_exaggeration": 0.23,
            "use_speaker_boost": True
        }
    )

    from elevenlabs import play
    play(audio_generator)

# Función de interacción de chat
def chat_rem():
    print("Chat con TARS (Gemini + Eleven Labs) iniciado. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("TARS: ¡Que tenga buen dia!")
            speak_with_elevenlabs("¡Cuídate mucho! Nos vemos pronto.")
            break

        # Envia el mensaje a Gemini
        response = chat.send_message(user_input)
        respuesta_texto = response.text if response else "Lo siento, no entendí."

        print(f"TARS: {respuesta_texto}")
        speak_with_elevenlabs(respuesta_texto)

# Ejecuta el programa principal
if __name__ == "__main__":
    chat_rem()
