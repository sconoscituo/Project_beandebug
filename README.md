# Bean Debug

> **개발자 커뮤니티 + AI 디버깅 도우미**
> Debug your coffee, debug your code.

[![CI](https://github.com/sconoscituo/Project_beandebug/actions/workflows/ci.yml/badge.svg)](https://github.com/sconoscituo/Project_beandebug/actions/workflows/ci.yml)

---

## 개요

Bean Debug는 **커피를 사랑하는 개발자**를 위한 커뮤니티 플랫폼입니다.
원두 레시피·기어 리뷰·아티클을 공유하는 커뮤니티 기능과,
프리미엄 구독자 전용 **AI 디버깅 도우미** 및 **코드 리뷰** 기능을 제공합니다.

---

## 수익 구조

| 플랜 | 가격 | 주요 기능 |
|------|------|-----------|
| **Free** | 무료 | 커뮤니티 (원두·레시피·기어·아티클), 하루 게시물 5건 |
| **Premium** | ₩9,900/월 | Free 전체 + AI 디버깅 도우미 + 코드 리뷰 + 게시물 무제한 |

프리미엄 전용 기능:
- `POST /subscriptions/ai-debug` — 코드 스니펫 AI 분석
- `POST /subscriptions/code-review` — AI 코드 리뷰

---

## 기술 스택

### Backend
| 분류 | 기술 |
|------|------|
| 언어 | Python 3.11 |
| 프레임워크 | FastAPI 0.115 |
| ORM | SQLAlchemy 2.0 + Alembic |
| DB | PostgreSQL 15 |
| 인증 | JWT (python-jose) + bcrypt |
| 서버 | Uvicorn / Gunicorn |

### Frontend
| 분류 | 기술 |
|------|------|
| 언어 | JavaScript (ESM) |
| 프레임워크 | React 19 + Vite |
| 라우팅 | React Router v7 |
| 상태 관리 | TanStack Query v5 |
| 스타일 | Tailwind CSS v4 |
| HTTP | Axios |

### Infrastructure
| 분류 | 기술 |
|------|------|
| 컨테이너 | Docker + Docker Compose |
| 정적 파일 서빙 | Nginx |
| CI/CD | GitHub Actions |

---

## 주요 기능

### 커뮤니티 (무료)
- **원두(Beans)** — 원두 등록·검색·평가
- **레시피(Recipes)** — 브루잉 레시피 공유·댓글·좋아요
- **아티클(Articles)** — 커피 관련 아티클 작성·댓글·좋아요
- **기어(Gears)** — 커피 장비 등록·리뷰
- **이달의 원두 / 추천 레시피** — 큐레이션 섹션

### AI 디버깅 도우미 (프리미엄)
- 코드 스니펫 붙여넣기 → AI가 버그 원인 분석 및 개선 제안
- 지원 언어: Python, JavaScript, TypeScript 등

### 코드 리뷰 (프리미엄)
- PR 단위 코드 리뷰 요청 → AI가 가독성·보안·성능 관점 피드백 제공

---

## 설치 및 실행 (Docker Compose)

### 필수 요구사항
- Docker 24+
- Docker Compose v2+

### 1. 저장소 클론

```bash
git clone https://github.com/sconoscituo/Project_beandebug.git
cd Project_beandebug
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 값 설정
```

`.env` 필수 항목:

```env
POSTGRES_USER=beandebug
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=beandebug
DATABASE_URL=postgresql://beandebug:your_secure_password@db:5432/beandebug
SECRET_KEY=your_secret_key_min_32_chars
ALLOWED_ORIGINS=http://localhost
```

### 3. 실행

```bash
docker compose up -d
```

| 서비스 | URL |
|--------|-----|
| Frontend | http://localhost |
| API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

### 4. 시드 데이터 주입 (선택)

```bash
curl -X POST http://localhost:8000/seed
```

---

## API 엔드포인트 요약

```
GET  /                        # 루트
GET  /health                  # 헬스체크
GET  /docs                    # Swagger UI

POST /auth/register           # 회원가입
POST /auth/login              # 로그인 (JWT 발급)
GET  /auth/me                 # 내 정보 조회
PUT  /auth/me                 # 내 정보 수정

GET  /beans                   # 원두 목록
GET  /recipes                 # 레시피 목록
GET  /articles                # 아티클 목록
GET  /gears                   # 기어 목록

GET  /subscriptions/plans     # 구독 플랜 목록
GET  /subscriptions/me        # 내 구독 현황
POST /subscriptions/upgrade   # 프리미엄 업그레이드
POST /subscriptions/downgrade # 무료 전환

# 프리미엄 전용
POST /subscriptions/ai-debug      # AI 디버깅
POST /subscriptions/code-review   # 코드 리뷰
```

---

## 개발 환경 (로컬)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env 설정 후
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### 테스트 실행

```bash
# 루트에서
pytest tests/ -v
```

---

## 프로젝트 구조

```
.
├── backend/
│   ├── app/
│   │   ├── core/          # 설정, 로깅, 보안
│   │   ├── database/      # DB 연결
│   │   ├── models/        # SQLAlchemy 모델
│   │   ├── routers/       # API 라우터
│   │   ├── schemas/       # Pydantic 스키마
│   │   ├── services/      # 비즈니스 로직
│   │   └── utils/         # 인증 유틸리티
│   ├── alembic/           # DB 마이그레이션
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api/           # API 클라이언트
│       ├── components/    # 공통 컴포넌트
│       ├── context/       # React Context
│       └── pages/         # 페이지 컴포넌트
├── tests/                 # 백엔드 테스트
├── .github/workflows/     # CI/CD
└── docker-compose.yml
```

---

## 라이선스

MIT
