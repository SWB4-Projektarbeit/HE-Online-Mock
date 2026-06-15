import os

from flask import Flask, json, Response, redirect, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from examples.courses import courses
from examples.appointments import rooms

LOCAL_PORT = 8081
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

oauth = OAuth(app)
keycloak = oauth.register(
    name="keycloak",
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url=f'{os.getenv("KEYCLOAK_URL")}/realms/{os.getenv("KEYCLOAK_REALM")}/.well-known/openid-configuration',
    client_kwargs={
        "scope": "openid profile email",
        "code_challenge_method": "S256",
    },
)


@app.route("/he/co/co-tm-core/course/api/appointments", methods=["GET"])
def getAppointments():
    user = session.get("user")
    if not user:
        return redirect(url_for("login", redirect_method="getAppointments", _external=True))
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
                "successorUid": room.successorUid,
            }
            for room in rooms
        ]
    )

    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp


@app.route("/he/co/co-tm-core/course/api/courses/<int:uid>", methods=["GET"])
def getCourse(uid):
    user = session.get("user")
    if not user:
        return redirect(url_for("login", redirect_method="getCourse", uid=uid, _external=True))
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

@app.route("/login/<redirect_method>/<uid>")
def login(redirect_method = None, uid = None):
    redirect_uri = url_for("auth", redirect_method=redirect_method, uid=uid, _external=True)
    return keycloak.authorize_redirect(redirect_uri)

@app.route("/auth/<redirect_method>/<uid>")
def auth(redirect_method = None, uid = None):
    token = keycloak.authorize_access_token()
    session["user"] = token.get("userinfo")
    if redirect:
        if uid:
            return redirect(url_for(redirect_method, uid=uid))
        return redirect(url_for(redirect_method))
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

app.run(host="127.0.0.1", port=LOCAL_PORT)