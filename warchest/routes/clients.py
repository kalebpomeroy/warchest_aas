from warchest import api
import uuid


# TODO: We should have this password protected
@api.post('/register', skip_auth=True)
def register_client():
    return {"client_id": uuid.uuid4()}
