import streamlit as st
import requests

# 讀取 API URL
OLLAMA_API_URL = st.secrets["OLLAMA_API_URL"]

st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖")
st.title("💬 Ollama Chatbot")

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 顯示歷史訊息
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 使用者輸入
if prompt := st.chat_input("請輸入訊息..."):
    # 顯示使用者訊息
    st.chat_message("user").markdown(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # 呼叫 Ollama API
    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json={"model": "llama2", "prompt": prompt},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        reply = data.get("response", "（無回覆）")
    except Exception as e:
        reply = f"❌ 無法連接 Ollama API: {e}"

    # 顯示模型回覆
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state["messages"].append({"role": "assistant", "content": reply})
