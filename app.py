import streamlit as st
from datetime import datetime

# Configuração da página para parecer um aplicativo de Tablet
st.set_page_config(page_title="ORION - O-Ring Check", page_icon="📱", layout="centered")

# Estilização em Vermelho/Vinho e Cinza Escuro (Identidade Visual da Consultoria)
st.markdown("""
    <style>
    .main-title { color: #800020; font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .section-box { padding: 15px; border-radius: 5px; background-color: #f5f5f5; border-left: 5px solid #800020; margin-bottom: 15px; }
    .section-title { color: #800020; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    .stButton>button { background-color: #800020; color: white; width: 100%; border-radius: 5px; font-weight: bold; }
    .stButton>button:hover { background-color: #4a0012; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📱 REGISTRO DE INSTALAÇÃO DE SELOS</div>', unsafe_allow_html=True)

# --- SEÇÃO 1: IDENTIFICAÇÃO DO EQUIPAMENTO ---
st.markdown('<div class="section-box"><div class="section-title">1. Identificação do Equipamento</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    equipamento = st.selectbox("Descrição do Equipamento", ["Drain Valve 5\"", "Gate Valve", "Choke Valve", "Outro"])
    pn_equip = st.text_input("Part Number (P/N Equipamento)", placeholder="Ex: PN-9923")
with col2:
    sap_id = st.text_input("SAP ID / Tool ID (Simulação de QR Code)", placeholder="Ex: SAP-88341")
    # Pressão fixa conforme o formulário original de alta pressão
    st.metric(label="Pressão Máxima de Trabalho", value="9,701 PSI")
st.markdown('</div>', unsafe_allow_html=True)

# --- SEÇÃO 2: DADOS DO SELO / O-RING ---
st.markdown('<div class="section-box"><div class="section-title">2. Dados do Selo / O-Ring</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    pn_selo = st.text_input("Part Number do Selo", placeholder="Ex: PN-ORING-90")
    composto = st.selectbox("Material / Composto", ["Viton", "Nitrílica", "HNBR"])
    cure_date = st.date_input("Cure Date (Data de Fab.)")
with col4:
    trace_number = st.text_input("Trace Number (Lote)", placeholder="Ex: LOT-2026-09A")
    dureza = st.text_input("Dureza (Shore)", value="90 Shore")
    shelf_life = st.date_input("Shelf Life (Validade)")
st.markdown('</div>', unsafe_allow_html=True)

# --- SEÇÃO 3: CHECKLIST DE PREPARAÇÃO ---
st.markdown('<div class="section-box"><div class="section-title">3. Checklist de Preparação e Instalação</div>', unsafe_allow_html=True)
ch1 = st.checkbox("1. Limpeza da ranhura/alojamento executada e livre de resíduos antigos.")
ch2 = st.checkbox("2. Inspeção visual dimensional da ranhura realizada (sem riscos ou danos).")
ch3 = st.checkbox("3. Selo/O-ring verificado fisicamente (ausência de rebarbas, cortes).")
ch4 = st.checkbox("4. Lubrificação adequada aplicada no selo utilizando composto compatível.")
ch5 = st.checkbox("5. Assentamento correto do selo na ranhura sem torções ou esmagamento.")
st.markdown('</div>', unsafe_allow_html=True)

# --- SEÇÃO 4: EVIDÊNCIAS DIGITAIS OBRIGATÓRIAS (CÂMERA DO TABLET) ---
st.markdown('<div class="section-box"><div class="section-title">4. Evidências Digitais Obrigatórias</div>', unsafe_allow_html=True)
st.warning("O aplicativo utiliza a câmera nativa. Fotos da galeria estão bloqueadas no código.")

foto1 = st.camera_input("📸 Foto 1: Embalagem do Selo (P/N e Lote)")
foto2 = st.camera_input("📸 Foto 2: Alojamento Limpo e Inspecionado")
foto3 = st.camera_input("📸 Foto 3: Selo Instalado e Lubrificado")
st.markdown('</div>', unsafe_allow_html=True)

# --- VALIDAÇÃO RESTRITA E FECHAMENTO ---
checklist_aprovado = ch1 and ch2 and ch3 and ch4 and ch5
fotos_aprovadas = foto1 is not None and foto2 is not None and foto3 is not None

st.markdown('<div class="section-box"><div class="section-title">5. Encerramento e Assinatura</div>', unsafe_allow_html=True)
assinatura = st.text_input("Assinatura Digital do Técnico (Digite o Nome Completo para Validar)")

# Trava lógica: o botão só processa se tudo estiver cumprido
if checklist_aprovado and fotos_aprovadas and assinatura:
    if st.button("💾 ENVIAR REGISTRO (CONFORME)"):
        # Simulação dos metadados e salvamento local seguro (PO-13)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.success(f"Sucesso! Registro transmitido em {timestamp}.")
        st.info("Arquivo JSON estruturado localmente. Pronto para espelhamento em Excel ou conector SAP.")
        
        # Mostra o formato de dado universal gerado nos bastidores
        st.json({
            "status": "CONFORME",
            "equipamento_id": sap_id,
            "pressao_teste": "9701 PSI",
            "lote_selo": trace_number,
            "operador": assinatura,
            "data_registro": timestamp
        })
else:
    st.error("❌ BOTÃO BLOQUEADO: Preencha todo o checklist e capture as 3 fotos obrigatórias para liberar o envio.")
st.markdown('</div>', unsafe_allow_html=True)