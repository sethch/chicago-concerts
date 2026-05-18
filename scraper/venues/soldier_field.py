from venues.ticketmaster import get_artists as _get

VENUE_ID = "KovZpZAF6tIA"


def get_artists() -> list[dict]:
    return _get(VENUE_ID)
