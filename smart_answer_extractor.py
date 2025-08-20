#!/usr/bin/env python3
"""
Smart Answer Extractor for RAG Search Results
Extracts specific information based on query intent
"""

import re
import json
from typing import Dict, List, Any
from natural_answer_generator import NaturalAnswerGenerator

class SmartAnswerExtractor:
    def __init__(self):
        self.natural_generator = NaturalAnswerGenerator()
        self.query_patterns = {
            'price': [
                r'giá.*?(?:bao nhiêu|là gì|của|bán)',
                r'bao nhiêu.*?giá',
                r'(?:chi phí|giá tiền|giá cả|giá bán)',
                r'(?:price|cost)',
                r'(?:tiền|đồng|vnd)'
            ],
            'color': [
                r'màu.*?(?:gì|nào|có|sắc)',
                r'(?:có.*?màu|màu sắc|tùy chọn màu)',
                r'(?:color|colours?)',
                r'(?:phiên bản màu|lựa chọn màu)'
            ],
            'specs': [
                r'(?:thông số|cấu hình|specs?|chi tiết)',
                r'(?:RAM|bộ nhớ|memory|GB)',
                r'(?:camera|máy ảnh|MP)',
                r'(?:pin|battery|mAh)',
                r'(?:màn hình|screen|display|inch)',
                r'(?:chip|processor|CPU)',
                r'(?:thông tin kỹ thuật|tính năng)'
            ],
            'promotion': [
                r'(?:khuyến mãi|ưu đãi|giảm giá|sale)',
                r'(?:promotion|sale|discount)',
                r'(?:voucher|giảm|tặng|quà)',
                r'(?:chương trình|combo|deal)'
            ],
            'general_info': [
                r'(?:thông tin|chi tiết|về)',
                r'(?:giới thiệu|mô tả|review)',
                r'(?:như thế nào|ra sao|gì)'
            ]
        }
        
        # Template responses cho từng loại câu hỏi
        self.response_templates = {
            'price': {
                'fields': ['title', 'current_price', 'color_options'],
                'format': '📱 **{title}**\n💰 **Giá bán**: {current_price}\n🎨 **Màu sắc**: {color_options}'
            },
            'color': {
                'fields': ['title', 'color_options', 'current_price'],
                'format': '📱 **{title}**\n🎨 **Màu sắc có sẵn**: {color_options}\n💰 **Giá**: {current_price}'
            },
            'specs': {
                'fields': ['title', 'product_specs', 'current_price'],
                'format': '📱 **{title}**\n📋 **Thông số kỹ thuật**: {product_specs}\n💰 **Giá**: {current_price}'
            },
            'promotion': {
                'fields': ['title', 'product_promotion', 'current_price'],
                'format': '📱 **{title}**\n🎁 **Khuyến mãi**: {product_promotion}\n💰 **Giá**: {current_price}'
            },
            'general_info': {
                'fields': ['title', 'current_price', 'color_options', 'product_specs'],
                'format': '📱 **{title}**\n💰 **Giá**: {current_price}\n🎨 **Màu sắc**: {color_options}\n📋 **Thông số**: {product_specs}'
            }
        }
    
    def detect_query_intent(self, query: str) -> str:
        """Detect what the user is asking about"""
        query_lower = query.lower()
        
        # Tăng độ ưu tiên cho các intent cụ thể
        intent_scores = {}
        
        for intent, patterns in self.query_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, query_lower)
                score += len(matches)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            # Trả về intent có điểm cao nhất
            return max(intent_scores, key=intent_scores.get)
        
        return 'general_info'
    
    def extract_field_data(self, result: Dict[str, Any]) -> Dict[str, str]:
        """Extract all structured data fields from result"""
        content = result.get('combined_information', '')
        
        # Regex patterns for each field
        field_patterns = {
            'title': r'title:\s*([^,]+)',
            'current_price': r'current_price:\s*([^,]+)', 
            'color_options': r'color_options:\s*(\[.*?\])',
            'product_specs': r'product_specs:\s*([^,]+(?:,[^,]*)*)',
            'product_promotion': r'product_promotion:\s*([^,]+(?:,[^,]*)*)'
        }
        
        extracted_data = {}
        for field, pattern in field_patterns.items():
            match = re.search(pattern, content)
            if match:
                value = match.group(1).strip()
                
                # Special processing for color_options
                if field == 'color_options' and value.startswith('['):
                    try:
                        colors = eval(value)
                        if isinstance(colors, list):
                            value = ", ".join(colors)
                    except:
                        value = value.strip('[]').replace("'", "").replace('"', '')
                
                # Limit length for long fields
                if field in ['product_specs', 'product_promotion'] and len(value) > 200:
                    value = value[:200] + "..."
                
                extracted_data[field] = value
            else:
                # Default values
                defaults = {
                    'title': 'Sản phẩm',
                    'current_price': 'Liên hệ',
                    'color_options': 'Không có thông tin',
                    'product_specs': 'Không có thông tin',
                    'product_promotion': 'Không có khuyến mãi'
                }
                extracted_data[field] = defaults.get(field, 'Không có thông tin')
        
        return extracted_data
    
    def format_structured_answer(self, intent: str, data: Dict[str, str]) -> Dict[str, Any]:
        """Format structured answer based on intent and extracted data"""
        template = self.response_templates.get(intent, self.response_templates['general_info'])
        
        # Format the answer using template
        try:
            formatted_answer = template['format'].format(**data)
        except KeyError as e:
            # Fallback if any field is missing
            formatted_answer = f"📱 **{data.get('title', 'Sản phẩm')}**\n"
            for field in template['fields']:
                if field in data:
                    field_icons = {
                        'current_price': '💰',
                        'color_options': '🎨', 
                        'product_specs': '📋',
                        'product_promotion': '🎁'
                    }
                    icon = field_icons.get(field, '📍')
                    field_name = {
                        'current_price': 'Giá',
                        'color_options': 'Màu sắc',
                        'product_specs': 'Thông số',
                        'product_promotion': 'Khuyến mãi'
                    }.get(field, field)
                    formatted_answer += f"{icon} **{field_name}**: {data[field]}\n"
        
        # Create structured data for display
        structured_fields = []
        for field in template['fields']:
            if field in data and field != 'title':
                field_info = {
                    'key': field,
                    'label': {
                        'current_price': 'Giá bán',
                        'color_options': 'Màu sắc',
                        'product_specs': 'Thông số kỹ thuật',
                        'product_promotion': 'Khuyến mãi'
                    }.get(field, field),
                    'value': data[field],
                    'icon': {
                        'current_price': '💰',
                        'color_options': '🎨',
                        'product_specs': '📋', 
                        'product_promotion': '🎁'
                    }.get(field, '📍')
                }
                structured_fields.append(field_info)
        
        return {
            'formatted_text': formatted_answer,
            'structured_fields': structured_fields,
            'product_title': data.get('title', 'Sản phẩm')
        }
    
    def extract_smart_answer(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract smart answer based on query intent"""
        if not results:
            return {
                'type': 'no_results',
                'answer': 'Không tìm thấy kết quả phù hợp.',
                'structured_fields': []
            }
        
        # Get the best result (highest score)
        best_result = max(results, key=lambda x: x.get('rerank_score', x.get('score', 0)))
        
        # Detect intent
        intent = self.detect_query_intent(query)
        
        # Extract structured data
        extracted_data = self.extract_field_data(best_result)
        
        # Format answer based on intent
        formatted_response = self.format_structured_answer(intent, extracted_data)
        
        # Tạo câu trả lời tự nhiên như CSKH
        natural_answer = self.natural_generator.generate_natural_answer(intent, extracted_data)
        natural_variants = self.natural_generator.generate_multiple_variants(intent, extracted_data, 3)
        
        return {
            'type': intent,
            'answer': formatted_response['formatted_text'],
            'natural_answer': natural_answer,
            'natural_variants': natural_variants,
            'structured_fields': formatted_response['structured_fields'],
            'product_title': formatted_response['product_title'],
            'best_result': best_result,
            'intent': intent,
            'confidence': best_result.get('rerank_score', best_result.get('score', 0)),
            'extracted_data': extracted_data
        }

