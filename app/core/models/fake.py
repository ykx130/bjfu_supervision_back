from app.core.models.user import User, UserRole, Group, Role
from app import db

def insert_user():
    user1 = User()
    user1.username = "admin"
    user1.password = "root"
    user2 = User()
    user2.username = "leader"
    user2.password = "root"
    user3 = User()
    user3.username = "admin01"
    user3.password = "admin01"
    group1 = Group()
    group1.name = "first"
    group1.leader_name = "admin"
    group2 = Group()
    group2.name = "second"
    group2.leader_name = "leader"
    role1 = Role()
    role1.name = "teacher"
    role1.permissions = ["a"]
    role2 = Role()
    role2.name = "leader"
    role2.permissions = ["b"]
    db.session.add(role1)
    db.session.add(role2)
    db.session.commit()
    user_role1 = UserRole()
    user_role1.username = user1.username
    user_role1.role_id = role1.id
    user_role2 = UserRole()
    user_role2.username = user2.username
    user_role2.role_id = role1.id
    user_role3 = UserRole()
    user_role3.username = user2.username
    user_role3.role_id = role2.id
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(group1)
    db.session.add(group2)
    db.session.add(user_role1)
    db.session.add(user_role2)
    db.session.add(user_role3)


