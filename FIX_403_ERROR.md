# 🔧 Cách fix lỗi 403 khi push lên GitHub

## ❌ Lỗi 403 - Forbidden

GitHub không cho phép sử dụng password thông thường để push code từ tháng 8/2021. Bạn cần sử dụng **Personal Access Token**.

## ✅ Giải pháp: Tạo Personal Access Token

### Bước 1: Tạo Token trên GitHub
1. **Đăng nhập GitHub**: https://github.com/nhatchuba
2. **Click avatar** (góc phải) → **Settings**
3. **Sidebar trái** → **Developer settings** 
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**

### Bước 2: Cấu hình Token
- **Note**: `RAG-chromaDB-push-token`
- **Expiration**: `90 days` (hoặc `No expiration`)
- **Scopes** (tick những mục này):
  - ✅ `repo` (Full control of private repositories)
  - ✅ `workflow` (Update GitHub Action workflows)

### Bước 3: Copy Token
- Click **Generate token**
- 🚨 **QUAN TRỌNG**: Copy token ngay (chỉ hiện 1 lần)
- Ví dụ: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Bước 4: Push với Token
```bash
# Thay <YOUR_TOKEN> bằng token vừa copy
git remote set-url origin https://nhatchuba:<YOUR_TOKEN>@github.com/nhatchuba/RAG-chromaDB.git
git push -u origin main
```

## 🔐 Cách khác: Git Credential Manager

### Option 1: Sử dụng Git Credential Manager
```bash
git push -u origin main
```
- Khi hỏi username: `nhatchuba`
- Khi hỏi password: **Paste token** (không phải password GitHub)

### Option 2: Cache credentials
```bash
git config --global credential.helper store
git push -u origin main
```

## 🚨 Lưu ý bảo mật
- **KHÔNG** share token với ai
- **KHÔNG** commit token vào code
- **KHÔNG** để token trong file config
- Nếu token bị lộ → **Revoke** và tạo token mới

## 📝 Backup Plan: GitHub CLI
Nếu vẫn gặp khó khăn, dùng GitHub CLI:
```bash
# Cài GitHub CLI
winget install GitHub.cli

# Đăng nhập
gh auth login

# Push
git push -u origin main
```

## ✅ Xác nhận thành công
Sau khi push thành công, check:
- Repository: https://github.com/nhatchuba/RAG-chromaDB
- Files đã xuất hiện đầy đủ
- README.md hiển thị đẹp
