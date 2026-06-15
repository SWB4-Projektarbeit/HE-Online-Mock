import os
from functools import wraps

from authlib.integrations.flask_oauth2 import current_token
from functools import wraps
import jwt
import requests
from flask import Flask, json, Response, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from examples.courses import courses
from examples.appointments import rooms
from flask_oidc import OpenIDConnect

LOCAL_PORT = 8081
load_dotenv()

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.getenv("FLASK_SECRET_KEY"),
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'flask-demo',
    'OIDC_SCOPES': ['openid', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token'
})

oidc = OpenIDConnect(app)

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


def get_public_key():
    response = requests.get(os.getenv("PUBLICKEY_URL"))
    response.raise_for_status()
    jwks = response.json()
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks['keys'][1])
    return public_key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get the token from the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            print(token)

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode and validate the token
            public_key = get_public_key()
            print(public_key)
            data = jwt.decode(token, public_key, algorithms=["RS256"], audience=os.getenv("KEYCLOAK_CLIENT_ID"))
            # Optionally, you can add more checks here (e.g., roles, expiration, etc.)
        except jwt.ExpiredSignatureError:
            print("HELLO")
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            print("HELLO2")
            return jsonify({"message": "Invalid token!"}), 401

        # Attach the decoded token data to the request object
        request.user_data = data
        return f(*args, **kwargs)

    return decorated


@app.route("/he/co/co-tm-core/course/api/appointments", methods=["GET"])
@token_required
def getAppointments():
    print(request.headers)
    print(current_token)
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
    print(request.headers)
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

app.run(host="127.0.0.1", port=LOCAL_PORT)