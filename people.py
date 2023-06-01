from datetime import datetime
from flask import abort, make_response

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {
    "Fairy": {
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "Ruprecht": {
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "Bunny": {
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    }
}


def create(person):
    """Creates a new person in the people structure """

    lname = person.get("lname")
    fname = person.get("fname", "")

    if lname and lname not in PEOPLE:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }

        return PEOPLE[lname], 201

    abort(
        406,
        f"Person with last name {lname} already exists"
    )


def read_all():
    """Returns list of people """

    return list(PEOPLE.values())


def read_one(lname):
    """Returns one person for the given last name"""

    if lname in PEOPLE:
        return PEOPLE[lname]

    abort(
        404, 
        f"Person with last name {lname} not found"
    )


def update(lname, person):
    """ Updates an existing person in the people structure """

    if lname in PEOPLE:
        ## Here, we only update the existing person's first name and timestamp
        ## (the lname) is retained
        PEOPLE[lname]["fname"] = person.get("fname", PEOPLE[lname]["fname"])
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]

    abort(
        404,
        f"Person with last name {lname} not found"
    )


def delete(lname):
    """ Deletes a person from the people structure """

    if lname in PEOPLE:
        del PEOPLE[lname]

        return make_response(
            f"{lname} successfully deleted", 200
        )

    abort(
        404,
        f"Person with last name {lname} not found"
    )