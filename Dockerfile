FROM python:3.5
RUN mkdir /home/supervision
WORKDIR /home/supervision
COPY . /home/supervision
RUN python3 pip3  install -r ./requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8030
CMD python3 ./run.py runserver -h "0.0.0.0" -p 8030
