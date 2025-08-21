# 🤖 RAG + ChromaDB - Vietnamese Phone Search System

Hệ thống tìm kiếm sản phẩm điện thoại thông minh sử dụng RAG (Retrieval-Augmented Generation) với ChromaDB, có giao diện web và khả năng trả lời tự nhiên như CSKH.

## ✨ Tính năng chính

### 🔍 **Vector Search với RAG**
- **Semantic Search**: Tìm kiếm theo ngữ nghĩa, không chỉ từ khóa
- **ChromaDB**: Vector database hiệu năng cao
- **ReRanking**: Cải thiện độ chính xác kết quả
- **Multi-language**: Hỗ trợ tiếng Việt tốt

### 💬 **Smart Answer Generation**
- **Natural Language**: Câu trả lời tự nhiên như CSKH
- **Intent Detection**: Nhận dạng ý định (giá, màu, thông số, khuyến mãi)
- **Structured Extraction**: Trích xuất thông tin theo trường
- **Multiple Variants**: Tạo nhiều cách trả lời khác nhau

### 🌐 **Web Interface**
- **Real-time Search**: Tìm kiếm tức thời
- **Dual Mode**: Trả lời CSKH vs Chi tiết cấu trúc
- **Score Visualization**: Hiển thị độ tin cậy
- **Best Result Highlight**: Làm nổi bật kết quả tốt nhất

## 🚀 Cài đặt nhanh

### 1. **Clone Repository**
```bash
git clone https://github.com/[your-username]/RAG-chromaDB.git
cd RAG-chromaDB
```

### 2. **Cài đặt Dependencies**
```bash
pip install -r requirements_search_only.txt
```

### 3. **Chuẩn bị dữ liệu**
- Đặt file CSV vào thư mục `data/`
- File CSV cần có các cột: `_id`, `title`, `current_price`, `product_promotion`, `product_specs`, `color_options`

### 4. **Chạy Web Interface**
```bash
python web_search_interface.py
```

Truy cập: http://localhost:5000

## 📊 Cấu trúc dữ liệu

### **CSV Format**
```csv
_id,title,current_price,product_promotion,product_specs,color_options
666baeb...,Điện thoại iPhone 15 (128GB),22.878.334 ₫,Voucher giảm 300.000đ...,Màn hình: 6.1 inch OLED...,["Vàng", "Hồng", "Đen", "Trắng"]
```

### **Metadata Structure**
```python
{
    "title": "Tên sản phẩm",
    "current_price": "Giá bán", 
    "product_promotion": "Thông tin khuyến mãi",
    "product_specs": "Thông số kỹ thuật",
    "color_options": "Tùy chọn màu sắc"
}
```

## 🎯 Sử dụng

### **1. Search Only Mode**
```bash
# Tìm kiếm đơn giản
python setup_search_only.py --query "iPhone 15 có những màu gì"

# Interactive mode
python setup_search_only.py

# Test hệ thống
python test_search.py
```

### **2. Web Interface Mode**

**Development Server (Tự động reload khi code thay đổi):**
```bash
# Windows PowerShell (cần dấu ./ ở đầu)
.\start_dev.bat

# Linux/Mac  
chmod +x start_dev.sh
./start_dev.sh

# Hoặc chạy trực tiếp
python run_dev.py
```

**Simple Server (Không auto-reload, ổn định hơn):**
```bash
python simple_server.py
```

**Production Server:**
```bash
python web_search_interface.py
```

**Lưu ý:**
- Nếu gặp lỗi Unicode trên Windows, hãy dùng `simple_server.py`
- PowerShell cần `.\start_dev.bat` thay vì `start_dev.bat`

### **3. API Endpoints**
```bash
# Search API
POST /api/search
{
    "query": "iPhone 15 có những màu gì",
    "limit": 5,
    "use_rerank": true
}

# Sample queries
GET /api/sample_queries

# System status  
GET /api/status
```

## 🧠 Smart Answer Examples

### **Hỏi về giá:**
```
User: "Giá iPhone 15 Pro bao nhiêu?"
AI: "Dạ, iPhone 15 Pro (128GB) hiện có giá 22.878.334 ₫. Anh/chị có thể chọn màu Vàng, Hồng, Đen, Trắng. Anh/chị có cần tư vấn thêm không ạ?"
```

### **Hỏi về màu sắc:**
```
User: "Samsung Galaxy A54 có những màu gì?"
AI: "Chào anh/chị, Samsung Galaxy A54 có màu Đen, Trắng, Xanh và Tím. Giá hiện tại là 8.990.000 ₫ ạ."
```

### **Hỏi về khuyến mãi:**
```
User: "iPhone 14 có ưu đãi gì?"
AI: "iPhone 14 đang có voucher giảm 300.000đ. Giá sản phẩm 19.075.222 ₫. Có gì thắc mắc anh/chị cứ hỏi nhé!"
```

## 🏗️ Kiến trúc hệ thống

```
├── 📁 embeddings/           # Embedding models
├── 📁 llms/                 # LLM integrations  
├── 📁 rag/                  # RAG core logic
├── 📁 re_rank/              # Reranking system
├── 📁 reflection/           # Query processing
├── 📁 semantic_router/      # Intent routing
├── 📁 insert_data/          # Data ingestion
├── 📁 templates/            # Web templates
├── 📁 test/                 # Test suites
├── 📄 web_search_interface.py      # Web server
├── 📄 setup_search_only.py         # Search-only mode
├── 📄 smart_answer_extractor.py    # Answer generation
├── 📄 natural_answer_generator.py  # Natural language
└── 📄 requirements_search_only.txt # Dependencies
```

## ⚡ Performance

- **Search Speed**: < 1s cho 160 sản phẩm
- **Accuracy**: >85% với reranking
- **Languages**: Tiếng Việt, English
- **Scalability**: Hỗ trợ đến 10K+ sản phẩm

## 🛠️ Customization

### **Thêm Intent mới:**
```python
# smart_answer_extractor.py
self.query_patterns['new_intent'] = [
    r'pattern1',
    r'pattern2'
]
```

### **Custom Answer Templates:**
```python
# natural_answer_generator.py  
self.answer_templates['new_intent'] = [
    "Template 1: {product_name} {info}",
    "Template 2: {info} cho {product_name}"
]
```

### **Thay đổi Embedding Model:**
```python
# Trong setup_search_only.py
embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'
```

## 📈 Monitoring & Analytics

- **Query Intent Distribution**: Thống kê loại câu hỏi
- **Response Quality**: Điểm tin cậy trung bình
- **Search Performance**: Thời gian phản hồi
- **User Feedback**: Rating từ người dùng

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- **ChromaDB** - Vector database
- **Sentence Transformers** - Embedding models
- **Alibaba GTE** - Multilingual embeddings
- **Flask** - Web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/[your-username]/RAG-chromaDB/issues)
- **Discussions**: [GitHub Discussions](https://github.com/[your-username]/RAG-chromaDB/discussions)
- **Email**: your.email@domain.com

---

⭐ **Nếu project hữu ích, hãy star repo để ủng hộ nhé!** ⭐