import streamlit as st
# from authlib.integrations.requests_client import OAuth2Session
# import requests

# 🔐 Credenciais do Google OAuth
# CLIENT_ID = "SEU_CLIENT_ID"
# CLIENT_SECRET = "SEU_CLIENT_SECRET"
# REDIRECT_URI = "http://localhost:8501"  # ou seu domínio Streamlit Cloud

# 🔎 Endpoints do Google
# AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
# TOKEN_URL = "https://oauth2.googleapis.com/token"
# USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# 🎯 Escopos de acesso
# SCOPE = "openid email profile"

# ✅ Lista de e-mails autorizados
# EMAILS_AUTORIZADOS = ["rogerio@empresa.com", "admin@empresa.com"]

def login():
    """Autenticação desativada temporariamente."""
    # if "autenticado" not in st.session_state:
    #     st.session_state["autenticado"] = False

    # if "token" not in st.session_state:
    #     oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    #     auth_url, state = oauth.create_authorization_url(AUTH_URL)
    #     st.session_state["state"] = state
    #     st.markdown(f"[🔐 Clique aqui para entrar com Google]({auth_url})")

    # # Verifica se voltou com código
    # query_params = st.query_params
    # if "code" in query_params:
    #     code = query_params["code"][0]
    #     oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    #     token = oauth.fetch_token(TOKEN_URL, code=code)
    #     st.session_state["token"] = token

    #     # Busca dados do usuário
    #     access_token = token["access_token"]
    #     resp = requests.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    #     userinfo = resp.json()
    #     st.session_state["email"] = userinfo["email"]

    #     # Verifica se está autorizado
    #     if st.session_state["email"] in EMAILS_AUTORIZADOS:
    #         st.session_state["autenticado"] = True
    #         st.success(f"✅ Autenticado como {st.session_state['email']}")
    #     else:
    #         st.session_state["autenticado"] = False
    #         st.error("❌ E-mail não autorizado.")

    # Força como autenticado para uso temporário
    st.session_state["autenticado"] = True
    st.session_state["email"] = "acesso_livre@temporario.com"

def verificar_autenticacao():
    """Bloqueio desativado temporariamente."""
    # if not st.session_state.get("autenticado", False):
    #     st.warning("⚠️ Você precisa estar logado com uma conta autorizada.")
    #     st.stop()
    pass
