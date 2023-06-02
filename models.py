from datetime import datetime
from config import db, ma

class Person(db.Model):
    """A model class represents the person table."""

    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class PersonSchema(ma.SQLAlchemyAutoSchema):
    """A marshmallow schema class represents the person table."""

    class Meta:
        """ Meta class for PersonSchema """

        model = Person
        sqla_session = db.session
        load_instance = True

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)