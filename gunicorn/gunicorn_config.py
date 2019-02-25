# Sample Gunicorn configuration file:
# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

# Couple of configurations comes form:
# /etc/systemd/system/flaskproject.service and they are:
# ExecStart=/home/paperspace/anaconda3/envs/flasko/bin/gunicorn 
# --workers 3 --bind unix:flaskproject.sock -m 007 wsgi:app

timeout = 300

errorlog = '/home/paperspace/flaskproject/gunicorn/error_log'
loglevel = 'debug'
accesslog = '/home/paperspace/flaskproject/gunicorn/access_log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
