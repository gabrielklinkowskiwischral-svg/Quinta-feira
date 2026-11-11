import os
import speech_recognition as sr
import pyttsx3
from google import genai

# Inicializa o sintetizador de voz para a Quinta-Feira falar
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Tenta configurar uma voz em português se disponível
for voice in voices:
    if "portuguese" in voice.name.lower() or "brazil" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 180)

def falar(texto):
    print(f"Quinta-Feira: {texto}")
    engine.say(texto)
    engine.runAndWait()

# Inicializa o cliente do Gemini
client = genai.Client()

def pensar_com_ia(pergunta):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Tu és a Quinta-Feira, uma assistente virtual inteligente, eficiente e prestativa. Responde em português de forma direta e concisa: {pergunta}"
        )
        return response.text
    except Exception as e:
        return f"Desculpe chefe, ocorreu um erro: {e}"

def ouvir_microfone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nOuvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processando áudio...")
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {comando}")
            return comando.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento de voz: {e}")
            return ""

if __name__ == "__main__":
    falar("Sistemas online, chefe. Quinta-Feira pronta para ajudar.")
    
    while True:
        texto_falado = ouvir_microfone()
        
        if not texto_falado:
            continue
            
        if "desligar sistema" in texto_falado or "sair" in texto_falado:
            falar("A desligar os sistemas. Até logo, chefe.")
            break
            
        resposta_ia = pensar_com_ia(texto_falado)
        falar(resposta_ia)
      
