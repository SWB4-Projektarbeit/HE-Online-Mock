from generics.course import Course

courses = []

course1 = Course(
    144707,
    False,
    "LVEAB",
    "BSA064",
    90355,
    "SE",
    0.0,
    "BSA.064",
    ["DE"],
    "DE",
    14023,
    {"value": {"de": "Anmeldeverfahren"}},
    2.0,
    "2025W",
    {
        "value": {
            "de": "Gesellschaftliche Bedeutung von familien- und schulergänzenden Angeboten"
        }
    },
)

course2 = Course(
    144708,
    False,
    "LVEAB",
    "BSA065",
    90356,
    "SE",
    0.0,
    "BSA.065",
    ["DE"],
    "DE",
    14023,
    {
        "value": {
            "de": "Anmeldeverfahren"
        }
    },
    2.0,
    "2025W",
    {
        "value": {
            "de": "Gesellschaftliche Bedeutung von familien- und schulergänzenden Angeboten 2"
        }
    },
)

courses.append(course1)
courses.append(course2)
