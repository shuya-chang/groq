import os

import streamlit as st
from groq import APIConnectionError, APIStatusError, AuthenticationError, Groq, RateLimitError

st.set_page_config(page_title="Groq 聊天室", page_icon="💬")
st.title("💬 Groq 聊天室")
st.caption("Streamlit × Groq · OpenAI GPT-OSS 120B · v1.0.0")


def configured_api_key():
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets.get("GROQ_API_KEY", "")).strip()
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return ""


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("聊天設定")
    entered_key = st.text_input("Groq API Key（選填）", type="password", help="可在此輸入自己的金鑰，或由管理員設定 GROQ_API_KEY。")
    api_key = entered_key.strip() or configured_api_key()
    st.caption("模型：openai/gpt-oss-120b")
    if st.button("新聊天", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("聊天紀錄只保留於目前工作階段；內容會送至 Groq 產生回覆。")

if not api_key:
    st.info("請先在側邊欄輸入 Groq API Key，或於部署平台的 Secrets 設定 GROQ_API_KEY。")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("請輸入您的訊息", disabled=not bool(api_key), max_chars=8000)
if user_input and user_input.strip():
    user_message = {"role": "user", "content": user_input.strip()}
    with st.chat_message("user"):
        st.markdown(user_message["content"])
    # 只傳送最近十輪已完成的對話，避免歷史無限制增長。
    messages = st.session_state.messages[-20:] + [user_message]
    try:
        with st.spinner("正在思考…"):
            with Groq(api_key=api_key, timeout=45.0, max_retries=1) as client:
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages,
                    temperature=0.7,
                    max_completion_tokens=2048,
                    stream=False,
                )
            response = completion.choices[0].message.content
            if not response or not response.strip():
                st.warning("模型未回傳文字，請重新送出或縮短問題。")
            else:
                st.session_state.messages.extend([user_message, {"role": "assistant", "content": response}])
                with st.chat_message("assistant"):
                    st.markdown(response)
    except AuthenticationError:
        st.error("API Key 無效或已失效，請檢查金鑰。")
    except RateLimitError:
        st.error("已達 Groq 使用額度或速率限制，請稍後再試。")
    except APIConnectionError:
        st.error("暫時無法連線至 Groq，請稍後重試。")
    except APIStatusError as exc:
        st.error(f"Groq 暫時無法完成請求（HTTP {exc.status_code}），請縮短訊息或稍後重試。")
    except Exception:
        st.error("無法完成這次請求，請重新送出；若持續發生，請管理員檢查套件與部署設定。")
