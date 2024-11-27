from typing import Optional

from flask_restful import Resource, marshal_with, abort
from punchline_interfaces import ChuckNorrisServiceInterface

from app import db, service_pool
from app.models import Joke
from app.resources.joke.schema import joke_fields, joke_parser, joke_fields_with_local
from app.service.chuck_norris import ChuckNorrisServiceData, ChuckNorrisJoke


class RetrieveUpdateDeleteJokeResource(Resource):
    @property
    def chucknorris_service(self):
        return ChuckNorrisServiceInterface.get_instance(service_pool)

    def get_joke_from_chuck_norris(self, joke_id) -> Optional[ChuckNorrisJoke]:
        service_raw_data = self.chucknorris_service.get_joke(joke_id)
        service_data = ChuckNorrisServiceData.model_validate(service_raw_data)
        if not service_data.successful:
            return None
        joke: ChuckNorrisJoke = service_data.data
        return joke

    @marshal_with(joke_fields_with_local)
    def get(self, joke_id):
        try:
            joke = Joke.query.filter_by(id=int(joke_id), is_deleted=False).first()
        except ValueError:
            joke = None

        if (joke := joke or self.get_joke_from_chuck_norris(joke_id)) is None:
            abort(404, message=f"Joke {joke_id} not found")

        return joke

    @marshal_with(joke_fields)
    def put(self, joke_id):
        joke = Joke.query.filter_by(id=joke_id, is_deleted=False).first_or_404()

        args = joke_parser.parse_args()
        joke.value = args['value']
        joke.categories = args['categories']

        db.session.commit()

        return joke

    def delete(self, joke_id):
        joke = Joke.query.filter_by(id=joke_id, is_deleted=False).first_or_404()

        joke.is_deleted = True
        db.session.commit()

        return '', 204
