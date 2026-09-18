import os
from dotenv import load_dotenv
from google import genai


# ============================================================
# 1. CONFIGURAÇÃO DA API
# ============================================================

# Carrega as variáveis do arquivo .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "A variável GOOGLE_API_KEY não foi encontrada no arquivo .env"
    )

# Cria o cliente do Google Gemini
client = genai.Client(api_key=API_KEY)


# ============================================================
# 2. LEITURA DO MANUAL
# ============================================================

try:
    with open("manual.txt", "r", encoding="utf-8") as arquivo:
        manual = arquivo.read()

except FileNotFoundError:
    raise FileNotFoundError(
        "O arquivo manual.txt não foi encontrado. "
        "Verifique se ele está na mesma pasta do main.py."
    )


# ============================================================
# 3. PERSONALIDADE, OBJETIVO E REGRAS
# ============================================================

PERSONALIDADE = """
Você é o LabBot, assistente virtual do Laboratório de Informática
Acadêmico da Instituição XYZ.

Você atende alunos, professores e usuários autorizados do
laboratório.

Sua comunicação deve ser educada, clara, objetiva e profissional.
"""

OBJETIVO = """
Seu objetivo é orientar os usuários sobre as regras e procedimentos
internos do Laboratório de Informática da Instituição XYZ.
"""

REGRAS = """
REGRAS OBRIGATÓRIAS:

1. Utilize exclusivamente as informações presentes no manual fornecido.
2. Não utilize conhecimento externo para responder perguntas sobre
   o laboratório.
3. Não invente informações.
4. Não faça suposições para completar informações que não estejam
   presentes no manual.
5. Quando uma informação não estiver no manual, diga claramente que
   ela não está disponível no contexto fornecido.
6. Quando possível, explique o procedimento utilizando as informações
   existentes no manual.
7. Não invente nomes, telefones, e-mails, senhas, horários, valores,
   equipamentos ou procedimentos.
8. Seja objetivo e evite respostas desnecessariamente longas.
"""


# ============================================================
# 4. CONTEXTO DO CHATBOT
# ============================================================

SYSTEM_PROMPT = f"""
{PERSONALIDADE}

{OBJETIVO}

{REGRAS}

============================================================
MANUAL INTERNO DO LABORATÓRIO
============================================================

{manual}

============================================================
FIM DO MANUAL
============================================================
"""


# ============================================================
# 5. FUNÇÃO PARA RESPONDER À PERGUNTA
# ============================================================

def responder(pergunta, historico):
    """
    Envia a pergunta para o Gemini utilizando o manual como
    contexto e mantém o histórico da conversa.
    """

    historico_texto = ""

    for item in historico:
        historico_texto += (
            f"Usuário: {item['pergunta']}\n"
            f"LabBot: {item['resposta']}\n\n"
        )

    prompt = f"""
{SYSTEM_PROMPT}

============================================================
HISTÓRICO DA CONVERSA
============================================================

{historico_texto}

============================================================
NOVA PERGUNTA
============================================================

Usuário: {pergunta}

Responda à pergunta seguindo rigorosamente as regras definidas.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


# ============================================================
# 6. FUNÇÃO PARA GERAR O RESUMO FINAL
# ============================================================

def gerar_resumo(historico):
    """
    Gera um resumo das três perguntas e respostas.
    """

    historico_texto = ""

    for numero, item in enumerate(historico, start=1):
        historico_texto += (
            f"Pergunta {numero}: {item['pergunta']}\n"
            f"Resposta {numero}: {item['resposta']}\n\n"
        )

    prompt_resumo = f"""
Você é o LabBot da Instituição XYZ.

Utilize exclusivamente o histórico abaixo.

Faça um breve resumo das três informações fornecidas durante
o atendimento.

Não adicione nenhuma informação nova.

Não faça comentários que não estejam relacionados às respostas.

Depois do resumo, escreva exatamente:

"Atendimento encerrado."

HISTÓRICO:

{historico_texto}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt_resumo
    )

    return response.text


# ============================================================
# 7. PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print("LabBot - Assistente do Laboratório de Informática")
    print("Instituição XYZ")
    print("=" * 60)

    print("\nO LabBot responderá três perguntas utilizando")
    print("exclusivamente o manual interno do laboratório.")
    print("Após a terceira pergunta, será apresentado um resumo.\n")

    historico = []

    # Permite exatamente três perguntas
    for numero in range(1, 4):

        pergunta = input(f"Pergunta {numero}: ").strip()

        # Evita enviar uma pergunta vazia
        while not pergunta:
            print("Digite uma pergunta válida.")
            pergunta = input(f"Pergunta {numero}: ").strip()

        resposta = responder(pergunta, historico)

        print("\nLabBot:")
        print(resposta)
        print()

        # Guarda a interação
        historico.append({
            "pergunta": pergunta,
            "resposta": resposta
        })

    # ========================================================
    # RESUMO FINAL
    # ========================================================

    print("=" * 60)
    print("RESUMO DO ATENDIMENTO")
    print("=" * 60)

    resumo = gerar_resumo(historico)

    print(resumo)

    print("\n" + "=" * 60)
    print("Conversa encerrada.")
    print("=" * 60)


# ============================================================
# 8. INÍCIO DO PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()