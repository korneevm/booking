from fabric.api import *
from contextlib import contextmanager

env.user = "bookinguser"
env.hosts = ["accel-propusk.iidf.ru"]
env.key_filename = ["/Users/korneevm/.ssh/korneevm"]
env.homedir = "/home/bookinguser"
env.project = "/home/bookinguser/project"
env.reload = "%s/docroot/reload.txt" % env.homedir


@contextmanager
def virtualenv():
    with cd(env.homedir):
        with prefix('source /home/bookinguser/.virtualenvs/env/bin/activate'):
            yield


def deploy():
    with virtualenv():
        with cd(env.project):
            run('git pull')
            run('pip install -r ./config/requirements.txt')
            #run('python manage.py migrate')
            #run('python manage.py collectstatic')
            #run('touch %s' % env.reload)