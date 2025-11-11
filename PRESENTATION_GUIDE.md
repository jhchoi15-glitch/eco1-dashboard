# E-Co1 업무 통합 대시보드 프레젠테이션 자료 생성 가이드

## 개요

이 도구는 E-Co1 업무 통합 대시보드 시스템을 고객사에 소개하기 위한 전문적인 프레젠테이션 자료를 자동으로 생성합니다.

## 생성되는 자료

1. **PDF 프레젠테이션** (`E-Co1_대시보드_프레젠테이션.pdf`)
   - 인쇄 및 공유에 적합한 PDF 형식
   - 시각적 차트 및 그래프 포함
   - 전문적인 디자인

2. **HTML 프레젠테이션** (`E-Co1_대시보드_프레젠테이션.html`)
   - 웹 브라우저에서 바로 확인 가능
   - 반응형 디자인
   - 인쇄 최적화

## 설치 방법

### 필수 패키지 설치

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install reportlab matplotlib numpy
```

## 사용 방법

### 기본 사용

```bash
python3 generate_presentation.py
```

스크립트를 실행하면 다음 파일들이 생성됩니다:
- `E-Co1_대시보드_프레젠테이션.pdf`
- `E-Co1_대시보드_프레젠테이션.html`

## 프레젠테이션 구성

### 1. 커버 페이지
- 시스템 이름 및 제목
- 작성일자

### 2. 목차
- 전체 프레젠테이션 구조

### 3. 시스템 개요
- 시스템 소개
- 주요 특징
- 기능 활용도 차트

### 4. 주요 기능 소개
- 업체 정보 조회
- 카테고리 경쟁사 조회
- 코칭 계정 관리
- 팀보고 리포트
- 영업DB 관리
- 일정 관리

### 5. 시스템 아키텍처
- 기술 스택
- 구성 요소 설명
- 시스템 구조

### 6. 데이터 현황 및 분석
- 세일즈 현황 파이 차트
- 리드 유형별 분포 차트
- 월별 성장 추이 차트
- 데이터 분석 내용

### 7. 사용 방법
- 단계별 사용 가이드

### 8. 기대 효과
- 업무 효율성 향상
- 데이터 기반 의사결정
- 영업 성과 개선
- 팀 협업 강화
- 확장성 및 유지보수성

## 커스터마이징

### 차트 데이터 수정

`generate_presentation.py` 파일의 `create_chart_image` 메서드에서 차트 데이터를 수정할 수 있습니다:

```python
def create_chart_image(self, chart_type='overview'):
    # 차트 데이터 수정
    values = [95, 88, 92, 85, 98, 75]  # 여기서 값 변경
    ...
```

### 텍스트 내용 수정

각 섹션의 텍스트는 `generate_pdf` 및 `generate_html` 메서드에서 수정할 수 있습니다.

### 스타일 변경

- PDF: `setup_custom_styles` 메서드에서 스타일 수정
- HTML: HTML 템플릿의 `<style>` 섹션에서 CSS 수정

## 한글 폰트 문제 해결

### Linux 환경

한글 폰트가 설치되어 있지 않은 경우:

```bash
# Ubuntu/Debian
sudo apt-get install fonts-nanum fonts-nanum-coding

# 또는 나눔 폰트 직접 설치
wget https://github.com/naver/nanumfont/releases/download/VER2.5/NanumFont_TTF_ALL.zip
unzip NanumFont_TTF_ALL.zip
sudo cp NanumFont_TTF_ALL/*.ttf /usr/share/fonts/truetype/nanum/
sudo fc-cache -fv
```

### macOS 환경

시스템에 기본적으로 한글 폰트가 설치되어 있습니다.

### Windows 환경

시스템에 기본적으로 한글 폰트가 설치되어 있습니다.

## 출력 파일 확인

### PDF 파일
- PDF 뷰어로 열어 확인
- 인쇄 가능
- 공유 및 배포 가능

### HTML 파일
- 웹 브라우저에서 열기
- 인쇄 시 페이지 단위로 출력
- 온라인 공유 가능

## 문제 해결

### 한글 폰트 경고 메시지

차트에서 한글 폰트 경고가 나타나는 경우:
1. 시스템에 한글 폰트 설치 확인
2. 폰트 설치 후 스크립트 재실행
3. 경고는 무시해도 PDF/HTML 파일은 정상 생성됨

### 차트가 표시되지 않는 경우

1. matplotlib이 정상 설치되었는지 확인
2. 필요한 패키지 재설치:
   ```bash
   pip install --upgrade matplotlib numpy
   ```

### PDF 생성 오류

1. reportlab 패키지 확인:
   ```bash
   pip install --upgrade reportlab
   ```

2. 권한 문제 확인 (파일 쓰기 권한)

## 추가 기능

### 데이터베이스 연동 (선택사항)

실제 데이터베이스에서 데이터를 가져와 차트를 생성하려면:

1. `app.py`의 데이터베이스 연결 함수 활용
2. `generate_presentation.py`에 데이터베이스 쿼리 추가
3. 실제 데이터로 차트 생성

## 문의사항

프레젠테이션 자료 생성과 관련된 문의사항이 있으시면 엔터프라이즈 코칭 1팀에 연락 주시기 바랍니다.
