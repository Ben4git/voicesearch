# -*- coding: utf-8 -*-
#
# Iterativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2015 Iterativ GmbH. All rights reserved.
#
# Created on 16/10/15
# @author: pawel
from fabric.api import env
from dev.dev import *
from prod.prod import *

import glob
import json

from deployit.fabrichelper.taskbase import Deploy
from deployit.fabrichelper.common import rsync_project

env.rsync_exclude.remove('*.dat')
env.rsync_exclude = env.rsync_exclude + ['media/']


class SearchServiceDeploy(Deploy):
    """
    Deploy project, initialize and deploy libraries
    """
    name = "full_deploy"
    full_deploy = True

    def run(self, no_input=False, migrate=False):
        if self.full_deploy:
            self.create_project_directories()
            self.initialize_virtualenv()

        # python sources
        rsync_project(
            remote_dir=env.remote_path(),
            local_dir=env.local_path('searchService'),
            exclude=env.rsync_exclude,
            extra_opts='--rsync-path="sudo rsync"',
        )

        # self.clear_pycs()
        self.adjust_rights()

        # if self.full_deploy:
        self.deploy_services()
        self.restart_services()

        status_code = self.load_site("http://%s" % env.server_names[0])
        self.deploy_log(message='%s %s: HTTP status code: %s' % (env.env_name, self.__class__.name, status_code))


class LightSearchServiceDeploy(SearchServiceDeploy):
    """
    Light deploy project, assuming eveything is initialized and no libraries have to be updated
    """
    name = "deploy"
    full_deploy = False


class ResetElastic(BaseTask):
    """
    Delete elasticsearch index
    """
    name = "reset_elastic"

    def run(self):
        # first delete existing indices
        self.delete_all_indices()
        # setup index mappings
        self.setup_mappings()
        # setup aliases
        self.setup_aliases()

    def delete_all_indices(self):
        run('curl -XDELETE localhost:9200/_all')

    def setup_mappings(self):
        for qs in glob.glob('../elastic/mappings/*'):
            index_file = qs.split('/')[-1]
            if '.json' in index_file and len(index_file) > 5:
                index_name = index_file[:-5]

                print "Load index '%s' mapping from '%s'" % (index_name, qs)
                mapping = open(qs).read().replace('\n', '').replace('\r', '').replace('  ', ' ')

                run("curl -k -XPOST localhost:9200/%s -d '%s'" % (index_name, mapping))

    def setup_aliases(self):
        for qs in glob.glob('../elastic/aliases/*'):
            alias_file = qs.split('/')[-1]
            if '.json' in alias_file and len(alias_file) > 5:
                alias_name = alias_file[:-5]

                print "Load alias '%s' from '%s'" % (alias_name, qs)
                alias = open(qs).read().replace('\n', '').replace('\r', '').replace('  ', ' ')

                run("curl -k -XPOST localhost:9200/_aliases -d '%s'" % alias)


full_deploy = SearchServiceDeploy()
light_deploy = LightSearchServiceDeploy()

reset_elastic = ResetElastic()