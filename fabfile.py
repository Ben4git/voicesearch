import os
from os.path import exists
from fabric.api import *
from fabric.contrib.project import *


def _local_path(*args):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *args)


NAME = 'voice.iterativ.ch'

# environments
env.use_ssh_config = True
env.user = 'cloudguru'
env.hosts = ['iterativ.ch']
env.remote_app = '/srv/www/%s' % NAME
env.dist_dir = 'dist'
env.local_app = _local_path() + '/' + env.dist_dir
env.rsync_exclude = ['.settings/',
                     '.project',
                     'ssl.nginx.conf',
                     'nginx.conf',
                     '.git/',
                     '*.py',
                     '*.pyc',
                     '.keep']


def deploy():
    if not exists(env.dist_dir):
        local('mkdir %s' % env.dist_dir)
    local('cp index.html %s' % env.dist_dir)

    # sources & templates
    sudo('mkdir -p %(remote_app)s' % env)
    rsync_project(
        remote_dir=env.remote_app,
        local_dir=env.local_app,
        exclude=env.rsync_exclude,
        extra_opts='--rsync-path="sudo rsync"'
    )
    # sudo("chown -R {user}:{user} {remote_app_path}/.".format(user=env.server_user, remote_app_path=env.remote_app))

    put('nginx.conf', os.path.join('/etc/nginx/sites-enabled/%s.conf' % NAME), use_sudo=True)

    sudo("chown -R {user}:{user} {nginx_conf_file}".format(
        user='root',
        nginx_conf_file=os.path.join('/etc/nginx/sites-enabled/%s.conf' % NAME)))

    # don't restart
    sudo('/etc/init.d/nginx restart')
