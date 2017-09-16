#! encoding: utf-8
from fabric.api import cd, env, lcd, local, sudo
from fabric.contrib.files import exists, sed
from fabric.operations import get, put, run
from fabric.context_managers import shell_env
from fabric.operations import open_shell


###############
# configurate remote ip
###############
host_ip = "118.89.57.249"


###############
# configurate remote account
###############
env.hosts = ['ubuntu@{}'.format(host_ip)]


###############
# configurate remote passwd
###############
env.password = 'scut0000'


########
###
########
def runbg(cmd, sockname="dtach"):
    return run('dtach -n `mktemp -u /tmp/%s.XXXX` %s'  % (sockname,cmd))


def upload_server():
    local('zip -0 -r source mysqlServer.py DBInterface.py')
    run('mkdir -p server/DBserver')
    put('source.zip', '~/server/DBserver/')
    with cd('~/server/DBserver'):
        run('unzip -o source.zip')


def run_server():
    with cd('./server/DBserver'):
        run('python mysqlServer.py')