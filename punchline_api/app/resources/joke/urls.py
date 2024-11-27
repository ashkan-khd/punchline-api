from .list_create import ListCreateJokeResource
from .retrieve_update_delete import RetrieveUpdateDeleteJokeResource

url_mapping = [
    (ListCreateJokeResource, '/api/jokes/'),
    (RetrieveUpdateDeleteJokeResource, '/api/jokes/<string:joke_id>/'),
]