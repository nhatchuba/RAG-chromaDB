#!/usr/bin/env python3
"""
Natural Answer Generator - Tạo câu trả lời tự nhiên như CSKH
"""

import re
from typing import Dict, List, Any

class NaturalAnswerGenerator:
    def __init__(self):
        # Template câu trả lời tự nhiên cho từng loại câu hỏi
        self.answer_templates = {
            'price': [
                "{product_name} hiện có giá {price}. {color_info}",
                "Giá của {product_name} là {price}, anh/chị có thể lựa chọn {color_info}",
                "{product_name} đang bán với giá {price}. Sản phẩm có {color_info}",
                "Hiện tại {product_name} có giá {price}, {color_info}"
            ],
            'color': [
                "{product_name} có {colors} với giá {price}",
                "Anh/chị có thể chọn {product_name} với các màu {colors}. Giá hiện tại là {price}",
                "{product_name} hiện có {colors}, giá bán {price}",
                "Sản phẩm {product_name} có {colors} để anh/chị lựa chọn, giá {price}"
            ],
            'specs': [
                "{product_name} có {specs}. Giá bán hiện tại là {price}",
                "Thông số của {product_name}: {specs}. Sản phẩm có giá {price}",
                "{product_name} được trang bị {specs}, hiện có giá {price}",
                "Cấu hình {product_name}: {specs}. Giá bán {price}"
            ],
            'promotion': [
                "{product_name} đang có {promotion}. Giá hiện tại {price}",
                "Hiện tại {product_name} có ưu đãi: {promotion}. Giá sản phẩm {price}",
                "{product_name} (giá {price}) đang có chương trình {promotion}",
                "Anh/chị quan tâm {product_name} đúng không? Sản phẩm đang có {promotion}, giá {price}"
            ],
            'general_info': [
                "{product_name} có giá {price}, {colors}, {specs_short}",
                "Sản phẩm {product_name} hiện có giá {price}. Máy có {colors} và {specs_short}",
                "{product_name} đang bán với giá {price}, có {colors}. Cấu hình: {specs_short}",
                "Về {product_name}: giá {price}, màu sắc {colors}, {specs_short}"
            ]
        }
        
        # Cụm từ kết nối tự nhiên
        self.connectors = {
            'price_to_color': [", anh/chị có thể chọn ", ", có sẵn ", ", máy có "],
            'price_to_specs': [" với cấu hình ", ", thông số ", ", được trang bị "],
            'specs_to_price': [". Giá hiện tại ", ". Máy có giá ", ". Bán với giá "]
        }
        
        # Từ khóa để làm ngắn thông số
        self.specs_keywords = ['RAM', 'camera', 'pin', 'màn hình', 'chip', 'bộ nhớ']

    def clean_product_name(self, title: str) -> str:
        """Làm sạch tên sản phẩm"""
        # Loại bỏ "điện thoại" ở đầu
        title = re.sub(r'^điện thoại\s+', '', title, flags=re.IGNORECASE)
        
        # Loại bỏ các từ thừa
        title = re.sub(r'\s*-?\s*chính hãng.*$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*\(.*?\)', '', title)  # Loại bỏ ngoặc đơn
        
        return title.strip()

    def format_colors(self, colors_text: str) -> str:
        """Format màu sắc tự nhiên"""
        if not colors_text or colors_text == "Không có thông tin":
            return "nhiều màu sắc"
        
        # Xử lý danh sách màu
        colors = [c.strip() for c in colors_text.split(',')]
        
        if len(colors) == 1:
            return f"màu {colors[0]}"
        elif len(colors) == 2:
            return f"màu {colors[0]} và {colors[1]}"
        elif len(colors) <= 4:
            return f"các màu {', '.join(colors[:-1])} và {colors[-1]}"
        else:
            return f"{len(colors)} màu sắc khác nhau"

    def extract_key_specs(self, specs: str) -> str:
        """Trích xuất thông số quan trọng"""
        if not specs or specs == "Không có thông tin":
            return "cấu hình tốt"
        
        # Tìm các thông số quan trọng
        key_specs = []
        
        # RAM
        ram_match = re.search(r'RAM:\s*(\d+GB)', specs, re.IGNORECASE)
        if ram_match:
            key_specs.append(f"RAM {ram_match.group(1)}")
        
        # Camera
        camera_match = re.search(r'Camera[^:]*:\s*(\d+MP)', specs, re.IGNORECASE)
        if camera_match:
            key_specs.append(f"camera {camera_match.group(1)}")
        
        # Pin
        battery_match = re.search(r'Pin[^:]*:\s*(\d+mAh)', specs, re.IGNORECASE)
        if battery_match:
            key_specs.append(f"pin {battery_match.group(1)}")
        
        # Màn hình
        screen_match = re.search(r'Màn hình[^:]*:\s*([\d.]+\s*inch)', specs, re.IGNORECASE)
        if screen_match:
            key_specs.append(f"màn hình {screen_match.group(1)}")
        
        if key_specs:
            if len(key_specs) <= 2:
                return ", ".join(key_specs)
            else:
                return f"{key_specs[0]}, {key_specs[1]} và nhiều tính năng khác"
        
        # Fallback: lấy 50 ký tự đầu
        return specs[:50] + ("..." if len(specs) > 50 else "")

    def simplify_promotion(self, promotion: str) -> str:
        """Đơn giản hóa thông tin khuyến mãi"""
        if not promotion or promotion == "Không có khuyến mãi":
            return "ưu đãi hấp dẫn"
        
        # Tìm giảm giá
        discount_match = re.search(r'giảm.*?(\d+[.,]?\d*\s*(?:triệu|nghìn|đồng|₫|%))', promotion, re.IGNORECASE)
        if discount_match:
            return f"giảm {discount_match.group(1)}"
        
        # Tìm voucher
        voucher_match = re.search(r'voucher.*?(\d+[.,]?\d*\s*(?:triệu|nghìn|đồng|₫))', promotion, re.IGNORECASE)
        if voucher_match:
            return f"voucher {voucher_match.group(1)}"
        
        # Tìm từ khóa phổ biến
        if 'trả góp' in promotion.lower():
            return "hỗ trợ trả góp 0%"
        if 'tặng' in promotion.lower():
            return "có quà tặng"
        if 'thu cũ' in promotion.lower():
            return "thu cũ đổi mới"
        
        # Fallback
        return "khuyến mãi đặc biệt"

    def generate_natural_answer(self, intent: str, extracted_data: Dict[str, str]) -> str:
        """Tạo câu trả lời tự nhiên"""
        import random
        
        # Chuẩn bị dữ liệu
        product_name = self.clean_product_name(extracted_data.get('title', 'Sản phẩm'))
        price = extracted_data.get('current_price', 'Liên hệ')
        colors = self.format_colors(extracted_data.get('color_options', ''))
        specs_short = self.extract_key_specs(extracted_data.get('product_specs', ''))
        promotion = self.simplify_promotion(extracted_data.get('product_promotion', ''))
        
        # Chọn template ngẫu nhiên
        templates = self.answer_templates.get(intent, self.answer_templates['general_info'])
        template = random.choice(templates)
        
        # Điền thông tin
        try:
            if intent == 'price':
                if colors != "nhiều màu sắc":
                    color_info = colors
                else:
                    color_info = "nhiều lựa chọn màu sắc"
                answer = template.format(
                    product_name=product_name,
                    price=price,
                    color_info=color_info
                )
            elif intent == 'color':
                answer = template.format(
                    product_name=product_name,
                    colors=colors,
                    price=price
                )
            elif intent == 'specs':
                answer = template.format(
                    product_name=product_name,
                    specs=specs_short,
                    price=price
                )
            elif intent == 'promotion':
                answer = template.format(
                    product_name=product_name,
                    promotion=promotion,
                    price=price
                )
            else:  # general_info
                answer = template.format(
                    product_name=product_name,
                    price=price,
                    colors=colors,
                    specs_short=specs_short
                )
        except KeyError:
            # Fallback nếu template bị lỗi
            answer = f"{product_name} có giá {price}. {colors if colors != 'nhiều màu sắc' else 'Có nhiều màu sắc'}. {specs_short}."
        
        # Thêm lời chào hỏi tự nhiên
        greetings = [
            "Dạ, ",
            "Vâng ạ, ",
            "",  # Không có lời chào
            "Chào anh/chị, ",
        ]
        
        ending_phrases = [
            ". Anh/chị có cần tư vấn thêm không ạ?",
            ". Anh/chị quan tâm sản phẩm này đúng không?",
            ". Có gì thắc mắc anh/chị cứ hỏi nhé!",
            ".",
            " ạ.",
        ]
        
        greeting = random.choice(greetings)
        ending = random.choice(ending_phrases)
        
        return greeting + answer + ending

    def generate_multiple_variants(self, intent: str, extracted_data: Dict[str, str], count: int = 3) -> List[str]:
        """Tạo nhiều biến thể câu trả lời"""
        variants = []
        for _ in range(count):
            answer = self.generate_natural_answer(intent, extracted_data)
            if answer not in variants:
                variants.append(answer)
        
        return variants[:count]
