import google.generativeai as genai
from configuration.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def listar_modelos():
    modelos = genai.list_models()
    print("Modelos disponibles:")
    for modelo in modelos:  # iteramos directamente
        print(f"Nombre: {modelo.name}")
        print(f"Versión: {modelo.version}")
        print(f"Métodos soportados: {modelo.supported_generation_methods}")
        print("-------------")

if __name__ == "__main__":
    listar_modelos()
