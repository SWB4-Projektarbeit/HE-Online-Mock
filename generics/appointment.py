class Appointment:
    def __init__(
        self,
        uid: int,
        application_type_key: str,
        course_group_uid: int,
        course_uid: int,
        start_at: str,
        end_at: str,
        event_type_key: str,
        resource_uid: int,
        room_uid: int,
        status_type_key: str,
        successor_uid: int | None = None,
    ):
        self.uid = uid
        self.applicationTypeKey = application_type_key
        self.courseGroupUid = course_group_uid
        self.courseUid = course_uid
        self.startAt = start_at
        self.endAt = end_at
        self.eventTypeKey = event_type_key
        self.externalObjectUid = self.courseUid
        self.resourceUid = resource_uid
        self.roomUid = room_uid
        self.resourceUrl = f"https://qm.heonline.hs-esslingen.de/he/ee/rest/pages/slc.cp.apt/resource/{self.roomUid}"
        self.statusTypeKey = status_type_key
        self.successorUid = successor_uid
