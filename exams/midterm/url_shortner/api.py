from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
from hashids import Hashids



app = Flask(__name__)
api = Api(app)

urls = {}
parser = reqparse.RequestParser()
hashids = Hashids()

class Url(Resource):
    def get(self, url_hash):
        for uri in urls.items():
            if uri['id'] == hashids.decrypt(url_hash):
                return {'id': uri.id, 'short': uri.short, 'url': uri.url}, 201
        abort(409, message="url {} doesn't exist".format(url_hash))

    def delete(self, url_hash):
            id = hashids.decrypt(url_hash)
            url = urls['url{}'.format(id)]
            try:
                del urls['url{}'.format(id)]
            except KeyError as ex:
                abort(409, message="url {} doesn't exist".format(url_hash))
            return url, 201

class ShortenUrl(Resource):
    def post(self):
        args = parser.parse_args()
        if len(urls) != 0:
            url_id = int(max(urls.keys()).lstrip('url')) + 1
        else:
            url_id = 1
        short = hashids.encrypt(url_id)
        id = url_id
        url_id = 'url%i' % url_id
        url = args['url']
        urls[url_id] = {'id':id, 'short':request.base_url+ '/' + short, 'url': url}
        return urls[url_id], 201


api.add_resource(ShortenUrl, '/url')
api.add_resource(Url, '/url/<string:url_hash>')

if __name__ == '__main__':
    app.run(debug=True)