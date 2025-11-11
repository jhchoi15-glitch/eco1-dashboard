"""
ECO1 영업 대시보드 시스템 - 고객 프레젠테이션 자료 생성기
Professional PDF presentation generator using ReportLab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

# 한글 폰트 등록 (시스템에 설치된 폰트 사용)
try:
    # Linux 시스템의 일반적인 한글 폰트 경로
    font_paths = [
        '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
        '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    ]
    
    font_loaded = False
    for font_path in font_paths:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('Korean', font_path))
            font_loaded = True
            break
    
    if not font_loaded:
        print("Warning: Korean font not found. Using default font.")
        FONT_NAME = 'Helvetica'
        FONT_NAME_BOLD = 'Helvetica-Bold'
    else:
        FONT_NAME = 'Korean'
        FONT_NAME_BOLD = 'Korean'
except Exception as e:
    print(f"Font loading error: {e}. Using default font.")
    FONT_NAME = 'Helvetica'
    FONT_NAME_BOLD = 'Helvetica-Bold'


class PresentationGenerator:
    """전문적인 프레젠테이션 PDF 생성기"""
    
    def __init__(self, filename="ECO1_Dashboard_Presentation.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.story = []
        self.styles = self._create_styles()
        
        # 브랜드 컬러 정의
        self.primary_color = colors.HexColor('#2C3E50')
        self.secondary_color = colors.HexColor('#3498DB')
        self.accent_color = colors.HexColor('#E74C3C')
        self.success_color = colors.HexColor('#27AE60')
        self.light_gray = colors.HexColor('#ECF0F1')
        
    def _create_styles(self):
        """커스텀 스타일 생성"""
        styles = getSampleStyleSheet()
        
        # 제목 스타일
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontName=FONT_NAME_BOLD,
            fontSize=32,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_CENTER,
            spaceAfter=30,
            leading=40
        ))
        
        # 섹션 제목 스타일
        styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=styles['Heading1'],
            fontName=FONT_NAME_BOLD,
            fontSize=20,
            textColor=colors.HexColor('#3498DB'),
            spaceBefore=20,
            spaceAfter=15,
            leading=24
        ))
        
        # 서브 제목 스타일
        styles.add(ParagraphStyle(
            name='SubTitle',
            parent=styles['Heading2'],
            fontName=FONT_NAME_BOLD,
            fontSize=16,
            textColor=colors.HexColor('#2C3E50'),
            spaceBefore=15,
            spaceAfter=10,
            leading=20
        ))
        
        # 본문 스타일
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontName=FONT_NAME,
            fontSize=11,
            textColor=colors.HexColor('#34495E'),
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=16
        ))
        
        # 하이라이트 스타일
        styles.add(ParagraphStyle(
            name='Highlight',
            parent=styles['BodyText'],
            fontName=FONT_NAME_BOLD,
            fontSize=12,
            textColor=colors.HexColor('#E74C3C'),
            alignment=TA_CENTER,
            spaceAfter=10,
            leading=16
        ))
        
        return styles
    
    def add_cover_page(self):
        """표지 페이지 생성"""
        # 로고/타이틀 영역
        self.story.append(Spacer(1, 1.5*inch))
        
        # 메인 제목
        title = Paragraph(
            "ECO1 영업 대시보드 시스템",
            self.styles['CustomTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        
        # 서브타이틀
        subtitle = Paragraph(
            "<font size=16>통합 영업 관리 및 데이터 분석 솔루션</font>",
            ParagraphStyle(
                'subtitle',
                parent=self.styles['CustomBody'],
                alignment=TA_CENTER,
                textColor=self.secondary_color
            )
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1*inch))
        
        # 주요 특징 박스
        features_data = [
            ['🎯', '실시간 영업 현황 모니터링'],
            ['📊', '데이터 기반 의사결정 지원'],
            ['🔄', '자동화된 데이터 수집 및 분석'],
            ['👥', '팀 협업 및 성과 관리'],
        ]
        
        features_table = Table(features_data, colWidths=[1*inch, 4*inch])
        features_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 0), (0, -1), 24),
            ('FONTSIZE', (1, 0), (1, -1), 12),
            ('TEXTCOLOR', (1, 0), (1, -1), self.primary_color),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.light_gray]),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        self.story.append(features_table)
        self.story.append(Spacer(1, 1*inch))
        
        # 날짜 및 문서 정보
        date_text = Paragraph(
            f"<font size=10>{datetime.now().strftime('%Y년 %m월 %d일')}</font>",
            ParagraphStyle(
                'date',
                parent=self.styles['CustomBody'],
                alignment=TA_CENTER,
                textColor=colors.grey
            )
        )
        self.story.append(date_text)
        
        self.story.append(PageBreak())
    
    def add_overview_section(self):
        """개요 섹션"""
        title = Paragraph("1. 시스템 개요", self.styles['SectionTitle'])
        self.story.append(title)
        
        overview_text = """
        ECO1 영업 대시보드는 엔터프라이즈 영업팀을 위한 통합 관리 솔루션입니다. 
        실시간 데이터 수집 및 분석을 통해 영업 활동의 효율성을 극대화하고, 
        데이터 기반의 전략적 의사결정을 지원합니다.
        """
        
        para = Paragraph(overview_text, self.styles['CustomBody'])
        self.story.append(para)
        self.story.append(Spacer(1, 0.3*inch))
        
        # 핵심 가치 제안
        subtitle = Paragraph("핵심 가치 제안", self.styles['SubTitle'])
        self.story.append(subtitle)
        
        value_props = [
            ["항목", "설명"],
            ["실시간 모니터링", "영업 현황을 실시간으로 파악하고 즉각적인 대응 가능"],
            ["데이터 자동화", "수동 작업 최소화로 생산성 향상 및 오류 감소"],
            ["통합 관리", "영업 DB, 일정, 성과를 하나의 플랫폼에서 관리"],
            ["인사이트 도출", "데이터 분석을 통한 전략적 의사결정 지원"],
        ]
        
        value_table = Table(value_props, colWidths=[2*inch, 4.5*inch])
        value_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.secondary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), FONT_NAME_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.light_gray]),
        ]))
        
        self.story.append(value_table)
        self.story.append(PageBreak())
    
    def add_features_section(self):
        """주요 기능 섹션"""
        title = Paragraph("2. 주요 기능", self.styles['SectionTitle'])
        self.story.append(title)
        
        features = [
            {
                "name": "업체 정보 조회",
                "icon": "🏢",
                "description": "몰아이디 EC 데이터를 자동으로 조회하여 업체의 매출, 방문자, 전환율 등 핵심 지표를 실시간으로 확인할 수 있습니다."
            },
            {
                "name": "카테고리 경쟁사 조회",
                "icon": "🔍",
                "description": "동일 카테고리 내 경쟁사 분석을 통해 시장 포지셔닝 및 영업 전략 수립을 지원합니다."
            },
            {
                "name": "코칭 계정 관리",
                "icon": "👤",
                "description": "고객사의 코칭 계정 정보와 활동 이력을 체계적으로 관리하고 추적합니다."
            },
            {
                "name": "팀보고 리포트",
                "icon": "📈",
                "description": "팀 성과 및 주요 지표를 자동으로 집계하여 보고서 작성 시간을 단축합니다."
            },
            {
                "name": "영업DB 관리",
                "icon": "💼",
                "description": "엔터프라이즈 영업 리드를 체계적으로 관리하고 영업 현황을 추적합니다."
            },
            {
                "name": "일정 관리",
                "icon": "📅",
                "description": "미팅 및 주요 일정을 효율적으로 관리하고 팀원 간 일정을 공유합니다."
            }
        ]
        
        for idx, feature in enumerate(features):
            feature_content = [
                [
                    Paragraph(f"{feature['icon']} <b>{feature['name']}</b>", 
                             ParagraphStyle('feature_title', 
                                          parent=self.styles['SubTitle'],
                                          fontName=FONT_NAME_BOLD,
                                          fontSize=14)),
                ],
                [
                    Paragraph(feature['description'], self.styles['CustomBody'])
                ]
            ]
            
            feature_table = Table(feature_content, colWidths=[6.5*inch])
            feature_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.light_gray),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1.5, self.secondary_color),
            ]))
            
            self.story.append(feature_table)
            self.story.append(Spacer(1, 0.2*inch))
        
        self.story.append(PageBreak())
    
    def add_technical_section(self):
        """기술 스택 섹션"""
        title = Paragraph("3. 기술 스택 및 아키텍처", self.styles['SectionTitle'])
        self.story.append(title)
        
        # 기술 스택
        subtitle = Paragraph("기술 스택", self.styles['SubTitle'])
        self.story.append(subtitle)
        
        tech_stack = [
            ["구분", "기술", "설명"],
            ["백엔드", "Python Flask", "경량화된 웹 프레임워크로 빠른 개발 및 확장 가능"],
            ["데이터베이스", "PostgreSQL", "안정적이고 확장 가능한 관계형 데이터베이스"],
            ["프론트엔드", "HTML/CSS/JavaScript", "반응형 웹 디자인으로 다양한 디바이스 지원"],
            ["배포", "Gunicorn", "프로덕션 레벨의 WSGI 서버"],
            ["외부 연동", "N8N Webhook", "자동화 워크플로우 연동"],
        ]
        
        tech_table = Table(tech_stack, colWidths=[1.5*inch, 2*inch, 3*inch])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), FONT_NAME_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.light_gray]),
        ]))
        
        self.story.append(tech_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # 시스템 아키텍처
        subtitle = Paragraph("시스템 아키텍처", self.styles['SubTitle'])
        self.story.append(subtitle)
        
        architecture_text = """
        본 시스템은 3계층 아키텍처를 기반으로 설계되었습니다:
        
        • 프레젠테이션 계층: 사용자 인터페이스 및 대시보드 (웹 브라우저)
        • 비즈니스 로직 계층: Flask 애플리케이션 서버 (데이터 처리 및 비즈니스 로직)
        • 데이터 계층: PostgreSQL 데이터베이스 (데이터 저장 및 관리)
        
        외부 시스템과의 연동을 위해 RESTful API 및 Webhook을 활용하여
        확장성과 유연성을 확보하였습니다.
        """
        
        para = Paragraph(architecture_text, self.styles['CustomBody'])
        self.story.append(para)
        
        self.story.append(PageBreak())
    
    def add_data_analysis_section(self):
        """데이터 분석 기능 섹션"""
        title = Paragraph("4. 데이터 분석 및 리포팅", self.styles['SectionTitle'])
        self.story.append(title)
        
        intro = Paragraph(
            "시스템은 다양한 영업 지표를 실시간으로 수집하고 분석하여 의미 있는 인사이트를 제공합니다.",
            self.styles['CustomBody']
        )
        self.story.append(intro)
        self.story.append(Spacer(1, 0.2*inch))
        
        # 주요 분석 지표
        subtitle = Paragraph("주요 분석 지표", self.styles['SubTitle'])
        self.story.append(subtitle)
        
        metrics = [
            ["지표명", "설명", "활용"],
            ["매출액 (Order Amount)", "최근 30일 주문 금액", "영업 성과 측정"],
            ["방문자 수 (All Visit)", "전체 방문자 트래픽", "마케팅 효과 분석"],
            ["전환율 (CVR)", "구매 전환 비율", "영업 효율성 평가"],
            ["객단가 (AOV)", "평균 주문 금액", "고객 가치 분석"],
            ["페이지뷰 (PV)", "페이지 조회수", "콘텐츠 인기도 측정"],
            ["성장률", "전월 대비 증감률", "성장 추세 파악"],
        ]
        
        metrics_table = Table(metrics, colWidths=[2*inch, 2.5*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.success_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), FONT_NAME_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.light_gray]),
        ]))
        
        self.story.append(metrics_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # 리드 관리 기능
        subtitle = Paragraph("영업 리드 관리", self.styles['SubTitle'])
        self.story.append(subtitle)
        
        lead_features = """
        • 영업 단계별 리드 분류: 확정, 영업중, 영업전, 실패
        • 리드 타입별 세분화: 고객경험강화형, 온보딩집중형, 데이터기반형 등 7가지 유형
        • 서비스 타입 관리: 소통, 기능, 컨설팅 등 맞춤형 서비스 제공
        • 온보딩 케이스 추적: 고객 성공 사례 관리
        • 국내/글로벌 시장 구분: 시장별 영업 전략 수립
        • 담당자별 리드 배정 및 성과 추적
        """
        
        para = Paragraph(lead_features, self.styles['CustomBody'])
        self.story.append(para)
        
        self.story.append(PageBreak())
    
    def add_benefits_section(self):
        """기대 효과 섹션"""
        title = Paragraph("5. 도입 효과", self.styles['SectionTitle'])
        self.story.append(title)
        
        intro = Paragraph(
            "ECO1 영업 대시보드 도입을 통해 다음과 같은 효과를 기대할 수 있습니다:",
            self.styles['CustomBody']
        )
        self.story.append(intro)
        self.story.append(Spacer(1, 0.3*inch))
        
        benefits = [
            {
                "category": "생산성 향상",
                "icon": "⚡",
                "items": [
                    "수동 데이터 수집 작업 80% 감소",
                    "리포트 작성 시간 70% 단축",
                    "영업 프로세스 자동화로 업무 효율 향상"
                ]
            },
            {
                "category": "의사결정 품질 개선",
                "icon": "🎯",
                "items": [
                    "실시간 데이터 기반 의사결정",
                    "정확한 영업 현황 파악",
                    "데이터 기반 전략 수립 가능"
                ]
            },
            {
                "category": "고객 관리 강화",
                "icon": "🤝",
                "items": [
                    "체계적인 리드 관리 시스템",
                    "고객별 맞춤형 서비스 제공",
                    "고객 성공률 향상"
                ]
            },
            {
                "category": "협업 효율화",
                "icon": "👥",
                "items": [
                    "팀원 간 정보 공유 원활",
                    "통합된 플랫폼으로 소통 개선",
                    "일정 및 업무 투명성 확보"
                ]
            }
        ]
        
        for benefit in benefits:
            # 카테고리 제목
            cat_title = Paragraph(
                f"{benefit['icon']} <b>{benefit['category']}</b>",
                ParagraphStyle('benefit_title',
                             parent=self.styles['SubTitle'],
                             fontSize=14)
            )
            self.story.append(cat_title)
            
            # 항목 리스트
            items_text = "<br/>".join([f"• {item}" for item in benefit['items']])
            items_para = Paragraph(items_text, self.styles['CustomBody'])
            
            benefit_table = Table([[items_para]], colWidths=[6.5*inch])
            benefit_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.light_gray),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            self.story.append(benefit_table)
            self.story.append(Spacer(1, 0.2*inch))
        
        self.story.append(PageBreak())
    
    def add_security_section(self):
        """보안 및 권한 관리 섹션"""
        title = Paragraph("6. 보안 및 권한 관리", self.styles['SectionTitle'])
        self.story.append(title)
        
        security_text = """
        시스템의 보안과 데이터 무결성을 보장하기 위해 다음과 같은 보안 기능을 구현하였습니다:
        """
        para = Paragraph(security_text, self.styles['CustomBody'])
        self.story.append(para)
        self.story.append(Spacer(1, 0.2*inch))
        
        security_features = [
            ["보안 기능", "설명"],
            ["사용자 인증", "세션 기반 로그인 시스템으로 승인된 사용자만 접근 가능"],
            ["권한 관리", "사용자별 권한 설정으로 데이터 접근 제어"],
            ["데이터베이스 보안", "환경 변수를 통한 안전한 DB 연결 정보 관리"],
            ["세션 보안", "암호화된 세션 키를 통한 안전한 세션 관리"],
            ["SQL Injection 방지", "파라미터화된 쿼리를 통한 SQL Injection 공격 차단"],
        ]
        
        security_table = Table(security_features, colWidths=[2*inch, 4.5*inch])
        security_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), FONT_NAME_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.light_gray]),
        ]))
        
        self.story.append(security_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # 등록된 사용자
        subtitle = Paragraph("등록된 사용자", self.styles['SubTitle'])
        self.story.append(subtitle)
        
        users_text = """
        현재 시스템에는 6명의 승인된 사용자가 등록되어 있으며, 
        각 사용자는 안전하게 관리되고 있습니다. 추가 사용자 등록이 필요한 경우 
        시스템 관리자를 통해 간편하게 추가할 수 있습니다.
        """
        para = Paragraph(users_text, self.styles['CustomBody'])
        self.story.append(para)
        
        self.story.append(PageBreak())
    
    def add_conclusion_section(self):
        """결론 섹션"""
        title = Paragraph("7. 결론 및 향후 계획", self.styles['SectionTitle'])
        self.story.append(title)
        
        conclusion_text = """
        ECO1 영업 대시보드 시스템은 현대적인 기술 스택과 사용자 중심의 디자인을 통해
        영업팀의 생산성과 효율성을 크게 향상시킬 수 있는 솔루션입니다.
        
        실시간 데이터 분석, 자동화된 리포팅, 체계적인 리드 관리 기능을 통해
        영업 프로세스 전반의 디지털 혁신을 실현하였습니다.
        """
        para = Paragraph(conclusion_text, self.styles['CustomBody'])
        self.story.append(para)
        self.story.append(Spacer(1, 0.3*inch))
        
        # 향후 계획
        subtitle = Paragraph("향후 개선 계획", self.styles['SubTitle'])
        self.story.append(subtitle)
        
        future_plans = [
            "고급 데이터 시각화 기능 추가 (차트 및 그래프)",
            "AI 기반 영업 예측 및 추천 시스템 도입",
            "모바일 앱 개발로 접근성 향상",
            "외부 CRM 시스템과의 연동 확대",
            "고급 분석 리포트 및 대시보드 커스터마이징",
            "실시간 알림 및 자동화 기능 강화"
        ]
        
        plans_text = "<br/>".join([f"• {plan}" for plan in future_plans])
        plans_para = Paragraph(plans_text, self.styles['CustomBody'])
        
        plans_table = Table([[plans_para]], colWidths=[6.5*inch])
        plans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8F8F5')),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('BOX', (0, 0), (-1, -1), 2, self.success_color),
        ]))
        
        self.story.append(plans_table)
        self.story.append(Spacer(1, 0.5*inch))
        
        # 마무리 메시지
        closing = Paragraph(
            "<b>감사합니다</b><br/><br/>"
            "본 시스템에 대한 추가 문의사항이나 시연이 필요하신 경우<br/>"
            "언제든지 연락 주시기 바랍니다.",
            ParagraphStyle('closing',
                         parent=self.styles['Highlight'],
                         fontSize=13,
                         textColor=self.primary_color)
        )
        self.story.append(closing)
    
    def generate(self):
        """PDF 생성"""
        print("프레젠테이션 PDF 생성 중...")
        
        self.add_cover_page()
        self.add_overview_section()
        self.add_features_section()
        self.add_technical_section()
        self.add_data_analysis_section()
        self.add_benefits_section()
        self.add_security_section()
        self.add_conclusion_section()
        
        # PDF 빌드
        self.doc.build(self.story)
        print(f"✅ PDF 생성 완료: {self.filename}")
        print(f"📄 파일 위치: {os.path.abspath(self.filename)}")


def main():
    """메인 실행 함수"""
    generator = PresentationGenerator("ECO1_Dashboard_Presentation.pdf")
    generator.generate()
    
    print("\n" + "="*60)
    print("🎉 고객 프레젠테이션 자료가 성공적으로 생성되었습니다!")
    print("="*60)


if __name__ == "__main__":
    main()
