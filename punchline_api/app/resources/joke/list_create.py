from typing import Optional, List

from flask import request
from flask_restful import Resource, marshal_with
from punchline_interfaces import ChuckNorrisServiceInterface

from app import db, service_pool
from app.models import Joke
from app.resources.joke.schema import joke_fields, joke_parser
from app.service.chuck_norris import ChuckNorrisJoke, ChuckNorrisServiceData


class ListCreateJokeResource(Resource):
    @property
    def chucknorris_service(self):
        return ChuckNorrisServiceInterface.get_instance(service_pool)

    def get_joke_from_chuck_norris(self, query) -> Optional[List[ChuckNorrisJoke]]:
        service_raw_data = self.chucknorris_service.query_jokes(query)
        service_data = ChuckNorrisServiceData.model_validate(service_raw_data)
        if not service_data.successful:
            return []
        jokes: List[ChuckNorrisJoke] = service_data.data
        return jokes

    @marshal_with(joke_fields)
    def get(self):
        query = request.args.get('query', '')
        if query.strip() == '':
            return []

        jokes = Joke.query.filter(
            Joke.value.ilike(f'%{query}%'),
            Joke.is_deleted == False
        ).all()

        return [
            *list(jokes),
            *self.get_joke_from_chuck_norris(query),
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
