import os

os.system("gunicorn -w 6 -t 10000 -b 0.0.0.0:{} bjfu_supervision_back:app".format(5000))