class LectureShip:
    def __init__(
        self,
        uid: int,
        course_uid: int,
        function_key: str,
        groups,
        person_uid: str,
        remunerations,
    ):
        self.uid = uid
        self.course_uid = course_uid
        self.function_key = function_key
        self.groups = groups
        self.person_uid = person_uid
        self.remunerations = remunerations
