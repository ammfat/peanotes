from flask import abort, make_response

from config import db
from models import Person, person_schema, people_schema

def create(person):
    """ Creates a new person in the people structure """

    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        
        return person_schema.dump(new_person), 201

    abort(
        406,
        f"Person with last name {lname} already exists"
    )


def read_all():
    """Returns all people from the people structure"""

    people = Person.query.all()

    return people_schema.dump(people)

def read_one(lname):
    """Returns one person for the given last name"""

    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person:
        return person_schema.dump(person)

    abort(
        404, 
        f"Person with last name {lname} not found"
    )


def update(lname, person):
    """ Updates an existing person in the people structure """

    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        existing_person.lname = update_person.lname        

        db.session.merge(existing_person)
        db.session.commit()

        return person_schema.dump(existing_person), 200

    abort(
        404,
        f"Person with last name {lname} not found"
    )


def delete(lname):
    """ Deletes a person from the people structure """

    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()

        return make_response(
            f"Person with last name {lname} successfully deleted", 204
        )

    abort(
        404,
        f"Person with last name {lname} not found"
    )