# 换源
ln -f -s /root/forum/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
ln -f -s /root/forum/misc/pip.conf /root/.pip/pip.conf

# 装依赖
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.6
curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python3.6 /tmp/get-pip.py
pip3 install jinja2 flask gunicorn sqlalchemy pymysql gevent

# 安装MySQL
apt-get -y install debconf-utils git supervisor nginx zsh curl ufw
debconf-set-selections <<< 'mysql-server mysql-server/root_password password admin'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password admin'
apt-get -y install mysql-server

ln -s -f /root/forum/my.cnf /etc/mysql/my.cnf

python3.6 /root/forum/reset.py

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# 配置防火墙
ufw allow 22
ufw allow 80
ufw allow 443
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接

ln -s -f /root/forum/web.conf /etc/supervisor/conf.d/web.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /root/forum/web.nginx /etc/nginx/sites-enabled/web

# 重启服务器
service supervisor restart
service nginx restart

echo 'deploy success'
echo 'succsss'
echo 'ip'
hostname -I