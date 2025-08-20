bind = "0.0.0.0:9009"
workers = 9
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
timeout = 30
preload_app = True


def post_fork(server, worker):
    if worker.worker_id == 0:
        import os
        if os.getenv("RUN_MAIN", "false") == "true":
            from app.job import run_job
            run_job()
