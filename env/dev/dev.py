# -*- coding: utf-8 -*-
#
# Iterativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2015 Iterativ GmbH. All rights reserved.
#
# Created on 16/10/15
# @author: pawel
import os
from fabric.api import env
from deployit.fabrichelper.servicebase import FlaskUwsgiService, NginxService
from deployit.fabrichelper.environments import EnvTask


class SearchFlaskUwsgiService(FlaskUwsgiService):
    files = [
        {
            'filename': 'flask_uwsgi.yaml',
            'destination': '%(uwsgi_conf)s/%(env_name)s.%(project_name)s.yaml',
            'template_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
        },
        {
            'filename': 'uwsgiemperor.conf',
            'destination': '/etc/init/uwsgiemperor.conf'
        }
    ]


class DevEnv(EnvTask):
    """
    Use dev environment
    """
    name = "dev"

    def run(self):
        env.hosts = ['ubuntu@prodsearch.iterativ.ch']
        env.user = 'ubuntu'
        env.key_filename = '~/.ssh/prodsearch.pem'
        env.env_name = 'dev'
        env.services = [SearchFlaskUwsgiService, NginxService]
        env.project_name = 'voicesearch'
        env.remote_virtualenv = '/srv/www/voicesearch/dev/voicesearch-env'
        env.server_names = ['voice.iterativ.ch']
        env.nginx_no_follow = True
        env.requirements_file = 'pip.txt'
        env.puppet_branch_name = 'ubuntu1604'
        env.not_allowed_tasks = ['resetload', 'delete']


dev_env = DevEnv()
