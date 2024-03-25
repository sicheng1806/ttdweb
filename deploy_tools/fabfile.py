'''自动部署脚本，需要fabric库

运行命令： 

$ fab -H YOURHOST --prompt-for-login-password deploy
'''

from fabric import Connection,task
from invoke import Responder

from pathlib import Path
import getpass
import random

#_TMP_HOST = "superlists.sicheng1806.xyz"
REPO_URL = "https://github.com/sicheng1806/ttdweb.git"

def remote_exisit(c,path):
    return c.run(f'test -e {path} && echo 1 || echo 0').stdout.strip() == '1'

def _create_directory_structure_if_necessary(c:Connection,site_folder):
    for subfolder in ('database','static','virtualenv','source'):
        c.run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(c:Connection,source_folder):
    if remote_exisit(c,path=source_folder / ".git"):
        c.run(f'cd {source_folder} && git fetch')
    else:
        c.run(f'git clone -b master {REPO_URL} {source_folder}')
    current_commit = c.local("git log -n 1 --format=%H").stdout.strip()
    c.run(f'cd {source_folder} && git reset --hard {current_commit}')

def _updata_settings(c:Connection,source_folder,site_name):
    settings_path = source_folder / 'superlists/settings.py'
    c.run(f"sed -i \'s/DEBUG = True/DEBUG = False/\' {settings_path}")
    c.run(f"sed -i 's/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = [\"{site_name}\"]/' {settings_path}")#[\"{site_name}\"]
    secret_key_file = source_folder / "superlists/secret_key.py"
    if not remote_exisit(c,secret_key_file):
        chars = 'abcdefghigklmnopqrstuvwxyz0123456789!@#$%^&*(_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        c.run(f"echo 'SECRET_KEY = \"{key}\"' > {secret_key_file}")
    c.run(f"echo 'from .secret_key import SECRET_KEY' >> {settings_path}")

def _update_virtualenv(c:Connection,source_folder):
    virtualenv_folder = source_folder / "../virtualenv"
    if not remote_exisit(c,virtualenv_folder / 'bin/pip'):
        c.run(f'python3 -m venv {virtualenv_folder}')
    c.run(f'{virtualenv_folder/"bin"/"pip"} install -r {source_folder/"requirements.txt"} -i https://pypi.tuna.tsinghua.edu.cn/simple')

def _update_static_files(c:Connection,source_folder):
    c.run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(c:Connection,source_folder):
    c.run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )

def _deploy_Nginx_and_Gunicorn(c:Connection,source_folder):
    if input("do you want to deploy Nginx and Gunicorn config files?\n \"yes\" or other :") == "yes":
        _sudo_pass = getpass.getpass("[sudo] passwd for your usr:")
        sudopass = Responder(
            pattern=r'\[sudo\] password .*:',
            response=f'{_sudo_pass}\n',
        )
        c.run(
            f"cat {source_folder/'deploy_tools/nginx.template.conf'}"
            f"| sed 's/SITENAME/{c.host}/g' " 
            f"| sed 's/USERNAME/{c.user}/g' "
            f"| sudo tee /etc/nginx/sites-available/{c.host}",
            pty=True, watchers=[sudopass]
            )
        c.run(
            f"sudo ln -s /etc/nginx/sites-available/{c.host} "
            f"/etc/nginx/sites-enabled/{c.host}",
            pty=True, watchers=[sudopass]
        )
        c.run(
            f"cat {source_folder/'deploy_tools/gunicorn-systemd.template.service'} "
            f"| sed 's/SITENAME/{c.host}/g' " 
            f"| sed 's/USERNAME/{c.user}/g' "
            f"| sudo tee /etc/systemd/system/gunicorn-{c.host}.service",
            pty=True, watchers=[sudopass]
        )
    else:
        print("don't deploy Nginx and Gunicorn")
        


@task
def deploy(c:Connection):
    c.config.run.echo = True
    site_folder = Path(f'/home/{c.user}/sites/{c.host}')
    source_folder = site_folder / "source"
    _create_directory_structure_if_necessary(c,site_folder)
    _get_latest_source(c,source_folder)
    _updata_settings(c,source_folder,c.host)
    _update_virtualenv(c,source_folder)
    _update_static_files(c,source_folder)
    _update_database(c,source_folder)
    _deploy_Nginx_and_Gunicorn(c,source_folder)
    

    



if __name__ == '__main__':
    _host = input("host to connect:\n")
    _login_pwd = getpass.getpass("password for login ssh:\n")
    connect_kwargs=dict(password=_login_pwd)
    #_sudo_pass = getpass.getpass("What's your sudo password:\n")
    c:Connection = Connection(_host,connect_kwargs=connect_kwargs,
                              #config=config
                              )
    
    deploy(c)


