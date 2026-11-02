import streamlit as st
import subprocess
import os

# 確保 Streamlit 雲端環境有安裝隱形瀏覽器核心
os.system("playwright install chromium")

st.set_page_config(page_title="個人萬用 AI 戰情室", layout="wide")
st.title("🤖 個人萬用 AI 智慧戰情室")
st.write("這是一套不受限制的萬用 AI 助理。不管是查資料、寫程式、處理報告或任何日常問題，直接在下方對話框輸入即可！")

# 側邊欄：檔案隨意上傳區 (不管你要上傳 Word、Excel 還是圖片都可以讓 AI 參考)
with st.sidebar:
    st.header("📂 隨身檔案上傳區")
    st.write("如果有任何檔案需要 AI 幫忙分析或修改，請先上傳到這裡：")
    uploaded_files = st.file_uploader("支援各種格式檔案", type=["docx", "csv", "txt", "png", "jpg", "pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success("✅ 檔案已上傳至伺服器，AI 隨時可以調用！")

    st.markdown("---")
    st.subheader("📥 產出檔案下載區")
    valid_files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.endswith('.py') and not f.startswith('.')]
    for f in valid_files:
        with open(f, "rb") as file:
            st.download_button(label=f"下載 {f}", data=file, file_name=f)

# 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示歷史對話
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 核心萬用輸入框：不管問什麼都可以！
if prompt := st.chat_input("隨便問吧！不管是查天氣、寫程式、或是任何你想解決的問題..."):
    # 紀錄並顯示使用者的話
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 呼叫背景大腦處理
    with st.chat_message("assistant"):
        with st.spinner("🧠 AI 正在全速思考並執行任務中..."):
            try:
                # 呼叫底層 OpenManus 引擎執行指令
                process = subprocess.Popen(
                    ["python", "main.py"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(input=f"{prompt}\n")
                
                # 將結果顯示在網頁上
                if process.returncode == 0:
                    reply_text = "✅ 任務已順利執行完畢！\n\n如果你剛才有要求它產生檔案（例如報表或圖表），請至左側側邊欄的「產出檔案下載區」下載。"
                    st.success(reply_text)
                    st.session_state.messages.append({"role": "assistant", "content": reply_text})
                    
                    # 展開面板顯示詳細過程供參考
                    with st.expander("🛠️ 查看 AI 執行細節"):
                        st.code(stderr[-3000:], language="bash")
                else:
                    error_msg = "⚠️ 執行過程中遇到阻礙（可能是 API 額度用盡或網路逾時），請檢查下方除錯訊息。"
                    st.error(error_msg)
                    with st.expander("查看錯誤詳情"):
                        st.code(stderr, language="bash")
            except Exception as e:
                st.error(f"系統發生異常：{str(e)}")