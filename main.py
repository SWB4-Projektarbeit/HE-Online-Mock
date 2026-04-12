from flask import Flask, json

from interfaces.course import Course
from interfaces.lectureship import LectureShip
from interfaces.person_claim import Person_Claim
from interfaces.room import Room

LOCAL_PORT = 8081

api = Flask(__name__)

rooms = []
courses = []
lectureships = []
person_claims = []

room1 = Room(
    23421,
    "LEH",
    59539,
    144707,
    "2026-01-14t08:45:00",
    "2026-01-14t11:15:00",
    "REGULAR",
    84,
    6976,
    "CONFIRMED",
)

rooms.append(room1)

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

courses.append(course1)

lectureship1 = LectureShip(
    249500,
    144707,
    "LECTURE",
    {"items": []},
    "72B6DB94A83FA65A",
    {"items": [{"lectureShipType": "Pflicht", "semesterHours": 3.0}]},
)

lectureships.append(lectureship1)

person_claim1 = Person_Claim(
    [
        {
            "givenName": "Max",
            "surname": "Mustermann",
            "titlePrefix": "Prof. Dr. phil.",
            "uid": "72B6DB94A83FA65A",
        }
    ],
    100,
    ["CO_CLAIM_TITLE", "CO_CLAIM_PERSON_UID", "CO_CLAIM_NAME"],
)

person_claims.append(person_claim1)


@api.route("/he/co/co-tm-core/course/api/appointments", methods=["GET"])
def getAppointments():
    return json.dumps(
        [
            {
                "uid": room.uid,
                "applicationTypeKey": room.applicationTypeKey,
                "courseGroupUid": room.courseGroupUid,
                "endAt": room.endAt,
                "eventTypeKey": room.eventTypeKey,
                "externalObjectUid": room.externalObjectUid,
                "resourceUId": room.resourceUId,
                "resourceUrl": room.resourceUrl,
                "roomUid": room.roomUid,
                "startAt": room.startAt,
                "statusTypeKey": room.statusTypeKey,
            }
            for room in rooms
        ]
    )


@api.route("/he/co/co-tm-core/course/api/courses/<uid>", methods=["GET"])
def getCourse(uid):
    for course in courses:
        if course.uid == uid:
            return json.dumps(
                {
                    "uid": course.uid,
                    "blocked": course.blocked,
                    "courseClassificationKey": course.course_classification_key,
                    "courseCode": course.course_code,
                    "courseIdentityCodeUid": course.course_identity_code_uid,
                    "courseTypeKey": course.course_type_key,
                    "credits": course.credits,
                    "formattedCourseCode": course.formatted_course_code,
                    "instructionLanguages": course.instruction_languages,
                    "mainLanguageOfInstruction": course.main_language_of_instruction,
                    "organisationUid": course.organisation_uid,
                    "registrationConfigType": course.registration_config_type,
                    "semesterHours": course.semester_hours,
                    "semesterKey": course.semester_key,
                    "title": course.title,
                }
            )
    return json.dumps({})


@api.route("/he/co/co-tm-core/course/api/lectureships/<course_uid>", methods=["GET"])
def getLectureships(course_uid):
    for lectureship in lectureships:
        if lectureship.course_uid == course_uid:
            return json.dumps(
                {
                    "uid": lectureship.uid,
                    "courseUid": lectureship.courseUid,
                    "functionKey": lectureship.functionKey,
                    "groups": lectureship.groups,
                    "personUid": lectureship.personUid,
                    "remunerations": lectureship.remunerations,
                }
            )
    return json.dumps({})