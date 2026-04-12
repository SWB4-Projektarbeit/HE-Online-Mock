class Course:
    def __init__(
        self,
        uid: int,
        blocked: bool,
        course_classification_key: str,
        course_code: str,
        course_identity_code_uid: int,
        course_type_key: str,
        credits: float,
        formatted_course_code: str,
        instruction_languages: list[str],
        main_language_of_instructions: str,
        organisation_uid: int,
        registration_config_type,
        semester_hours: float,
        semester_key: str,
        title,
    ):
        self.uid = uid
        self.blocked = blocked
        self.course_classification_key = course_classification_key
        self.course_code = course_code
        self.course_identity_code_uid = course_identity_code_uid
        self.course_type_key = course_type_key
        self.credits = credits
        self.formatted_course_code = formatted_course_code
        self.instruction_languages = instruction_languages
        self.main_language_of_instructions = main_language_of_instructions
        self.organisation_uid = organisation_uid
        self.registration_config_type = registration_config_type
        self.semester_hours = semester_hours
        self.semester_key = semester_key
        self.title = title
