# ECO1 대시보드 프레젠테이션 자료 생성기

## 📋 개요

이 스크립트는 ECO1 영업 대시보드 시스템을 고객사에게 안내하기 위한 전문적인 프레젠테이션 자료를 PDF 형식으로 자동 생성합니다.

## 🎯 주요 특징

- ✨ **전문적인 디자인**: 현대적이고 깔끔한 레이아웃
- 📊 **체계적인 구성**: 7개 섹션으로 구성된 포괄적인 내용
- 🎨 **시각적 효과**: 컬러 테마, 아이콘, 표를 활용한 가독성 향상
- 📄 **A4 크기**: 출력 및 공유에 최적화된 PDF 포맷

## 📚 문서 구성

생성되는 PDF 프레젠테이션은 다음 섹션으로 구성됩니다:

1. **표지 페이지**: 시스템 소개 및 주요 특징
2. **시스템 개요**: 프로젝트 소개 및 핵심 가치 제안
3. **주요 기능**: 6가지 핵심 기능 상세 설명
4. **기술 스택 및 아키텍처**: 사용 기술 및 시스템 구조
5. **데이터 분석 및 리포팅**: 분석 지표 및 리드 관리 기능
6. **도입 효과**: 생산성, 의사결정, 고객 관리, 협업 측면의 효과
7. **결론 및 향후 계획**: 시스템 총평 및 개선 계획

## 🚀 사용 방법

### 1. 필수 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 2. PDF 생성

```bash
python3 generate_presentation.py
```

### 3. 생성 결과

스크립트 실행 후 `ECO1_Dashboard_Presentation.pdf` 파일이 생성됩니다.

```
✅ PDF 생성 완료: ECO1_Dashboard_Presentation.pdf
📄 파일 위치: /workspace/ECO1_Dashboard_Presentation.pdf
```

## 🛠️ 기술 스택

- **Python 3.x**
- **ReportLab 4.0.7**: PDF 생성 라이브러리
- **한글 폰트 지원**: Nanum Gothic (시스템 폰트 사용)

## 🎨 디자인 요소

### 컬러 팔레트

- **Primary Color** (#2C3E50): 제목 및 주요 텍스트
- **Secondary Color** (#3498DB): 섹션 제목 및 강조
- **Accent Color** (#E74C3C): 중요 정보 하이라이트
- **Success Color** (#27AE60): 긍정적 지표 표시
- **Light Gray** (#ECF0F1): 배경 및 구분선

### 레이아웃 특징

- **마진**: 상하좌우 2cm
- **페이지 크기**: A4 (210mm × 297mm)
- **폰트 크기**: 10-32pt (계층적 구조)
- **시각적 요소**: 표, 아이콘, 컬러 박스

## 📝 커스터마이징

### 파일명 변경

```python
generator = PresentationGenerator("Custom_Filename.pdf")
```

### 컬러 변경

`PresentationGenerator` 클래스의 `__init__` 메서드에서 컬러를 수정:

```python
self.primary_color = colors.HexColor('#YOUR_COLOR')
```

### 콘텐츠 수정

각 섹션별 메서드를 수정하여 내용을 변경할 수 있습니다:

- `add_cover_page()`: 표지
- `add_overview_section()`: 개요
- `add_features_section()`: 기능
- `add_technical_section()`: 기술 스택
- `add_data_analysis_section()`: 데이터 분석
- `add_benefits_section()`: 도입 효과
- `add_security_section()`: 보안
- `add_conclusion_section()`: 결론

## 💡 사용 시나리오

1. **고객 미팅**: 영업 미팅 시 제안 자료로 활용
2. **프로젝트 소개**: 내부 공유 및 보고용 자료
3. **온보딩**: 신규 팀원 교육 자료
4. **마케팅**: 제품 소개 및 홍보 자료

## 🔧 문제 해결

### 한글 폰트가 표시되지 않는 경우

시스템에 한글 폰트를 설치하세요:

```bash
# Ubuntu/Debian
sudo apt-get install fonts-nanum fonts-nanum-extra

# macOS (Homebrew)
brew tap homebrew/cask-fonts
brew install font-nanum-gothic
```

### ReportLab 설치 오류

```bash
pip install --upgrade pip
pip install reportlab==4.0.7
```

## 📦 파일 구조

```
/workspace/
├── generate_presentation.py    # PDF 생성 스크립트
├── ECO1_Dashboard_Presentation.pdf  # 생성된 PDF 파일
├── requirements.txt            # 필요 라이브러리 목록
└── PRESENTATION_README.md      # 본 문서
```

## 📄 라이선스

이 스크립트는 ECO1 팀의 내부 프로젝트용으로 제작되었습니다.

## 🤝 기여

개선 사항이나 버그 리포트는 팀 리포지토리를 통해 제출해 주세요.

## 📞 문의

추가 문의사항이나 지원이 필요하신 경우 ECO1 팀에 연락해 주세요.

---

**생성일**: 2025-11-11  
**버전**: 1.0.0  
**제작**: ECO1 Dashboard Team
