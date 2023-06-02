from datetime import datetime
from marshmallow_sqlalchemy import fields
from config import db, ma

class Note(db.Model):
    """A model class represents the note table."""

    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class NoteSchema(ma.SQLAlchemyAutoSchema):
    """A marshmallow schema class represents the note table."""

    class Meta:
        """ Meta class for NoteSchema """

        model = Note
        sqla_session = db.session
        load_instance = True
        include_fk = True

class Person(db.Model):
    """A model class represents the person table."""

    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes = db.relationship(
        Note,
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )

class PersonSchema(ma.SQLAlchemyAutoSchema):
    """A marshmallow schema class represents the person table."""

    class Meta:
        """ Meta class for PersonSchema """

        model = Person
        sqla_session = db.session
        load_instance = True
        include_relationships = True

    notes = fields.Nested(NoteSchema, many=True)


note_schema = NoteSchema()
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)