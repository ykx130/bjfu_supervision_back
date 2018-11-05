from app.core.models.user import User, Group, Supervisor
from app.core.models.lesson import Term
from datetime import datetime
from app.utils.mysql import db


def insert_user():
    term1 = Term()
    term1.name = '2017-2018-1'
    term1.begin_time = datetime.now()
    term1.end_time = datetime.now()
    term2 = Term()
    term2.name = '2016-2017-1'
    term2.begin_time = datetime.now()
    term2.end_time = datetime.now()
    user1 = User()
    user1.username = "admin"
    user1.name = "admin"
    user1.password = "root"
    user2 = User()
    user2.username = "leader"
    user2.name = "leader"
    user2.password = "root"
    user3 = User()
    user3.name = "root"
    user3.username = "admin01"
    user3.password = "admin01"
    group1 = Group()
    group1.name = "first"
    group1.leader_name = "admin"
    group2 = Group()
    group2.name = "second"
    group2.leader_name = "leader"
    supervisor1 = Supervisor
