import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="個人萬用 AI 智慧戰情室", layout="wide")
st.title("🤖 個人萬用 AI 智慧戰情室")
st.write("這是一套專屬於你的萬用 AI 助理。不管是查資料、寫程式、處理報告或任何日常問題，直接在下方對話框輸入即可！")

# 側邊欄：API 金鑰設定與檔案上傳
with st.sidebar:
    st.header("🔑 系統設定")
    # 如果你在 Streamlit 雲端有設定 Secrets，它會自動抓取；否則可以在這裡手動輸入
    api_key_input = st.text_input("請輸入你的 Google Gemini API 金鑰 (AQ開頭)", type="password")
    
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        genai.configure(api_key=api_key_input)
        st.success("✅ API 金鑰已載入！")
    
    st.markdown("---")
    st.header("📂 檔案參考區")
    uploaded_files = st.file_uploader("上傳任何檔案供 AI 閱讀", type=["docx", "csv", "txt", "pdf", "png", "jpg"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
        st.success("✅ 檔案上傳成功！")

# 初始化聊天紀錄
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 顯示歷史對話
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 使用者輸入框
if prompt := st.chat_input("隨便問吧！不管是查天氣、寫程式、或是任何你想解決的問題..."):
    if not api_key_input and "GEMINI_API_KEY" not in os.environ:
        st.error("⚠️ 請先在左側側邊欄輸入你的 Google Gemini API 金鑰！")
    else:
        # 顯示使用者訊息
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 呼叫 Gemini 大腦生成回覆
        with st.chat_message("assistant"):
            with st.spinner("🧠 AI 正在思考中..."):
                try:
                    # 使用目前 Google 支援的標準智慧模型
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    
                    reply = response.text
                    st.markdown(reply)
                    
                    # 紀錄 AI 回覆
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"發生錯誤：{str(e)}")
