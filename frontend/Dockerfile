# 使用輕量級 Node.js 版本
FROM node:14

# 設定工作目錄
WORKDIR /app

# 複製 package.json 並安裝依賴
COPY package.json package-lock.json ./
RUN npm install

# 複製所有項目文件
COPY . .

# 構建 React 應用
RUN npm run build

# 安裝 `serve`，並提供 `build` 目錄作為靜態文件服務
RUN npm install -g serve
CMD ["npx", "serve", "-s", "build", "-l", "80"]

# 暴露 80 端口
EXPOSE 80
