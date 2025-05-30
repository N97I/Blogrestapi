1) # Docker Install

apt-get update -y
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

apt-get update -y

systemctl start docker
systemctl enable docker
usermod -aG docker ${USER}
systemctl restart docker
systemctl status docker
docker --version

2) # Docker Compose Install
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
apt update -y
apt upgrade -y
docker-compose --version
3) созадем файл и прописываем в нем как на рисунке
![image](https://github.com/user-attachments/assets/531a491f-1327-4fa3-848b-808e1067c267)

4) создавем файл requirements.txt командой pip freeze > requirements.txt 
![image](https://github.com/user-attachments/assets/d94e8bf1-a5c0-4fdc-a10c-4954a8d1f71d)

5) создаем файл docker-compose.yaml
![image](https://github.com/user-attachments/assets/b6c5a225-48f9-4cb7-a41f-c29bfaee40bb)

6) создаем образ контейнера командой docker-compose build .
7) запускаем командой docker-compose up
8) открываем терминал dockera командой docker-compose exec blog-api bash
9) производим миграцию командой python manage.py migrate в самом терминале dockera
10) создаем usera
заркыть можно командой docker-compose down or ctl+c

без dockera 
запустить в терминале вс кода команду python3 manage.py runserver



