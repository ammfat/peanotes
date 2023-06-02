from flask import abort, make_response

from config import db
from models import Note, Person, note_schema

def create(note):
    person_id = note.get("person_id")
    person = Person.query.filter(Person.id == person_id).one_or_none()

    if person:
        new_note = note_schema.load(note, session=db.session)
        person.notes.append(new_note)
        db.session.commit()

        return note_schema.dump(new_note), 201

    abort(
        404,
        f"Person with id {person_id} not found"
    )

def read_one(note_id):
    """Returns one note for the given note id"""

    note = Note.query.filter(Note.id == note_id).one_or_none()

    if note:
        return note_schema.dump(note)

    abort(
        404,
        f"Note with id {note_id} not found"
    )

def update(note_id, note):
    """ Updates an existing note in the notes structure """

    existing_note = Note.query.filter(Note.id == note_id).one_or_none()

    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        existing_note.content = update_note.content

        db.session.merge(existing_note)
        db.session.commit()

        return note_schema.dump(existing_note), 200

    abort(
        404,
        f"Note with id {note_id} not found"
    )

def delete(note_id):
    """ Deletes a note from the notes structure """

    existing_note = Note.query.filter(Note.id == note_id).one_or_none()

    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()

        return make_response(
            f"Note with id {note_id} successfully deleted", 204
        )

    abort(
        404,
        f"Note with id {note_id} not found"
    )