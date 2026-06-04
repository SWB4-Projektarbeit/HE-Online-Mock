from time import sleep

from flask import Flask, json, Response

from examples.courses import courses
from examples.rooms import rooms

LOCAL_PORT = 8081

api = Flask(__name__)


@api.route("/he/co/co-tm-core/course/api/appointments", methods=["GET"])
def getAppointments():
    ret = json.dumps(
        [
            {
                "uid": room.uid,
                "applicationTypeKey": room.applicationTypeKey,
                "courseGroupUid": room.courseGroupUid,
                "courseUid": room.courseUid,
                "endAt": room.endAt,
                "eventTypeKey": room.eventTypeKey,
                "externalObjectUid": room.externalObjectUid,
                "resourceUid": room.resourceUid,
                "resourceUrl": room.resourceUrl,
                "roomUid": room.roomUid,
                "startAt": room.startAt,
                "statusTypeKey": room.statusTypeKey,
                "successorUid": 1
            }
            for room in rooms
        ]
    )

    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp


@api.route("/he/co/co-tm-core/course/api/courses/<int:uid>", methods=["GET"])
def getCourse(uid):
    for course in courses:
        if course.uid == uid:
            ret = json.dumps(
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
                    "mainLanguageOfInstruction": course.main_language_of_instructions,
                    "organisationUid": course.organisation_uid,
                    "registrationConfigType": course.registration_config_type,
                    "semesterHours": course.semester_hours,
                    "semesterKey": course.semester_key,
                    "title": course.title,
                }
            )

            resp = Response(response=ret,
                            status=200,
                            mimetype="application/json")
            return resp

    ret = json.dumps({})
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp

api.run(host="127.0.0.1", port=LOCAL_PORT)
