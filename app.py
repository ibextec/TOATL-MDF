import streamlit as st
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from gridfs import GridFS

# Carregar variáveis de ambiente
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Conexão com o MongoDB
client = MongoClient(MONGODB_URI)
db = client["marceneiros"]
fs = GridFS(db)  # Para armazenar arquivos

# Coleção de marceneiros
carpinteiros = db["carpinteiros"]

st.set_page_config(page_title="Cadastro de Marceneiros", layout="wide")

def main():
    st.title("Cadastro de Marceneiro")
    
    # Formulário
    with st.form("cadastro_form"):
        nome = st.text_input("Nome Completo", key="nome")
        email = st.text_input("Email", key="email")
        telefone = st.text_input("Telefone", placeholder="(99) 9 9999-9999", key="telefone")
        endereco = st.text_area("Endereço", key="endereco")
        especialidade = st.multiselect(
            "Especialidades",
            ["Moveis Sob Medida", "Reparos", "Design de Interiores"],
            key="especialidade"
        )
        experiencia = st.number_input("Anos de Experiência", min_value=0, key="experiencia")
        portfolio = st.file_uploader("Portfólio (fotos)", accept_multiple_files=True, type=["jpg", "png"])
        certificacoes = st.text_area("Certificações", key="certificacoes")
        
        submitted = st.form_submit_button("Cadastrar")
        
        if submitted:
            # Validar campos obrigatórios
            if not nome or not email or not telefone:
                st.error("Preencha os campos obrigatórios!")
            else:
                # Salvar arquivos no GridFS
                portfolio_urls = []
                for file in portfolio:
                    file_id = fs.put(file.read(), filename=file.name)
                    portfolio_urls.append(f"{MONGODB_URI}/fs/{file_id}")  # URL fictícia
                
                # Inserir no MongoDB
                carpinteiros.insert_one({
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "endereco": endereco,
                    "especialidade": especialidade,
                    "experiencia": experiencia,
                    "portfolio": portfolio_urls,
                    "certificacoes": certificacoes,
                    "createdAt": st.session_state.get("now", st.datetime.now())
                })
                st.success("Cadastro realizado com sucesso!")
                
                # Limpar formulário
                st.session_state.nome = ""
                st.session_state.email = ""
                st.session_state.telefone = ""
                st.session_state.endereco = ""
                st.session_state.especialidade = []
                st.session_state.certificacoes = ""

if __name__ == "__main__":
    main()
streamlit==1.27.0
pymongo==4.5.0
python-dotenv==1.0.0
MONGODB_URI=mongodb+srv://<seu-usuario>:<sua-senha>@cluster0.mongodb.net/marceneiros?retryWrites=true&w=majority
[server]
port = 8501
# Instalar dependências
pip install -r requirements.txt

# Executar localmente
streamlit run app.py
# Dashboard (aba extra)
if st.sidebar.checkbox("Visualizar Marceneiros"):
    st.header("Lista de Marceneiros")
    for carpinteiro in carpinteiros.find():
        st.write(f"**Nome:** {carpinteiro['nome']}")
        st.write(f"**Especialidades:** {', '.join(carpinteiro['especialidade'])}")
        st.image(carpinteiro['portfolio'][0] if carpinteiro['portfolio'] else "https://via.placeholder.com/150")
import subprocess
subprocess.run(["pip", "install", "streamlit==1.27.0"])
