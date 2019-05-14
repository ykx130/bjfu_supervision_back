import os

os.system('gunicorn -w 6 -t 10000 -b 0.0.0.0:{} run:app'.format(8080))