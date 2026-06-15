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
oauth.register(
    name="keycloak",
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url=os.getenv("KEYCLOAK_SERVER_METADATA_URL"),
    client_kwargs={"scope": "openid profile email"},
)


@app.route("/he/co/co-tm-core/course/api/appointments", methods=["GET"])
def getAppointments():
    user = session.get("user")
    if not user:
        return Response(response="Not authenticated",
                        status=401,
                        mimetype="application/json")
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
        return Response(response="Not authenticated",
                        status=401,
                        mimetype="application/json")
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

@app.route("/")
def index():
    user = session.get("user")
    if user:
        return render_template_string('''
            <h1>Welcome, {{ user['name'] }}!</h1>
            <form action="{{ url_for('logout') }}" method="post">
                <button type="submit">Logout</button>
            </form>
        ''', user=user)
    else:
        return render_template_string('''
            <h1>Hello, you are not logged in.</h1>
            <form action="{{ url_for('login') }}" method="post">
                <button type="submit">Login</button>
            </form>
        ''')

@app.route("/login", methods=["POST"])
def login():
    redirect_uri = url_for("auth", _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)

@app.route("/auth")
def auth(redirect_uri = None):
    token = oauth.keycloak.authorize_access_token()
    session["user"] = oauth.keycloak.parse_id_token(token)
    if redirect_uri:
        return redirect(redirect_uri)
    return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    logout_url = f"{os.getenv('KEYCLOAK_LOGOUT_URL')}?redirect_uri={url_for('index', _external=True)}"
    return redirect(logout_url)

app.run(host="127.0.0.1", port=LOCAL_PORT)