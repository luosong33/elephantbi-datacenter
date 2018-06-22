from fabric.api import run, env, cd, put

env.hosts = ['root@flexceed.top']

WORKING_PATH_DEVELOP = '/root/flexbi'


def undeploy_develop():
    prepare_deploy_develop()
    with cd(WORKING_PATH_DEVELOP):
        run('docker-compose -f docker-compose.yml rm -s -f -v')


def deploy_develop():
    undeploy_develop()
    with cd(WORKING_PATH_DEVELOP):
        run('docker ps --no-trunc -aqf "status=exited" | xargs --no-run-if-empty docker rm')
        run('docker-compose -f docker-compose.yml pull')
        run('docker-compose -f docker-compose.yml up -d')
    clean_containers()
    clean_images()


# Utils Commands:

def prepare_deploy_develop():
    DEPLOY_FILES = (
        'docker-compose.yml',
        'nginx-proxy.conf'
    )
    DEPLOY_DIRS = (
        'docker-postgresql-multiple-databases',
    )
    for dir in DEPLOY_DIRS:
        run('mkdir -p {0}/{1}'.format(WORKING_PATH_DEVELOP, dir))
    with cd(WORKING_PATH_DEVELOP):
        for filename in DEPLOY_FILES + DEPLOY_DIRS:
            put(filename, filename)



def clean_containers():
    run('docker ps')
    run('docker ps --no-trunc -aqf "status=exited" | xargs --no-run-if-empty docker rm')


def clean_images():
    run('docker images')
    run('docker images --no-trunc -aqf "dangling=true" | xargs --no-run-if-empty docker rmi')
