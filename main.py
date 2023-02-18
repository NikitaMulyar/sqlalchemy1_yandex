import datetime
from data import db_session
from data.users import User
from data.jobs import Jobs


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = User()
    user.name = "Ridley"
    user.surname = "Scott"
    user.age = 21
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    db_sess.add(user)
    db_sess.commit()
    data = {1: {'name': 'River', 'surname': 'Song', 'age': 30, 'position': 'бортмеханик',
                'speciality': 'управляет ТАРДИС', 'address': 'module_0', 'email': 'river_song@tardis.gallifrey'},
            2: {'name': 'Dalek', 'surname': '1', 'age': 999999, 'position': 'enemy',
                'speciality': 'engineer', 'address': 'Scaro', 'email': 'dalek1@scaro.universe'},
            3: {'name': 'Master', 'surname': '-', 'age': 2000, 'position': 'clown',
                'speciality': 'изобретатель', 'address': 'TARDIS', 'email': 'master@gallifrey.universe'}}
    for i in data:
        user = User()
        user.name = data[i]['name']
        user.surname = data[i]['surname']
        user.age = data[i]['age']
        user.position = data[i]['position']
        user.speciality = data[i]['speciality']
        user.address = data[i]['address']
        user.email = data[i]['email']
        db_sess.add(user)
        db_sess.commit()

    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False


if __name__ == '__main__':
    main()
