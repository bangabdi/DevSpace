from flask_sqlalchemy import SQLAlchemy
from application import app
from utils import get_skills_text, get_resources_for_skills
from sqlalchemy import exc



db = SQLAlchemy(app)

title_skill = db.Table('title_skill',
            db.Column('id', db.Integer, db.ForeignKey('title.id')),
            db.Column('id', db.Integer, db.ForeignKey('skill.id'))
            )


class Title(db.Model):
    __tablename__='title'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30), unique = True)
    title_skill_map = db.relationship('Skill', secondary = title_skill, backref = db.backref('skill',lazy= 'dynamic'))


class Skill(db.Model):
    __tablename__='skill'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)

class Resource(db.Model):
    __tablename__='resource'
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(255), unique = True)
    name = db.Column(db.String(255), unique = True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    skill = db.relationship("Skill", backref=db.backref("skill", uselist=False))

def populate_db():
    #import ipdb; ipdb.set_trace()
    skills_text = get_skills_text()
    SKILL_RESOURCES_MAP = get_resources_for_skills(skills_text)

    for skill_name, resources in SKILL_RESOURCES_MAP.items():
        skill_obj = Skill(name = skill_name)
        print('Adding skill %s' % skill_name)
        #db.session.add(skill_obj)

    #db.session.commit()

    skills = Skill.query.all()
    skill_name_id_map = {}
    for skill in skills:
        skill_name_id_map[skill.name] = skill.id

    for skill_name, resources in SKILL_RESOURCES_MAP.items():
        skill_id = skill_name_id_map[skill_name]

        for resource_name, resource_link in resources:
            resource_obj = Resource(name = resource_name, link = resource_link, skill_id=skill_id)
            print('Adding resource %s' % resource_name)
            
            try:
                db.session.add(resource_obj)
                db.session.commit()
            except exc.IntegrityError as e:
                print e
                db.session.rollback()

            

