#!/bin/bash
yum update -y
yum install -y docker git
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "Docker setup complete!" > /home/ec2-user/setup-complete.txt
