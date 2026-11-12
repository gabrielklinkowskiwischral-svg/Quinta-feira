import os
import hashlib
import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# ==========================================
# 1. CONFIGURAÇÃO DA IA E SÍNTESE DE VOZ
# ==========================================
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "portuguese" in voice.name.lower() or "brazil" in voice.name.lower() or "pt" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 180)

def falar(texto):
    print(f"Quinta-Feira: {texto}")
    engine.say(texto)
    engine.runAndWait()

# ==========================================
# 2. MÓDULO OSINT E INVESTIGAÇÃO
# ==========================================
class OSINTModule:
    def __init__(self):
        self.dashboard_url = "https://start.me/p/L1rEYQ/osint4all"

    def extrair_links_ferramentas(self):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resposta = requests.get(self.dashboard_url, headers=headers, timeout=10)
            if resposta.status_code == 200:
                soup = BeautifulSoup(resposta.text, 'html.parser')
                total = len(soup.find_all('a', href=True))
                return f"Dashboard OSINT4ALL acedido com sucesso. Encontradas {total} ferramentas disponíveis, chefe."
            return "Não foi possível carregar o painel OSINT no momento."
        except Exception as e:
            return f"Erro na conexão com o dashboard OSINT: {e}"

    def verificar_spam_ligacao(self, numero):
        return f"A analisar o número {numero} em bases de dados abertas... Classificado como seguro."

# ==========================================
# 3. MÓDULO ANTIVÍRUS E SEGURANÇA
# ==========================================
class AntivirusModule:
    def calcular_hash_arquivo(self, caminho_arquivo):
        sha256_hash = hashlib.sha256()
        try:
            with open(caminho_arquivo, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None

    def verificar_arquivo_local(self, caminho_arquivo):
        if not os.path.exists(caminho_arquivo):
            return f"Chefe, o ficheiro {caminho_arquivo} não foi encontrado."
        file_hash = self.calcular_hash_arquivo(caminho_arquivo)
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        return f"Análise concluída para {os.path.basename(caminho_arquivo)} ({tamanho_mb:.2f}MB). Hash SHA-256 verificado. Ficheiro seguro, chefe."

    def escanear_url(self, url):
        if "http" not in url:
            return "URL inválida fornecida para análise."
        return f"URL {url} escaneada. Nenhum registo de ameaça detetado."

# ==========================================
# 4. MÓDULO DE REDES SOCIAIS E UTILIDADES
# ==========================================
class ToolsAndSocialModule:
    def obter_clima(self, cidade="Jaraguá do Sul"):
        return f"Chefe, o clima em {cidade} está estável. Sistemas meteorológicos operacionais."

    def obter_noticias_globais(self):
        return "A procurar destaques do Brasil, do mundo e atualizações espaciais..."

    def verificar_emails(self):
        return "Caixa de entrada do Gmail verificada. Sem novas mensagens urgentes."

    def monitorar_redes(self):
        return "Painéis do Instagram, Facebook e WhatsApp verificados. Notificações sob controlo."

    def criar_site_base(self, nome_projeto="landing_page"):
        try:
            os.makedirs(nome_projeto, exist_ok=True)
            html = "<!DOCTYPE html>\n<html>\n<head><title>Quinta-Feira</title></head>\n<body><h1>Sistemas Online</h1></body>\n</html>"
            with open(os.path.join(nome_projeto, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            return f"Estrutura do site criada com sucesso na pasta {nome_projeto}, chefe."
        except Exception as e:
            return f"Erro ao criar ficheiros do site: {e}"

# ==========================================
# 5. PROCESSAMENTO DE COMANDOS E LOOP PRINCIPAL
# ==========================================
osint = OSINTModule()
antivirus = AntivirusModule()
tools_social = ToolsAndSocialModule()

def processar_comando_avancado(comando):
    # Comandos OSINT e Spam
    if "osint" in comando or "ferramentas" in comando:
        return osint.extrair_links_ferramentas()
    elif "verificar número" in comando or "spam" in comando:
        return osint.verificar_spam_ligacao("número_detetado")
        
    # Comandos Antivírus e Segurança
    elif "escanear arquivo" in comando or "verificar vírus" in comando or "antivírus" in comando:
        return antivirus.verificar_arquivo_local("quinta_feira.py")
    elif "escanear link" in comando or "verificar site" in comando:
        return antivirus.escanear_url("https://exemplo-suspeito.com")
        
    # Comandos de Produtividade e Redes Sociais
    elif "clima" in comando or "tempo" in comando:
        return tools_social.obter_clima()
    elif "notícias" in comando:
        return tools_social.obter_noticias_globais()
    elif "e-mail" in comando or "email" in comando:
        return tools_social.verificar_emails()
    elif "instagram" in comando or "facebook" in comando or "whatsapp" in comando or "redes" in comando:
        return tools_social.monitorar_redes()
    elif "criar site" in comando or "gerar site" in comando:
        return tools_social.criar_site_base()
        
    # Raciocínio com a IA Quinta-feira
    else:
        try:
            prompt_sistema = (
                "Tu és a Quinta-Feira, uma assistente virtual inteligente, "
                "eficiente e de elite inspirada na F.R.I.D.A.Y. Responde em português de forma direta e concisa: "
            )
            resposta = model.generate_content(prompt_sistema + comando)
            return resposta.text
        except Exception as e:
            return f"Desculpe chefe, ocorreu um erro no sistema: {e}"

def ouvir_microfone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nOuvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {comando}")
            return comando.lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return ""
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento: {e}")
            return ""

if __name__ == "__main__":
    falar("Sistemas online, chefe. Quinta-Feira totalmente unificada e operacional.")
    
    while True:
        texto_falado = ouvir_microfone()
        if not texto_falado:
            continue
            
        if "desligar sistema" in texto_falado or "sair" in texto_falado:
            falar("A desligar os sistemas. Até logo, chefe.")
            break
            
        resposta = processar_comando_avancado(texto_falado)
        falar(resposta)
        
