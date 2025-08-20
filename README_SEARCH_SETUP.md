# 📋 RAG Search-Only Setup Guide

## ✅ Đã hoàn thành

### 1. **Kiểm tra cấu trúc dữ liệu Excel**
- ✅ File Excel của bạn có **160 dòng dữ liệu** với đúng cấu trúc
- ✅ Có đầy đủ 6 cột bắt buộc: `_id`, `title`, `current_price`, `product_promotion`, `product_specs`, `color_options`
- ✅ Đã convert thành file CSV tại `data/dienthoai_rag.csv`

### 2. **Cài đặt môi trường Search-Only**
- ✅ Tạo script `setup_search_only.py` - RAG search không cần LLM APIs
- ✅ Tạo script `test_search.py` - Test tìm kiếm
- ✅ Sửa imports để bỏ qua các dependencies LLM không cần thiết
- ✅ Cài đặt các packages cần thiết

## 🎯 Cấu trúc dữ liệu đã xác nhận

```
Dữ liệu sản phẩm điện thoại có 6 trường:

1. _id: ID duy nhất (string)
2. title: Tên sản phẩm 
3. current_price: Giá bán (VNĐ)
4. product_promotion: Khuyến mãi/ưu đãi
5. product_specs: Thông số kỹ thuật
6. color_options: Tùy chọn màu sắc

Ví dụ:
- _id: "666baeb9c0cb52f511d9cb8f"
- title: "Điện thoại iPhone iPhone 15 (128GB) - Chính hãng VN/A"
- current_price: "22.878.334 ₫"
- product_promotion: "Voucher giảm 300.000đ cho đơn từ 5 triệu..."
- product_specs: "Màn hình: 6.1 inch OLED, RAM: 8GB..."
- color_options: ["Vàng", "Hồng", "Đen", "Trắng"]
```

## 🚀 Hướng dẫn sử dụng

### **Chạy tìm kiếm đơn giản:**
```bash
cd retrieval-backend-with-rag
python setup_search_only.py --query "iPhone 15 có những màu gì"
```

### **Chạy interactive mode:**
```bash
python setup_search_only.py
```

### **Test toàn bộ hệ thống:**
```bash
python test_search.py
```

## 🔧 Packages đã cài đặt

```
sentence-transformers==5.1.0
chromadb>=1.0.20
pandas>=2.3.0
numpy>=2.3.0
scikit-learn>=1.7.0
torch>=2.8.0
transformers>=4.55.0
pymongo>=4.14.0
qdrant-client>=1.15.0
openpyxl>=3.1.0
```

## 🎯 Tính năng Search-Only

- ✅ **Vector Search**: Tìm kiếm semantic với embedding model
- ✅ **ReRanking**: Cải thiện độ chính xác kết quả 
- ✅ **ChromaDB**: Local vector database
- ✅ **No LLM APIs**: Không cần API key của OpenAI, Gemini, etc.
- ✅ **Multi-format**: Hỗ trợ ChromaDB, MongoDB, Qdrant

## 📝 Cách test

### **Test cơ bản:**
```python
from setup_search_only import SearchOnlyRAG

# Khởi tạo
search_rag = SearchOnlyRAG()

# Tìm kiếm
results = search_rag.search("iPhone 15 có những màu gì", limit=3)
print(results)
```

### **Test queries mẫu:**
- "iPhone 15 có những màu gì"
- "giá điện thoại iPhone 14"
- "khuyến mãi iPhone"
- "điện thoại Samsung dưới 10 triệu"

## 🔨 Nếu gặp lỗi dependencies

Chạy lệnh sau để cài lại toàn bộ:
```bash
pip install --force-reinstall sentence-transformers chromadb pandas numpy scikit-learn torch transformers pymongo qdrant-client openpyxl
```

## 📊 Kết quả Search

Mỗi kết quả trả về sẽ có:
```json
{
  "query": "iPhone 15 có những màu gì",
  "results": [
    {
      "_id": "666baeb9c0cb52f511d9cb8f",
      "combined_information": "title: Điện thoại iPhone iPhone 15...",
      "score": 0.8234,
      "rerank_score": 0.9156,
      "rank": 1
    }
  ],
  "total_found": 3
}
```

## 🎉 Tóm tắt

**Bạn đã có:**
1. ✅ Dữ liệu hoàn chỉnh 160 sản phẩm điện thoại
2. ✅ Hệ thống RAG search hoạt động độc lập (không cần LLM APIs)
3. ✅ Vector database với ChromaDB
4. ✅ ReRanking để cải thiện độ chính xác
5. ✅ Scripts test và demo

**Sẵn sàng sử dụng cho:**
- Tìm kiếm sản phẩm theo ngữ nghĩa
- Demo hệ thống RAG
- Benchmark và evaluation
- Tích hợp vào ứng dụng web

