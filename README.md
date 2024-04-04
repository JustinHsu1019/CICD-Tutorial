# CI/CD Tutorial

這份教學將展示如何利用 GitHub、PythonAnywhere 以及 Flask 應用來實現一個簡單的 CI/CD 流程。我們將通過 GitHub Actions 自動化更新 PythonAnywhere 上的 Flask 應用。

## 前提條件

- 一個 GitHub 帳號。
- 一個 PythonAnywhere 帳號。
- 有基本的 Git、Python 和 Flask 知識。

## 步驟 1: 準備 GitHub 專案

1. 在 GitHub 上 Fork 我的這個專案。
2. 將此 GitHub 專案 Clone 到本地。

## 步驟 2: 配置 GitHub Secrets

1. 在 GitHub 專案的 `Settings` -> `Secrets` 頁面中，新增一個名為 `FLASK_APP_TOKEN` 的 secret。這個值將用於 Flask 應用的身份驗證，確保只有擁有 token 的請求才能觸發更新操作 (這個值可以用 Scripts/gen_key.py 生成)

## 步驟 3: 配置 GitHub Actions

1. 在 GitHub 專案中，已有一個 `.github/workflows/update_server.yml` 檔案，並將 CI/CD 流程的配置填寫於此。
2. 這個 workflow 應當被設置為在每次推送到 master 分支時觸發，並執行更新 Flask 應用的操作。

## 步驟 4: 在 PythonAnywhere 上設置專案

1. 使用 SSH 或 PythonAnywhere 的 Bash Console 登入到你的 PythonAnywhere 帳號。
2. 克隆 GitHub 上的專案到 PythonAnywhere，並在專案目錄下運行 `pip install -r requirements.txt` 安裝依賴。
3. 在 PythonAnywhere 的 `Account` 頁面生成一個新的 API token，並記下來。

## 步驟 5: 配置 Flask 應用

1. 在 PythonAnywhere 的專案目錄中，新增一個 `config.ini` 檔案，並根據 PythonAnywhere 的配置填寫相關信息。

```ini
[pythonanywhere]
username = <你的 PythonAnywhere 用戶名>
api_token = <你的 PythonAnywhere API token>
domain_name = <你的 PythonAnywhere 應用域名>
github_secret = <與 GitHub Secrets 中 FLASK_APP_TOKEN 相匹配的值>
```

## 步驟 6: 啟動 Flask 應用
1. 在 PythonAnywhere 的 Web 頁面配置並啟動 Flask 應用。

## 步驟 7: 驗證 CI/CD 流程
1. 在本地對 Flask 應用進行一些小修改。
2. 將修改推送到 GitHub 上。
3. 觀察 GitHub Actions 的運行情況，檢查是否自動觸發了 PythonAnywhere 上 Flask 應用的更新。
4. 如果一切配置正確，你現在應該已經擁有一個可以自動反映 GitHub 上變動到 PythonAnywhere 上 Flask 應用的 CI/CD 流程。
