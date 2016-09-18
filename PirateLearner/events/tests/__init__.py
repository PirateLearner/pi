def get_backend_id(backend_name):
    from ..models import EVENT_MEDIA
    for bid, bname in EVENT_MEDIA:
        if bname == backend_name:
            return bid
    return None
