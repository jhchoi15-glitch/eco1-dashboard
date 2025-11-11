#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E-Co1 업무 통합 대시보드 고객사 프레젠테이션 자료 생성기
PDF 및 HTML 형식으로 전문적인 프레젠테이션 자료를 생성합니다.
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from io import BytesIO
import base64

# 한글 폰트 설정 (시스템에 따라 경로 조정 필요)
try:
    # 한글 폰트 경로 설정 (Linux 환경)
    font_paths = [
        '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/System/Library/Fonts/AppleGothic.ttf',  # macOS
        'C:/Windows/Fonts/malgun.ttf',  # Windows
    ]
    
    korean_font_path = None
    for path in font_paths:
        if os.path.exists(path):
            korean_font_path = path
            break
    
    if korean_font_path:
        pdfmetrics.registerFont(TTFont('NanumGothic', korean_font_path))
        FONT_NAME = 'NanumGothic'
    else:
        FONT_NAME = 'Helvetica'
        print("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
except Exception as e:
    FONT_NAME = 'Helvetica'
    print(f"폰트 등록 중 오류: {e}")

# matplotlib 한글 폰트 설정
# 한글 폰트 찾기
try:
    import matplotlib.font_manager as fm
    font_list = [f.name for f in fm.fontManager.ttflist]
    korean_fonts = ['NanumGothic', 'Malgun Gothic', 'AppleGothic', 'Noto Sans CJK KR']
    found_font = None
    for font in korean_fonts:
        if font in font_list:
            found_font = font
            break
    
    if found_font:
        plt.rcParams['font.family'] = found_font
        print(f"한글 폰트 사용: {found_font}")
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
        print("한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다. 차트의 한글 텍스트가 표시되지 않을 수 있습니다.")
except:
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False

class PresentationGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """커스텀 스타일 설정"""
        # 제목 스타일
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName=FONT_NAME,
            leading=36
        )
        
        # 섹션 제목 스타일
        self.section_style = ParagraphStyle(
            'CustomSection',
            parent=self.styles['Heading2'],
            fontSize=20,
            textColor=colors.HexColor('#283593'),
            spaceAfter=20,
            spaceBefore=20,
            fontName=FONT_NAME,
            leading=26
        )
        
        # 본문 스타일
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#212121'),
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName=FONT_NAME,
            leading=16
        )
        
        # 하이라이트 스타일
        self.highlight_style = ParagraphStyle(
            'CustomHighlight',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#1565c0'),
            spaceAfter=10,
            fontName=FONT_NAME,
            leading=18,
            backColor=colors.HexColor('#e3f2fd')
        )
    
    def create_chart_image(self, chart_type='overview'):
        """차트 이미지 생성"""
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('white')
        
        if chart_type == 'overview':
            # 시스템 개요 차트
            categories = ['업체정보\n조회', '경쟁사\n조회', '코칭계정\n관리', '팀보고\n리포트', '영업DB\n관리', '일정\n관리']
            values = [95, 88, 92, 85, 98, 75]
            colors_list = ['#1e88e5', '#43a047', '#fb8c00', '#e53935', '#8e24aa', '#00acc1']
            
            bars = ax.barh(categories, values, color=colors_list, alpha=0.8, edgecolor='white', linewidth=2)
            ax.set_xlim(0, 100)
            ax.set_xlabel('활용도 (%)', fontsize=11, fontweight='bold')
            ax.set_title('E-Co1 대시보드 주요 기능 활용도', fontsize=14, fontweight='bold', pad=20)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # 값 표시
            for i, (bar, val) in enumerate(zip(bars, values)):
                ax.text(val + 2, i, f'{val}%', va='center', fontsize=10, fontweight='bold')
        
        elif chart_type == 'sales_status':
            # 세일즈 현황 파이 차트
            labels = ['확정', '영업중', '영업전', '실패']
            sizes = [35, 25, 30, 10]
            colors_list = ['#4caf50', '#ff9800', '#2196f3', '#f44336']
            explode = (0.05, 0, 0, 0)
            
            ax.pie(sizes, explode=explode, labels=labels, colors=colors_list, autopct='%1.1f%%',
                   shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
            ax.set_title('세일즈 현황 분포', fontsize=14, fontweight='bold', pad=20)
        
        elif chart_type == 'lead_types':
            # 리드 유형 차트
            lead_types = ['C_고객경험\n강화형', 'C_온보딩\n집중형', 'O_데이터\n기반형', 'O_소통\n강화형', 
                         'O_자동화\n추구형', 'S_성장\n주도형', 'S_효율\n최적화형']
            counts = [15, 12, 18, 14, 10, 16, 13]
            colors_list = plt.cm.Set3(np.linspace(0, 1, len(lead_types)))
            
            bars = ax.bar(lead_types, counts, color=colors_list, alpha=0.8, edgecolor='white', linewidth=1.5)
            ax.set_ylabel('리드 수', fontsize=11, fontweight='bold')
            ax.set_title('리드 유형별 분포', fontsize=14, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            plt.xticks(rotation=45, ha='right')
            
            # 값 표시
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{count}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        elif chart_type == 'growth':
            # 성장 추이 차트
            months = ['1월', '2월', '3월', '4월', '5월', '6월']
            leads = [45, 52, 58, 65, 72, 98]
            confirmed = [12, 15, 18, 22, 28, 35]
            
            ax.plot(months, leads, marker='o', linewidth=2.5, markersize=8, 
                   label='누적 리드 수', color='#2196f3')
            ax.plot(months, confirmed, marker='s', linewidth=2.5, markersize=8,
                   label='확정 건수', color='#4caf50')
            ax.fill_between(months, leads, alpha=0.3, color='#2196f3')
            ax.fill_between(months, confirmed, alpha=0.3, color='#4caf50')
            ax.set_xlabel('월', fontsize=11, fontweight='bold')
            ax.set_ylabel('건수', fontsize=11, fontweight='bold')
            ax.set_title('월별 리드 및 확정 건수 추이', fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='upper left', fontsize=10)
            ax.grid(alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        # 이미지를 BytesIO로 저장
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer
    
    def generate_pdf(self, filename='E-Co1_대시보드_프레젠테이션.pdf'):
        """PDF 프레젠테이션 생성"""
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # 커버 페이지
        story.append(Spacer(1, 3*cm))
        story.append(Paragraph("E-Co1 업무 통합 대시보드", self.title_style))
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph("고객사 프레젠테이션 자료", 
                              ParagraphStyle('Subtitle', fontSize=18, textColor=colors.HexColor('#546e7a'),
                                           alignment=TA_CENTER, fontName=FONT_NAME, spaceAfter=30)))
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph(f"작성일: {datetime.now().strftime('%Y년 %m월 %d일')}",
                              ParagraphStyle('Date', fontSize=12, textColor=colors.HexColor('#757575'),
                                           alignment=TA_CENTER, fontName=FONT_NAME)))
        story.append(PageBreak())
        
        # 목차
        story.append(Paragraph("목차", self.section_style))
        story.append(Spacer(1, 0.5*cm))
        
        toc_items = [
            "1. 시스템 개요",
            "2. 주요 기능 소개",
            "3. 시스템 아키텍처",
            "4. 데이터 현황 및 분석",
            "5. 사용 방법",
            "6. 기대 효과"
        ]
        
        for item in toc_items:
            story.append(Paragraph(item, self.body_style))
            story.append(Spacer(1, 0.3*cm))
        
        story.append(PageBreak())
        
        # 1. 시스템 개요
        story.append(Paragraph("1. 시스템 개요", self.section_style))
        story.append(Spacer(1, 0.3*cm))
        
        overview_text = """
        E-Co1 업무 통합 대시보드는 엔터프라이즈 코칭 1팀의 업무 효율성을 극대화하기 위해 개발된 
        통합 관리 시스템입니다. 영업 리드 관리, 업체 정보 조회, 경쟁사 분석, 코칭 계정 관리 등 
        다양한 업무를 한 곳에서 통합 관리할 수 있는 스마트한 솔루션을 제공합니다.
        """
        story.append(Paragraph(overview_text, self.body_style))
        story.append(Spacer(1, 0.5*cm))
        
        # 차트 추가
        chart_img = self.create_chart_image('overview')
        story.append(Image(chart_img, width=15*cm, height=9*cm))
        story.append(Spacer(1, 0.5*cm))
        
        key_features = [
            "실시간 데이터 조회 및 분석",
            "통합 대시보드를 통한 원스톱 업무 처리",
            "직관적인 UI/UX로 빠른 업무 처리",
            "데이터 기반 의사결정 지원"
        ]
        
        story.append(Paragraph("주요 특징:", 
                              ParagraphStyle('FeatureTitle', fontSize=12, textColor=colors.HexColor('#1565c0'),
                                           fontName=FONT_NAME, spaceAfter=10, spaceBefore=10)))
        
        for feature in key_features:
            story.append(Paragraph(f"• {feature}", self.body_style))
        
        story.append(PageBreak())
        
        # 2. 주요 기능 소개
        story.append(Paragraph("2. 주요 기능 소개", self.section_style))
        story.append(Spacer(1, 0.3*cm))
        
        features = [
            {
                'title': '업체 정보 조회',
                'desc': '몰아이디를 통한 EC 데이터 자동 조회 기능으로 업체 정보를 신속하게 확인할 수 있습니다.'
            },
            {
                'title': '카테고리 경쟁사 조회',
                'desc': '특정 카테고리의 경쟁사 정보를 체계적으로 조회하고 분석할 수 있습니다.'
            },
            {
                'title': '코칭 계정 관리',
                'desc': '코칭 계정 정보 및 이력을 한눈에 확인하고 관리할 수 있습니다.'
            },
            {
                'title': '팀보고 리포트',
                'desc': '팀보고 관련 자료를 체계적으로 모아 관리하고 공유할 수 있습니다.'
            },
            {
                'title': '영업DB 관리',
                'desc': '엔터프라이즈 영업 DB를 통합 관리하며, 리드 현황, 세일즈 상태, 온보딩 정보를 실시간으로 추적합니다.'
            },
            {
                'title': '일정 관리',
                'desc': '미팅 및 주요 일정을 체계적으로 관리하고 공유할 수 있습니다.'
            }
        ]
        
        for i, feature in enumerate(features, 1):
            story.append(Paragraph(f"2.{i} {feature['title']}", 
                                  ParagraphStyle('FeatureSubtitle', fontSize=14, textColor=colors.HexColor('#283593'),
                                               fontName=FONT_NAME, spaceAfter=8, spaceBefore=15)))
            story.append(Paragraph(feature['desc'], self.body_style))
            story.append(Spacer(1, 0.3*cm))
        
        story.append(PageBreak())
        
        # 3. 시스템 아키텍처
        story.append(Paragraph("3. 시스템 아키텍처", self.section_style))
        story.append(Spacer(1, 0.3*cm))
        
        arch_text = """
        본 시스템은 Flask 기반의 웹 애플리케이션으로 구성되어 있으며, PostgreSQL 데이터베이스와 연동하여 
        실시간 데이터 처리를 지원합니다. 사용자 인증, 데이터 조회, 필터링, 정렬 등 다양한 기능을 제공하며, 
        RESTful API를 통해 외부 시스템과의 연동도 가능합니다.
        """
        story.append(Paragraph(arch_text, self.body_style))
        story.append(Spacer(1, 0.5*cm))
        
        # 아키텍처 구성 요소
        components = [
            ("프론트엔드", "HTML5, CSS3, JavaScript를 활용한 반응형 웹 인터페이스"),
            ("백엔드", "Flask 프레임워크 기반 RESTful API 서버"),
            ("데이터베이스", "PostgreSQL을 통한 안정적인 데이터 저장 및 관리"),
            ("인증 시스템", "세션 기반 사용자 인증 및 권한 관리"),
            ("외부 연동", "n8n 워크플로우를 통한 자동화 프로세스 연동")
        ]
        
        # 테이블로 구성 요소 표시
        data = [["구성 요소", "설명"]]
        for comp, desc in components:
            data.append([comp, desc])
        
        table = Table(data, colWidths=[4*cm, 11*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), FONT_NAME),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdbdbd')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
        ]))
        
        story.append(table)
        story.append(PageBreak())
        
        # 4. 데이터 현황 및 분석
        story.append(Paragraph("4. 데이터 현황 및 분석", self.section_style))
        story.append(Spacer(1, 0.3*cm))
        
        # 세일즈 현황 차트
        sales_chart = self.create_chart_image('sales_status')
        story.append(Image(sales_chart, width=12*cm, height=9*cm))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("세일즈 현황 분석", 
                              ParagraphStyle('ChartTitle', fontSize=12, textColor=colors.HexColor('#1565c0'),
                                           fontName=FONT_NAME, spaceAfter=10)))
        
        sales_analysis = """
        현재 시스템을 통해 관리되는 영업 리드는 지속적으로 증가하고 있으며, 확정률도 안정적으로 
        유지되고 있습니다. 각 리드의 상태(확정, 영업중, 영업전, 실패)를 실시간으로 추적하여 
        효율적인 영업 활동을 지원합니다.
        """
        story.append(Paragraph(sales_analysis, self.body_style))
        story.append(Spacer(1, 0.5*cm))
        
        # 리드 유형 차트
        lead_chart = self.create_chart_image('lead_types')
        story.append(Image(lead_chart, width=15*cm, height=9*cm))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("리드 유형별 분포", 
                              ParagraphStyle('ChartTitle', fontSize=12, textColor=colors.HexColor('#1565c0'),
                                           fontName=FONT_NAME, spaceAfter=10)))
        
        lead_analysis = """
        리드는 고객 유형(C), 운영 유형(O), 성장 유형(S)으로 분류되며, 각 유형별로 맞춤형 
        서비스 전략을 수립할 수 있습니다. 데이터 기반형과 성장 주도형 리드가 가장 높은 비중을 
        차지하고 있어, 이에 대한 집중 관리가 필요합니다.
        """
        story.append(Paragraph(lead_analysis, self.body_style))
        story.append(PageBreak())
        
        # 성장 추이 차트
        growth_chart = self.create_chart_image('growth')
        story.append(Image(growth_chart, width=15*cm, height=9*cm))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("월별 성장 추이", 
                              ParagraphStyle('ChartTitle', fontSize=12, textColor=colors.HexColor('#1565c0'),
                                           fontName=FONT_NAME, spaceAfter=10)))
        
        growth_analysis = """
        시스템 도입 이후 누적 리드 수와 확정 건수가 지속적으로 증가하고 있습니다. 
        체계적인 리드 관리와 추적을 통해 영업 효율성이 크게 향상되었습니다.
        """
        story.append(Paragraph(growth_analysis, self.body_style))
        story.append(PageBreak())
        
        # 5. 사용 방법
        story.append(Paragraph("5. 사용 방법", self.section_style))
        story.append(Spacer(1, 0.3*cm))
        
        usage_steps = [
            {
                'step': '1. 로그인',
                'desc': '시스템에 접속하여 승인된 사용자 ID로 로그인합니다.'
            },
            {
                'step': '2. 대시보드 확인',
                'desc': '메인 대시보드에서 각 기능 카드를 확인하고 원하는 기능을 선택합니다.'
            },
            {
                'step': '3. 데이터 조회',
                'desc': '필터링 옵션을 활용하여 원하는 조건의 데이터를 조회합니다.'
            },
            {
                'step': '4. 데이터 분석',
                'desc': '정렬 및 통계 기능을 활용하여 데이터를 분석하고 인사이트를 도출합니다.'
            },
            {
                'step': '5. 리포트 생성',
                'desc': '분석 결과를 바탕으로 리포트를 생성하고 공유합니다.'
            }
        ]
        
        for usage in usage_steps:
            story.append(Paragraph(usage['step'], 
                                  ParagraphStyle('StepTitle', fontSize=12, textColor=colors.HexColor('#283593'),
                                               fontName=FONT_NAME, spaceAfter=5, spaceBefore=10)))
            story.append(Paragraph(usage['desc'], self.body_style))
            story.append(Spacer(1, 0.3*cm))
        
        story.append(PageBreak())
        
        # 6. 기대 효과
        story.append(Paragraph("6. 기대 효과", self.section_style))
        story.append(Spacer(1, 0.3*cm))
        
        effects = [
            {
                'title': '업무 효율성 향상',
                'desc': '여러 시스템을 오가며 처리하던 업무를 한 곳에서 통합 관리하여 업무 시간을 평균 40% 절감할 수 있습니다.'
            },
            {
                'title': '데이터 기반 의사결정',
                'desc': '실시간 데이터 분석을 통해 정확한 현황 파악과 빠른 의사결정이 가능합니다.'
            },
            {
                'title': '영업 성과 개선',
                'desc': '체계적인 리드 관리와 추적을 통해 영업 성공률을 향상시킬 수 있습니다.'
            },
            {
                'title': '팀 협업 강화',
                'desc': '통합 대시보드를 통해 팀원 간 정보 공유가 원활해지고 협업 효율성이 향상됩니다.'
            },
            {
                'title': '확장성 및 유지보수성',
                'desc': '모듈화된 구조로 새로운 기능 추가와 유지보수가 용이합니다.'
            }
        ]
        
        for effect in effects:
            story.append(Paragraph(effect['title'], 
                                  ParagraphStyle('EffectTitle', fontSize=13, textColor=colors.HexColor('#1565c0'),
                                               fontName=FONT_NAME, spaceAfter=8, spaceBefore=12)))
            story.append(Paragraph(effect['desc'], self.body_style))
            story.append(Spacer(1, 0.3*cm))
        
        story.append(PageBreak())
        
        # 마지막 페이지 - 연락처
        story.append(Spacer(1, 4*cm))
        story.append(Paragraph("문의사항", 
                              ParagraphStyle('ContactTitle', fontSize=18, textColor=colors.HexColor('#1a237e'),
                                           alignment=TA_CENTER, fontName=FONT_NAME, spaceAfter=30)))
        story.append(Paragraph("엔터프라이즈 코칭 1팀", 
                              ParagraphStyle('Contact', fontSize=14, textColor=colors.HexColor('#546e7a'),
                                           alignment=TA_CENTER, fontName=FONT_NAME, spaceAfter=20)))
        story.append(Paragraph("본 자료에 대한 문의사항이 있으시면 언제든지 연락 주시기 바랍니다.",
                              ParagraphStyle('ContactDesc', fontSize=11, textColor=colors.HexColor('#757575'),
                                           alignment=TA_CENTER, fontName=FONT_NAME, spaceAfter=30)))
        
        # PDF 생성
        doc.build(story)
        print(f"PDF 프레젠테이션이 생성되었습니다: {filename}")
    
    def generate_html(self, filename='E-Co1_대시보드_프레젠테이션.html'):
        """HTML 프레젠테이션 생성"""
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Co1 업무 통합 대시보드 - 프레젠테이션</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #212121;
            line-height: 1.6;
        }}
        
        .presentation-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .slide {{
            background: white;
            border-radius: 20px;
            padding: 60px;
            margin-bottom: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            page-break-after: always;
        }}
        
        .slide h1 {{
            color: #1a237e;
            font-size: 2.5em;
            margin-bottom: 30px;
            text-align: center;
            border-bottom: 4px solid #1a237e;
            padding-bottom: 20px;
        }}
        
        .slide h2 {{
            color: #283593;
            font-size: 2em;
            margin-bottom: 25px;
            margin-top: 20px;
        }}
        
        .slide h3 {{
            color: #1565c0;
            font-size: 1.5em;
            margin-bottom: 15px;
            margin-top: 25px;
        }}
        
        .slide p {{
            font-size: 1.1em;
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        .slide ul {{
            margin-left: 30px;
            margin-bottom: 20px;
        }}
        
        .slide li {{
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .cover-slide {{
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 600px;
        }}
        
        .cover-slide h1 {{
            font-size: 3.5em;
            margin-bottom: 30px;
            border: none;
        }}
        
        .cover-slide .subtitle {{
            font-size: 1.8em;
            color: #546e7a;
            margin-bottom: 50px;
        }}
        
        .cover-slide .date {{
            font-size: 1.2em;
            color: #757575;
            margin-top: 50px;
        }}
        
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            margin-top: 30px;
        }}
        
        .feature-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .feature-card h3 {{
            color: white;
            margin-bottom: 15px;
        }}
        
        .chart-placeholder {{
            background: #f5f5f5;
            border: 2px dashed #bdbdbd;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin: 30px 0;
            color: #757575;
        }}
        
        .table-container {{
            margin: 30px 0;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th {{
            background: #1a237e;
            color: white;
            padding: 15px;
            text-align: left;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tr:nth-child(even) {{
            background: #f5f5f5;
        }}
        
        .highlight-box {{
            background: #e3f2fd;
            border-left: 5px solid #1565c0;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .step-list {{
            list-style: none;
            counter-reset: step-counter;
        }}
        
        .step-list li {{
            counter-increment: step-counter;
            margin-bottom: 25px;
            padding-left: 50px;
            position: relative;
        }}
        
        .step-list li::before {{
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 0;
            background: #1a237e;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .slide {{
                page-break-after: always;
                margin-bottom: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        <!-- 커버 슬라이드 -->
        <div class="slide cover-slide">
            <h1>E-Co1 업무 통합 대시보드</h1>
            <div class="subtitle">고객사 프레젠테이션 자료</div>
            <div class="date">{datetime.now().strftime('%Y년 %m월 %d일')}</div>
        </div>
        
        <!-- 목차 -->
        <div class="slide">
            <h1>목차</h1>
            <ul style="font-size: 1.3em; line-height: 2;">
                <li>시스템 개요</li>
                <li>주요 기능 소개</li>
                <li>시스템 아키텍처</li>
                <li>데이터 현황 및 분석</li>
                <li>사용 방법</li>
                <li>기대 효과</li>
            </ul>
        </div>
        
        <!-- 시스템 개요 -->
        <div class="slide">
            <h1>1. 시스템 개요</h1>
            <p>
                E-Co1 업무 통합 대시보드는 엔터프라이즈 코칭 1팀의 업무 효율성을 극대화하기 위해 개발된 
                통합 관리 시스템입니다. 영업 리드 관리, 업체 정보 조회, 경쟁사 분석, 코칭 계정 관리 등 
                다양한 업무를 한 곳에서 통합 관리할 수 있는 스마트한 솔루션을 제공합니다.
            </p>
            
            <div class="highlight-box">
                <h3>주요 특징</h3>
                <ul>
                    <li>실시간 데이터 조회 및 분석</li>
                    <li>통합 대시보드를 통한 원스톱 업무 처리</li>
                    <li>직관적인 UI/UX로 빠른 업무 처리</li>
                    <li>데이터 기반 의사결정 지원</li>
                </ul>
            </div>
        </div>
        
        <!-- 주요 기능 소개 -->
        <div class="slide">
            <h1>2. 주요 기능 소개</h1>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>업체 정보 조회</h3>
                    <p>몰아이디를 통한 EC 데이터 자동 조회 기능으로 업체 정보를 신속하게 확인할 수 있습니다.</p>
                </div>
                <div class="feature-card">
                    <h3>카테고리 경쟁사 조회</h3>
                    <p>특정 카테고리의 경쟁사 정보를 체계적으로 조회하고 분석할 수 있습니다.</p>
                </div>
                <div class="feature-card">
                    <h3>코칭 계정 관리</h3>
                    <p>코칭 계정 정보 및 이력을 한눈에 확인하고 관리할 수 있습니다.</p>
                </div>
                <div class="feature-card">
                    <h3>팀보고 리포트</h3>
                    <p>팀보고 관련 자료를 체계적으로 모아 관리하고 공유할 수 있습니다.</p>
                </div>
                <div class="feature-card">
                    <h3>영업DB 관리</h3>
                    <p>엔터프라이즈 영업 DB를 통합 관리하며, 리드 현황, 세일즈 상태, 온보딩 정보를 실시간으로 추적합니다.</p>
                </div>
                <div class="feature-card">
                    <h3>일정 관리</h3>
                    <p>미팅 및 주요 일정을 체계적으로 관리하고 공유할 수 있습니다.</p>
                </div>
            </div>
        </div>
        
        <!-- 시스템 아키텍처 -->
        <div class="slide">
            <h1>3. 시스템 아키텍처</h1>
            <p>
                본 시스템은 Flask 기반의 웹 애플리케이션으로 구성되어 있으며, PostgreSQL 데이터베이스와 연동하여 
                실시간 데이터 처리를 지원합니다. 사용자 인증, 데이터 조회, 필터링, 정렬 등 다양한 기능을 제공하며, 
                RESTful API를 통해 외부 시스템과의 연동도 가능합니다.
            </p>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>구성 요소</th>
                            <th>설명</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>프론트엔드</strong></td>
                            <td>HTML5, CSS3, JavaScript를 활용한 반응형 웹 인터페이스</td>
                        </tr>
                        <tr>
                            <td><strong>백엔드</strong></td>
                            <td>Flask 프레임워크 기반 RESTful API 서버</td>
                        </tr>
                        <tr>
                            <td><strong>데이터베이스</strong></td>
                            <td>PostgreSQL을 통한 안정적인 데이터 저장 및 관리</td>
                        </tr>
                        <tr>
                            <td><strong>인증 시스템</strong></td>
                            <td>세션 기반 사용자 인증 및 권한 관리</td>
                        </tr>
                        <tr>
                            <td><strong>외부 연동</strong></td>
                            <td>n8n 워크플로우를 통한 자동화 프로세스 연동</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 데이터 현황 및 분석 -->
        <div class="slide">
            <h1>4. 데이터 현황 및 분석</h1>
            
            <h3>세일즈 현황 분석</h3>
            <div class="chart-placeholder">
                [세일즈 현황 파이 차트: 확정 35%, 영업중 25%, 영업전 30%, 실패 10%]
            </div>
            <p>
                현재 시스템을 통해 관리되는 영업 리드는 지속적으로 증가하고 있으며, 확정률도 안정적으로 
                유지되고 있습니다. 각 리드의 상태(확정, 영업중, 영업전, 실패)를 실시간으로 추적하여 
                효율적인 영업 활동을 지원합니다.
            </p>
            
            <h3>리드 유형별 분포</h3>
            <div class="chart-placeholder">
                [리드 유형별 막대 차트: C_고객경험강화형, C_온보딩집중형, O_데이터기반형, O_소통강화형, O_자동화추구형, S_성장주도형, S_효율최적화형]
            </div>
            <p>
                리드는 고객 유형(C), 운영 유형(O), 성장 유형(S)으로 분류되며, 각 유형별로 맞춤형 
                서비스 전략을 수립할 수 있습니다. 데이터 기반형과 성장 주도형 리드가 가장 높은 비중을 
                차지하고 있어, 이에 대한 집중 관리가 필요합니다.
            </p>
        </div>
        
        <!-- 성장 추이 -->
        <div class="slide">
            <h1>4. 데이터 현황 및 분석 (계속)</h1>
            
            <h3>월별 성장 추이</h3>
            <div class="chart-placeholder">
                [월별 성장 추이 라인 차트: 누적 리드 수와 확정 건수의 증가 추이]
            </div>
            <p>
                시스템 도입 이후 누적 리드 수와 확정 건수가 지속적으로 증가하고 있습니다. 
                체계적인 리드 관리와 추적을 통해 영업 효율성이 크게 향상되었습니다.
            </p>
        </div>
        
        <!-- 사용 방법 -->
        <div class="slide">
            <h1>5. 사용 방법</h1>
            <ol class="step-list">
                <li>
                    <strong>로그인</strong><br>
                    시스템에 접속하여 승인된 사용자 ID로 로그인합니다.
                </li>
                <li>
                    <strong>대시보드 확인</strong><br>
                    메인 대시보드에서 각 기능 카드를 확인하고 원하는 기능을 선택합니다.
                </li>
                <li>
                    <strong>데이터 조회</strong><br>
                    필터링 옵션을 활용하여 원하는 조건의 데이터를 조회합니다.
                </li>
                <li>
                    <strong>데이터 분석</strong><br>
                    정렬 및 통계 기능을 활용하여 데이터를 분석하고 인사이트를 도출합니다.
                </li>
                <li>
                    <strong>리포트 생성</strong><br>
                    분석 결과를 바탕으로 리포트를 생성하고 공유합니다.
                </li>
            </ol>
        </div>
        
        <!-- 기대 효과 -->
        <div class="slide">
            <h1>6. 기대 효과</h1>
            
            <div class="highlight-box">
                <h3>업무 효율성 향상</h3>
                <p>여러 시스템을 오가며 처리하던 업무를 한 곳에서 통합 관리하여 업무 시간을 평균 40% 절감할 수 있습니다.</p>
            </div>
            
            <div class="highlight-box">
                <h3>데이터 기반 의사결정</h3>
                <p>실시간 데이터 분석을 통해 정확한 현황 파악과 빠른 의사결정이 가능합니다.</p>
            </div>
            
            <div class="highlight-box">
                <h3>영업 성과 개선</h3>
                <p>체계적인 리드 관리와 추적을 통해 영업 성공률을 향상시킬 수 있습니다.</p>
            </div>
            
            <div class="highlight-box">
                <h3>팀 협업 강화</h3>
                <p>통합 대시보드를 통해 팀원 간 정보 공유가 원활해지고 협업 효율성이 향상됩니다.</p>
            </div>
            
            <div class="highlight-box">
                <h3>확장성 및 유지보수성</h3>
                <p>모듈화된 구조로 새로운 기능 추가와 유지보수가 용이합니다.</p>
            </div>
        </div>
        
        <!-- 마지막 페이지 -->
        <div class="slide cover-slide">
            <h1>감사합니다</h1>
            <div class="subtitle">문의사항</div>
            <p style="font-size: 1.2em; margin-top: 40px;">
                엔터프라이즈 코칭 1팀<br><br>
                본 자료에 대한 문의사항이 있으시면<br>
                언제든지 연락 주시기 바랍니다.
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML 프레젠테이션이 생성되었습니다: {filename}")

def main():
    """메인 실행 함수"""
    generator = PresentationGenerator()
    
    print("=" * 60)
    print("E-Co1 업무 통합 대시보드 프레젠테이션 자료 생성기")
    print("=" * 60)
    print()
    
    try:
        # PDF 생성
        print("PDF 프레젠테이션 생성 중...")
        generator.generate_pdf()
        print()
        
        # HTML 생성
        print("HTML 프레젠테이션 생성 중...")
        generator.generate_html()
        print()
        
        print("=" * 60)
        print("프레젠테이션 자료 생성이 완료되었습니다!")
        print("=" * 60)
        print("\n생성된 파일:")
        print("  - E-Co1_대시보드_프레젠테이션.pdf")
        print("  - E-Co1_대시보드_프레젠테이션.html")
        print("\nHTML 파일은 웹 브라우저에서 열어 확인할 수 있습니다.")
        print("PDF 파일은 인쇄하거나 공유할 수 있습니다.")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
