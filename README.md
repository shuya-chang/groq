# Groq 聊天室

以 Streamlit 與 Groq Python SDK 建立的聊天網站，主程式為 `groqtest.py`，模型為 `openai/gpt-oss-120b`。目前版本：**1.0.0**。

## 本機執行（建議 Python 3.11）

在本資料夾開啟終端機：

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run groqtest.py
```

開啟終端機顯示的網站網址，在側邊欄貼上自己的 Groq API Key 即可聊天。
金鑰可從 https://console.groq.com/keys 建立。請勿把金鑰寫入程式或提交到 GitHub。

也可在啟動前設定環境變數：

```powershell
$env:GROQ_API_KEY="你的金鑰"
```

或在本機建立 `.streamlit/secrets.toml`（已由 `.gitignore` 排除）：

```toml
GROQ_API_KEY = "你的金鑰"
```

金鑰優先順序：側邊欄輸入 → 環境變數 → Streamlit Secrets。

## GitHub 與 Streamlit Community Cloud 部署

1. 將 `groqtest.py`、`requirements.txt`、`.gitignore`、`README.md`、`VERSION.txt` 上傳至 GitHub 儲存庫根目錄。
2. 登入 https://share.streamlit.io/，選擇建立應用程式並指定該 GitHub 儲存庫與分支。
3. Main file path 填入 `groqtest.py`，Python 選擇 3.11。
4. 如需由管理員提供金鑰，在 Advanced settings 的 Secrets 填入上面的 TOML 設定；也可留空，讓每位使用者自行在側邊欄輸入。
5. 按 Deploy，等待安裝完成後使用產生的 `.streamlit.app` 網址。

若提供共用金鑰，網站訪客的請求會使用該金鑰的額度，請依需求限制網站存取。

## 使用方式與資料

- 支援連續對話與「新聊天」清除紀錄。
- 每則輸入最多 8,000 字元；每次傳送最近十輪完整對話與本次問題。
- 聊天紀錄保留於目前 Streamlit 工作階段，重新連線後可能重置，沒有資料庫或持久化儲存。
- 訊息會送至 Groq API；請依自己的隱私需求決定輸入內容。
- 失敗請求不會寫入聊天紀錄，請重新送出問題。
- 沒有啟用搜尋或外部工具，回答不代表即時網路資訊。

## 常見問題

- **無法輸入訊息**：先輸入 API Key，或設定環境變數／Secrets。
- **金鑰無效**：至 Groq Console 確認金鑰，避免貼入多餘引號。
- **額度或速率限制**：稍後再試，並至 Groq Console 檢查額度。
- **部署找不到套件**：確認 `requirements.txt` 與主程式位於同一個儲存庫根目錄。

## 官方文件

- [Groq 模型](https://console.groq.com/docs/models)
- [Groq Python SDK](https://github.com/groq/groq-python)
- [Streamlit 部署](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Streamlit Secrets](https://docs.streamlit.io/deploy/concepts/secrets)

版本變更請見 `VERSION.txt`。
