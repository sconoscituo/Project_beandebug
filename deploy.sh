#!/bin/bash
set -e

EC2_IP="15.164.97.97"
EC2_USER="ec2-user"
PEM_KEY="./coffeelab-key.pem"
REPO_URL="https://github.com/sconoscituo/Project_beandebug.git"
APP_DIR="/home/ec2-user/beandebug"

chmod 400 "$PEM_KEY"

echo ""
echo "================================================"
echo "  Bean Debug - EC2 배포 시작"
echo "  서버: $EC2_IP"
echo "================================================"

echo ""
echo "[1/5] Docker / git 설치 확인..."
ssh -i "$PEM_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" '
  if ! command -v docker &>/dev/null; then
    sudo yum update -y -q
    sudo yum install -y -q docker git
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ec2-user
  fi
  if ! command -v docker-compose &>/dev/null; then
    sudo curl -fsSL \
      "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
      -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
  fi
  sudo systemctl start docker
  docker --version
  docker-compose --version
'

echo ""
echo "[2/5] 레포지터리 클론 / 업데이트..."
ssh -i "$PEM_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" "
  if [ -d '$APP_DIR/.git' ]; then
    cd '$APP_DIR' && git pull origin main
  else
    git clone '$REPO_URL' '$APP_DIR'
  fi
"

echo ""
echo "[3/5] .env 파일 전송..."
scp -i "$PEM_KEY" -o StrictHostKeyChecking=no .env.prod "$EC2_USER@$EC2_IP:$APP_DIR/.env"
ssh -i "$PEM_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" \
  "echo 'ALLOWED_ORIGINS=http://$EC2_IP' >> '$APP_DIR/.env'"

echo ""
echo "[4/5] Docker 빌드 및 실행 (시간이 걸릴 수 있습니다)..."
ssh -i "$PEM_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" "
  cd '$APP_DIR'
  sudo docker-compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true
  sudo docker-compose -f docker-compose.prod.yml build --no-cache
  sudo docker-compose -f docker-compose.prod.yml up -d
"

echo ""
echo "[5/5] 상태 확인..."
ssh -i "$PEM_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" "
  cd '$APP_DIR'
  echo '--- 컨테이너 상태 ---'
  sudo docker-compose -f docker-compose.prod.yml ps
  echo ''
  echo '--- API 헬스체크 대기 (15초)... ---'
  sleep 15
  curl -sf http://localhost:8000/health && echo ' <- API 정상' || echo 'API 아직 준비 중 (정상, 조금 더 기다려 주세요)'
"

echo ""
echo "================================================"
echo "  배포 완료!"
echo ""
echo "  사이트:   http://$EC2_IP"
echo "  API Docs: http://$EC2_IP/api/docs"
echo "================================================"
