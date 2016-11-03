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


class ThorEnv(EnvTask):
    """
    Use dev environment
    """
    name = "thor"

    def run(self):
        env.hosts = ['ubuntu@prodsearch.iterativ.ch']
        env.user = 'ubuntu'
        env.key_filename = '~/.ssh/prodsearch.pem'
        env.env_name = 'dev'
        env.services = [SearchFlaskUwsgiService, NginxService]
        env.project_name = 'searchService'
        env.remote_virtualenv = '/srv/www/searchService/dev/searchService-env'
        env.server_names = ['search.iterativ.ch']
        env.nginx_no_follow = True
        env.requirements_file = 'requirements/req.pip'
        env.puppet_branch_name = 'ubuntu1404'
        env.not_allowed_tasks = ['resetload', 'delete']


thor_env = ThorEnv()
