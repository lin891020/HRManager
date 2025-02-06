# 使用官方 Python 3.10 映像
FROM python:3.10

# 設置工作目錄
WORKDIR /app

# 複製所有應用程式代碼到容器內
COPY . /app

# 安裝依賴
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

# 啟動 FastAPI 應用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
