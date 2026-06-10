import streamlit as st
import pandas as pd
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONEXÃO COM FIREBASE ---
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de Redução de Custos", layout="wide")

# --- FUNÇÕES DE BANCO DE DADOS ---
def salvar_no_firebase(dados):
    db.collection("ideias").add(dados)

def ler_do_firebase():
    docs = db.collection("ideias").stream()
    return [doc.to_dict() for doc in docs]

# --- INTERFACE ---
st.sidebar.title("🛠️ Simulador de Perfil")
perfil_atual = st.sidebar.radio("Login:", ["1. Proponente", "2. Analista", "3. Gestor"])

st.sidebar.divider()

# ==========================================
# TELA 1: PROPONENTE
# ==========================================
if perfil_atual == "1. Proponente":
    st.title("💡 Nova Oportunidade de Melhoria")
    
    with st.form("form_nova_ideia"):
        titulo = st.text_input("Título da Ideia")
        descricao = st.text_area("Descrição do problema e da solução")
        area = st.selectbox("Área Impactada", ["Garantia", "TI", "RH", "Logística", "Outros"])
        
        enviado = st.form_submit_button("Enviar para Análise")
        
        if enviado:
            nova_ideia = {
                "data": datetime.datetime.now().strftime("%d/%m/%Y"),
                "titulo": titulo,
                "descricao": descricao,
                "area": area,
                "status": "Em Análise",
                "parecer_analista": "",
                "decisao_final": ""
            }
            salvar_no_firebase(nova_ideia)
            st.success("Ideia enviada para o Firebase com sucesso!")

    st.subheader("Minhas Ideias na Nuvem")
    dados = ler_do_firebase()
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df[['data', 'titulo', 'area', 'status']], hide_index=True)

# ==========================================
# TELA 2: ANALISTA
# ==========================================
elif perfil_atual == "2. Analista":
    st.title("🔍 Fila de Análise Técnica")
    dados = ler_do_firebase()
    
    if not dados:
        st.info("Nenhuma ideia no banco de dados.")
    else:
        # Nota: Para atualizar status no Firestore, precisaríamos do ID do documento. 
        # Como o LNT ainda não está aqui, apenas visualizamos os dados salvos.
        st.write("Dados encontrados no banco:")
        st.table(pd.DataFrame(dados))

# ==========================================
# TELA 3: GESTOR
# ==========================================
elif perfil_atual == "3. Gestor":
    st.title("✅ Fila de Aprovação Executiva")
    st.info("Aguardando os campos do LNT para implementar a lógica de aprovação.")