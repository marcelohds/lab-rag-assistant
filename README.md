# LabBot – Assistente do Laboratório de Informática

## Descrição

O LabBot é um chatbot especialista desenvolvido em Python para
responder dúvidas sobre os procedimentos internos de um
laboratório de informática acadêmico.

O projeto utiliza um contexto fechado contendo um manual fictício
com regras de utilização dos computadores, instalação de
softwares, impressões e comunicação de problemas.

O chatbot utiliza a API do Google Gemini como provedor do LLM.

## Tecnologias

- Python
- Google Gemini API
- Google GenAI SDK
- python-dotenv
- Git e GitHub

## Contexto

O conhecimento utilizado pelo chatbot está definido no código
do projeto e representa um manual interno fictício do laboratório.

O chatbot foi configurado para não inventar informações e para
informar quando uma informação não estiver presente no manual.

## Como Executar o Projeto

1. Clonar o repositório:
git clone https://github.com/marcelohds/lab-rag-assistant.git

2. Entrar na pasta:
cd labbot

3. Instalar as dependências:
pip install -r requirements.txt

4. Configurar a API Key:
Crie um arquivo chamado .env na raiz do projeto (utilize o env.example como modelo) e insira sua chave:
GOOGLE_API_KEY=SUA_CHAVE_AQUI

5. Executar:
python main.py
