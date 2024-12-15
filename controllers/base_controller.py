from flask_restful import Resource


class BaseController(Resource):
    def __init__(self, **kwargs):
        self.decorators = kwargs.get('decorators', [])
        super(BaseController, self).__init__()
