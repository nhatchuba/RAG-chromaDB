# 🚀 Hướng dẫn đẩy code lên GitHub

## Bước 1: Tạo Repository trên GitHub

1. **Truy cập GitHub**: https://github.com/nhatchuba
2. **Click "New Repository"** (nút màu xanh)
3. **Điền thông tin**:
   - Repository name: `RAG-chromaDB` 
   - Description: `🤖 Vietnamese Phone Search System using RAG + ChromaDB with Natural Language Response`
   - ✅ Public (để mọi người xem được)
   - ❌ KHÔNG tick "Add a README file" (vì đã có rồi)
   - ❌ KHÔNG tick "Add .gitignore" (vì đã có rồi)
4. **Click "Create repository"**

## Bước 2: Copy Remote URL

Sau khi tạo xong, GitHub sẽ hiện trang với URL như:
```
https://github.com/nhatchuba/RAG-chromaDB.git
```

## Bước 3: Chạy lệnh push

Mở PowerShell tại thư mục này và chạy:

```bash
git remote add origin https://github.com/nhatchuba/RAG-chromaDB.git
git push -u origin main
```

## Bước 4: Xác thực GitHub

Khi push lần đầu, GitHub sẽ yêu cầu đăng nhập:
- **Username**: nhatchuba
- **Password**: Sử dụng Personal Access Token (không phải password thường)

### Tạo Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → Classic
3. Chọn scopes: `repo`, `workflow`
4. Copy token và sử dụng làm password

## ✅ Hoàn thành!

Repository sẽ có URL: https://github.com/nhatchuba/RAG-chromaDB

## 📋 Checklist
- [ ] Tạo repository trên GitHub
- [ ] Copy remote URL  
- [ ] Add remote origin
- [ ] Push code lên main branch
- [ ] Kiểm tra repository online

## 🎯 Next Steps
- Thêm GitHub Actions cho CI/CD
- Tạo GitHub Pages cho demo
- Setup Issues templates
- Thêm Contributing guidelines
