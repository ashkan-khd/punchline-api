from flask_restful import reqparse, fields

# Request parsers
joke_parser = reqparse.RequestParser()
joke_parser.add_argument('value', type=str, required=True, help='Joke text is required')
joke_parser.add_argument('categories', type=list, location='json', default=[])

# Response fields
joke_fields = {
    'id': fields.String,
    'value': fields.String,
    'categories': fields.Raw,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
}

joke_fields_with_local = {
    **joke_fields,
    'local': fields.Boolean,
}
