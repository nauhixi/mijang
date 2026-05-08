# 📊 Institutional Alpha Dashboard

미국 주요 헤지펀드 / 기관투자자 포트폴리오 수익률 추적 대시보드.  
SEC EDGAR 13F 공시 데이터 + Yahoo Finance 주가 데이터를 기반으로 매일 자동 업데이트.

**Live demo →** `https://<your-username>.github.io/institutional-dashboard/`

---

## 🖥️ 화면 구성

| 영역 | 내용 |
|------|------|
| 상단 벤치마크 바 | S&P 500 / NASDAQ / Dow Jones / Russell 2000 실시간 수익률 |
| 좌측 랭킹 패널 | 15개 주요 기관 포트폴리오 수익률 순위 (YTD / 1M / 6M / 1Y) |
| 우측 상세 패널 | 선택 기관의 보유 종목, 수익률 차트, S&P 500 대비 알파 |

## 📅 데이터 업데이트

- **매일 KST 10:00** (UTC 01:00) 자동 실행 (GitHub Actions)
- 미국 장 마감 후 최신 주가 반영
- 13F 공시 기준 보유 종목 (분기별 업데이트)

## 🚀 설치 및 배포

### 1. 레포 Fork/Clone

```bash
git clone https://github.com/<your-username>/institutional-dashboard
cd institutional-dashboard
```

### 2. GitHub Pages 활성화

`Settings → Pages → Source: GitHub Actions`

### 3. 첫 데이터 생성

```bash
pip install -r requirements.txt
python scripts/fetch_data.py
git add data/institutions.json
git commit -m "init: first data fetch"
git push
```

### 4. Actions 권한 설정

`Settings → Actions → General → Workflow permissions: Read and write permissions` 체크

---

## 📁 프로젝트 구조

```
institutional-dashboard/
├── .github/
│   └── workflows/
│       └── daily-update.yml    # 매일 자동 실행
├── data/
│   └── institutions.json       # 자동 생성되는 데이터
├── scripts/
│   ├── fetch_data.py           # 데이터 수집 메인 스크립트
│   └── generate_mock_data.py   # 테스트용 목 데이터 생성
├── index.html                  # 대시보드 UI
├── requirements.txt
└── README.md
```

## 🏦 추적 기관 목록 (15개)

| 기관 | 타입 |
|------|------|
| Renaissance Technologies | Quant Hedge Fund |
| Citadel Advisors | Multi-Strategy |
| Coatue Management | Tech Hedge Fund |
| Tiger Global Management | Tech Hedge Fund |
| Two Sigma Investments | Quant Hedge Fund |
| D.E. Shaw & Co | Quant Hedge Fund |
| Appaloosa Management | Hedge Fund |
| Viking Global Investors | Long/Short Equity |
| Berkshire Hathaway | Conglomerate |
| Lone Pine Capital | Long/Short Equity |
| Pershing Square Capital | Activist |
| Third Point LLC | Activist |
| Baupost Group | Value Hedge Fund |
| Bridgewater Associates | Macro Hedge Fund |
| Greenlight Capital | Long/Short Equity |

## ⚙️ 데이터 소스

- **포트폴리오 구성** : SEC EDGAR 13F 공시 (분기별)
- **주가 / 수익률** : Yahoo Finance (yfinance)
- **업데이트 주기** : 매일 (주가), 분기별 (보유 종목 변경)

## 📌 주의사항

- 13F는 분기말 기준 보유 현황 (45일 이내 제출) → 실제 현재 포트폴리오와 차이 있을 수 있음
- 수익률은 공시된 보유 종목 기준 추정치 (실제 레버리지, 숏 포지션 미포함)
- 투자 목적으로 사용 금지 (참고용)
