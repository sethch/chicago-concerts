from venues.ticketmaster import get_artists as _get

VENUE_ID_INDOORS = "KovZ917AI5F"
VENUE_ID_OUTDOORS = "KovZ917Amf0"


def get_artists() -> list[dict]:
    return _get(VENUE_ID_INDOORS, VENUE_ID_OUTDOORS)
