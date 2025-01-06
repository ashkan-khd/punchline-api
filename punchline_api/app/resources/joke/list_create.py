from typing import Optional, List

from flask_restful import marshal_with
from punchline_interfaces import ChuckNorrisServiceInterface, DadJokeServiceInterface

from app import db, service_pool
from app.models import Joke

from app.resources.utils import Resource
from app.resources.joke.schema import joke_fields, joke_parser

from app.service import ServiceJoke, ServiceData


class ListCreateJokeResource(Resource):
    @property
    def chuck_norris_service(self):
        return ChuckNorrisServiceInterface.get_instance(service_pool)

    @property
    def dad_joke_service(self):
        return DadJokeServiceInterface.get_instance(service_pool)

    def convert_raw_data_to_jokes(self, service_raw_data) -> Optional[List[ServiceJoke]]:
        service_data = ServiceData.model_validate(service_raw_data)
        if not service_data.successful:
            return []
        jokes: List[ServiceJoke] = service_data.data
        return jokes

    def get_jokes_from_chuck_norris(self, query) -> Optional[List[ServiceJoke]]:
        return self.convert_raw_data_to_jokes(
            self.chuck_norris_service.query_jokes(query)
        )

    def get_jokes_from_dad(self, query) -> Optional[List[ServiceJoke]]:
        return self.convert_raw_data_to_jokes(
            self.dad_joke_service.query_jokes(query)
        )

    @marshal_with(joke_fields)
    def get(self):
        if not self.params.query:
            return []

        jokes = Joke.query.filter(
            Joke.value.ilike(f'%{self.params.query}%'),
            Joke.is_deleted == False
        ).all()

        return [
            *list(jokes),
            *self.get_jokes_from_chuck_norris(self.params.query),
            *self.get_jokes_from_dad(self.params.query),
        ]

    @marshal_with(joke_fields)
    def post(self):
        args = joke_parser.parse_args()

        joke = Joke(
            value=args['value'],
            categories=args['categories']
        )

        db.session.add(joke)
        db.session.commit()

        return joke, 201
