from typing import Optional

from flask_restful import Resource, marshal_with, abort
from punchline_interfaces import ChuckNorrisServiceInterface, DadJokeServiceInterface

from app import db, service_pool
from app.models import Joke
from app.resources.joke.schema import joke_fields, joke_parser, joke_fields_with_local
from app.service import ServiceJoke, ServiceData


class RetrieveUpdateDeleteJokeResource(Resource):
    @property
    def chuck_norris_service(self):
        return ChuckNorrisServiceInterface.get_instance(service_pool)

    @property
    def dad_joke_service(self):
        return DadJokeServiceInterface.get_instance(service_pool)

    def convert_raw_data_to_joke(self, service_raw_data) -> Optional[ServiceJoke]:
        service_data = ServiceData.model_validate(service_raw_data)
        if not service_data.successful:
            return None
        joke: ServiceJoke = service_data.data
        return joke

    def get_joke_from_chuck_norris(self, joke_id) -> Optional[ServiceJoke]:
        return self.convert_raw_data_to_joke(
            self.chuck_norris_service.get_joke(joke_id)
        )

    def get_joke_from_dad(self, joke_id) -> Optional[ServiceJoke]:
        return self.convert_raw_data_to_joke(
            self.dad_joke_service.get_joke(joke_id)
        )


    @marshal_with(joke_fields_with_local)
    def get(self, joke_id):
        try:
            joke = Joke.query.filter_by(id=int(joke_id), is_deleted=False).first()
        except ValueError:
            joke = self.get_joke_from_chuck_norris(joke_id) or self.get_joke_from_dad(joke_id)

        if joke is None:
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
