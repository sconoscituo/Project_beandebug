# 1. 빌드 스테이지: 안정적인 LTS 버전 사용 권장
FROM node:22-alpine as builder

WORKDIR /app

# 의존성 설치
COPY package*.json ./
RUN npm install

# 소스 복사 및 빌드
COPY . .
RUN npm run build

# 2. 프로덕션 스테이지 (Nginx)
FROM nginx:alpine

# Nginx 설정 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 빌드된 파일 복사 (builder 스테이지의 dist 폴더를 가져옴)
COPY --from=builder /app/dist /usr/share/nginx/html

# 헬스체크 (Nginx는 80포트)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]