# Bean Debug — 프로젝트 검토 보고서

> 검토일: 2026-02-23

---

## 1. 프로젝트 개요

**Bean Debug**는 커피 브루잉 레시피 관리 및 커뮤니티 플랫폼입니다. 슬로건은 *"Debug your coffee, one brew at a time"*.

| 구분 | 기술 스택 |
|---|---|
| 백엔드 | FastAPI + SQLAlchemy + PostgreSQL + Gunicorn |
| 프론트엔드 | React 19 + Vite (rolldown-vite) + TanStack Query + Tailwind CSS v4 |
| 인증 | JWT (python-jose + passlib/bcrypt) |
| 인프라 | Docker Compose (dev/prod 분리) + GitHub Actions CI/CD |
| 외부 연동 | GoogleNews (커피 뉴스 크롤링) |

---

## 2. 디렉토리 구조

```
Bean_Debug/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI 진입점
│       ├── api/endpoints/       # 구 방식 엔드포인트 (articles)
│       ├── routers/             # 신 방식 라우터 (auth, beans, recipes, gears, featured, articles)
│       ├── models/              # SQLAlchemy ORM 모델
│       ├── schemas/             # Pydantic 스키마
│       ├── services/            # 비즈니스 로직 (news_service)
│       ├── utils/               # 공통 유틸 (auth, slug)
│       └── database/            # DB 연결·설정
├── frontend/
│   └── src/
│       ├── api/                 # Axios API 클라이언트
│       ├── components/          # 공통 컴포넌트 (Navbar)
│       ├── context/             # AuthContext
│       └── pages/               # 페이지 컴포넌트
├── docker-compose.yml
├── docker-compose.prod.yml
└── .github/workflows/deploly.yml
```

---

## 3. 데이터 모델 관계

```
User ─┬─ Recipe ─── RecipeComment
      ├─ Bean        RecipeLike
      ├─ Article ─── ArticleComment
      ├─ GearReview  ArticleLike
      └─ (likes/comments via 관계 테이블)

Gear ──── GearReview
Recipe ── FeaturedRecipe
```

---

## 4. API 엔드포인트 목록

| 라우터 | 접두사 | 주요 기능 |
|---|---|---|
| auth | `/auth` | 회원가입, 로그인, 내 정보 조회/수정 |
| beans | `/beans` | 원두 CRUD (내 원두 / 공개 원두) |
| recipes | `/recipes` | 레시피 CRUD + 좋아요 + 댓글 |
| articles | `/articles` | 커뮤니티 아티클 + 좋아요 + 댓글 |
| gears | `/gears` | 장비 CRUD (관리자 전용) + 리뷰 |
| featured | `/featured` | 추천 레시피 관리 |
| **api/articles** | `/api/articles` | 구글 뉴스 연동 아티클 (별도 엔드포인트) |

---

## 5. 발견된 문제점

### 🔴 심각 (보안)

**[S-1] 민감 파일 Git 추적**
- `coffeelab-key.pem` — AWS/서버 PEM 키가 레포지터리에 포함되어 있습니다.
- `temp-key.json` — 임시 키 JSON이 추적됩니다.
- `.env` — 실제 시크릿 키 및 DB 비밀번호가 포함된 `.env` 파일이 커밋되어 있습니다.
- **조치**: 즉시 해당 파일들을 `.gitignore`에 추가하고, 키를 로테이션(재발급)해야 합니다.

**[S-2] docker-compose.yml 하드코딩된 시크릿**
```yaml
SECRET_KEY=super-secret-key-change-this-in-production-min-32-chars
POSTGRES_PASSWORD: beandebug123
```
- 이 값들이 버전 관리에 그대로 남아있습니다. 환경 변수 참조(`${SECRET_KEY}`) 방식으로 변경해야 합니다.

