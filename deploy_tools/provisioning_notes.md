配置新网站
===================

## 需要的包

* nginx
* Python >= 3.10
* virtualenv + pip 
* Git 

以Ubuntu为例:
	sudo apt install nginx 

## Nginx虚拟主机

* 参考nginx.template.conf
* 吧SITENAME替换成所需的域名,例如staging.my-domain.com
* 将USERNAME替换成当前用户名

## Systemd服务

* 参考gunicorn-upstart.template.conf
* 把SITENAME替换成所需的域名,例如staging.my-domain.com
* 将USERNAME替换成当前用户名

## 文件夹结构
假设用户账户HOME目录为 /home/username

/home/username
|__ sites
	|__ SITENAME
		|___ database 
		|___ source 
		|___ static
		|___ virtualenv

	
