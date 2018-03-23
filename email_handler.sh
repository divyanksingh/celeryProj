source $HOME/CeleryProj/celery-env/bin/activate
cd $HOME/CeleryProj
celery worker -A tasks --loglevel=INFO