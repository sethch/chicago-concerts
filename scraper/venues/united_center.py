from venues.ticketmaster import get_artists as _get

VENUE_ID = "KovZpa2M7e"


def get_artists() -> list[dict]:
    return _get(VENUE_ID)