**[S-3] CORS 와일드카드 (`allow_origins=["*"]`)**
- `allow_credentials=True`와 `allow_origins=["*"`]`의 조합은 동작하지 않으며(CORS 스펙 위반) 보안 위험이 있습니다.
- 프로덕션에서는 명시적인 도메인으로 제한해야 합니다.

---

### 🟠 중간 (기능·설계)

**[M-1] 아티클 라우터 이중 등록 (main.py)**
```python
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])  # 구 라우터
app.include_router(articles_router)  # 신 라우터 (routers/articles.py)
```
- 같은 기능을 담당하는 두 라우터가 공존합니다. `/api/articles`와 `/articles`에 각각 다른 로직이 동작하여 혼란을 야기합니다.
- `api/endpoints/articles.py`는 인증 없이 `author_id=1`을 하드코딩하는 방식으로, 구 코드를 정리하거나 단일 라우터로 통합해야 합니다.

**[M-2] article 생성 시 인증 없음 + 하드코딩된 author_id**
```python
# api/endpoints/articles.py
new_article = Article(
    author_id=1,  # 항상 1번 유저로 고정
    ...
)
```
- 누구나 인증 없이 아티클을 생성할 수 있으며, 항상 작성자가 ID=1로 지정됩니다.

**[M-3] Alembic 미사용 — `create_all()` 방식**
```python
Base.metadata.create_all(bind=engine)  # main.py
```
- 스키마 변경 이력이 관리되지 않아 운영 환경 DB 마이그레이션 시 데이터 손실 위험이 있습니다.
- Alembic이 `requirements.txt`에 포함되어 있음에도 마이그레이션 폴더가 없습니다.

**[M-4] `bs4` (BeautifulSoup) 의존성 누락**
```python
# api/endpoints/articles.py
from bs4 import BeautifulSoup
```
- `requirements.txt`에 `beautifulsoup4`가 없어 도커 빌드 시 ImportError가 발생합니다.

**[M-5] 프론트엔드에 Gear 관련 페이지 없음**
- 백엔드에 `/gears` 라우터가 완비되어 있지만 `App.jsx`에 장비 관련 라우트가 없습니다.

---

### 🟡 개선 권장 (코드 품질)

**[Q-1] `requirements.txt` 중복 항목**
```
passlib[bcrypt]==1.7.4   # 4번째 줄
passlib[bcrypt]          # 14번째 줄 (버전 없음, 중복)
```

**[Q-2] `datetime.utcnow()` 사용 (Python 3.12 deprecated)**
```python
created_at = Column(DateTime, default=datetime.utcnow)
```
- `datetime.now(timezone.utc)` 또는 `datetime.UTC` 사용을 권장합니다.

**[Q-3] `debug=True` 기본값**
```python
debug: bool = True  # database/connection.py
```
- 프로덕션에서 SQL 쿼리 전체 로그가 출력됩니다. `.env`에서 명시적으로 `DEBUG=False`를 강제하거나 기본값을 `False`로 변경해야 합니다.

**[Q-4] `recipe_update.dict()` Pydantic v2 비권장 메서드**
```python
update_data = recipe_update.dict(exclude_unset=True)  # routers/recipes.py
```
- Pydantic v2에서 `.dict()`는 deprecated이며 `.model_dump()`를 사용해야 합니다 (auth.py도 동일).

**[Q-5] CI/CD 워크플로우 파일명 오타**
```
.github/workflows/deploly.yml  # "deploly" → "deploy"
```

**[Q-6] `venv/` 폴더 Git 추적**
- Windows 환경의 Python venv 폴더(`venv/Lib/...`)가 레포지터리에 포함되어 있습니다. `.gitignore`에 `venv/`를 추가해야 합니다.

---

## 6. 잘 구현된 부분

- **인증 체계**: JWT + bcrypt 해싱, 활성 사용자/관리자 권한 분리가 명확합니다.
- **DB 세션 관리**: `yield` 패턴으로 세션 자동 정리가 올바르게 구현되어 있습니다.
- **좋아요 중복 방지**: `RecipeLike` 테이블을 통해 중복 좋아요를 방지합니다.
- **장비 평균 평점 자동 재계산**: 리뷰 추가/수정/삭제 시 `avg()` 집계로 실시간 반영됩니다.
- **Docker 환경 분리**: dev/prod Compose 파일이 분리되어 있습니다.
- **공개/비공개 모델**: Bean·Recipe 모두 `is_public` 플래그로 공개 범위를 제어합니다.

---

## 7. 우선 조치 사항 (체크리스트)

- [ ] `coffeelab-key.pem`, `temp-key.json`, `.env` → `.gitignore` 추가 후 `git rm --cached`로 추적 제거, 키 재발급
- [ ] `docker-compose.yml` 시크릿 → 환경 변수 참조로 변경
- [ ] `api/endpoints/articles.py` → 삭제 또는 인증 추가 후 `routers/articles.py`와 통합
- [ ] `requirements.txt` → `beautifulsoup4` 추가, `passlib[bcrypt]` 중복 제거
- [ ] Alembic 초기화 → `alembic init` 후 마이그레이션 파일 생성
- [ ] CORS → 프로덕션 도메인만 허용
- [ ] `.dict()` → `.model_dump()` 전환
- [ ] `venv/` → `.gitignore`에 추가
- [ ] 프론트엔드 Gear 페이지 구현
