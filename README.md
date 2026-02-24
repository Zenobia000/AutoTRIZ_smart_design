# RD Design Copilot MVP v0.5

AI 輔助早期概念設計系統，從「模糊需求」到「可審查的 KT 決策記錄」。

## 快速啟動

### 本地開發

```bash
# 1. 安裝依賴
pip install -e ".[dev]"

# 2. 設定環境變數
cp .env.example .env
# 編輯 .env，填入 ANTHROPIC_API_KEY

# 3. 啟動後端 (terminal 1)
uvicorn src.main:app --port 8000 --reload

# 4. 啟動前端 (terminal 2)
streamlit run ui/app.py --server.port 8501
```

### Docker

```bash
cp .env.example .env
# 編輯 .env
docker-compose up
```

瀏覽器開啟 http://localhost:8501

## 架構

```
Streamlit (8501) → FastAPI (8000) → SQLite + Claude API
```

## 三階段流程

1. **Phase I** — 定義問題空間：任務定義表 → 索克拉底問答 → TRIZ 矛盾識別
2. **Phase II** — 假設與發散：假設台帳 → TRIZ 解法 → SCAMPER 變形 → 方案集合 → MUST 篩選
3. **Phase III** — 收斂與驗證：WANT 評分 → 風險評估 → KT 決策記錄 → 最小實驗

每階段有 Gate 檢查點，通過才進入下一階段。

## API 文件

啟動後端後訪問 http://localhost:8000/docs

## 測試

```bash
pytest tests/ -v
```

## 技術堆疊

- Python 3.11+ / FastAPI / SQLAlchemy 2.0 / SQLite
- Claude API (claude-sonnet-4-6) / Streamlit / Pydantic 2.0
