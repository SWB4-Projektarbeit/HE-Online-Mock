from generics.appointment import Appointment

rooms = []

room1 = Appointment(
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

room2 = Appointment(
    23422,
    "LEH",
    59540,
    144708,
    "2026-01-14t08:45:00",
    "2026-01-14t11:15:00",
    "REGULAR",
    85,
    6977,
    "CONFIRMED",
)

room3 = Appointment(
    23423,
    "LEH",
    59541,
    144709,
    "2026-01-14t11:30:00",
    "2026-01-14t13:00:00",
    "REGULAR",
    86,
    6976,
    "RESCHEDULED",
    23422
)

room4 = Appointment(
    23424,
    "LEH",
    59542,
    144710,
    "2026-01-14t14:00:00",
    "2026-01-14t15:30:00",
    "REGULAR",
    87,
    6976,
    "CANCELLED",
)

rooms.append(room1)
rooms.append(room2)
rooms.append(room3)
rooms.append(room4)
