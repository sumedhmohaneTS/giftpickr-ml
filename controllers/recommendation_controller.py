from flask import request
from services.recommendation_service import RecommendationService
from flask_restful import Api, Resource


class RecommendationController(Resource):
    def __init__(self):
        self.service = RecommendationService()

    @classmethod
    def register(cls, api, prefix):
        api.add_resource(cls, prefix+'/recommendation')

    def get(self):
        req_data = request.args

        age = int(req_data.get('age'))
        gender = req_data.get('gender')
        relationship = (req_data.get('relationship'))
        occasion = (req_data.get('occasion'))
        if req_data.get('interests') is not None:
            interests = (req_data.get('interests')).split(
                ",")  # can be multiple

        # check if inputs are None, set default values if necessary
        if age is None:
            age = 25  # default age
        if gender is None:
            gender = 'any'  # default gender
        if occasion is None:
            occasion = ['christmas', 'holi', 'birthday', 'wedding', 'anniversary',
                        'graduation', 'valentine', 'mothersday', 'fathersday']  # default occasion
        if relationship is None:
            relationship = ['friend', 'father', 'mother',
                            'sibling', 'spouse', 'child']  # default relationship
        if interests is None:
            interests = ['sports', 'technology', 'travel',
                         'books', 'food']  # default interests

        result = self.service.get_recommendations(
            age, gender, occasion, relationship, interests)

        return result
