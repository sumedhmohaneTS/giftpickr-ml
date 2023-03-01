from flask import request
from services.recommendation_service import RecommendationService
from flask_restful import Api, Resource


class RecommendationController(Resource):
    def __init__(self):
        self.service = RecommendationService()

    @classmethod
    def register(cls, api):
        api.add_resource(cls, '/recommendation')

    def get(self):
        req_data = request.json
        age = req_data.get('age')
        gender = req_data.get('gender').split(",")
        occasion = req_data.get('occasion').split(",")
        relationship = req_data.get('relationship').split(",")
        interests = req_data.get('interests').split(",")

        # check if inputs are None, set default values if necessary
        if age is None:
            age = 25  # default age
        if gender is None:
            gender = ['male', 'female']  # default gender
        if occasion is None:
            occasion = ['christmas', 'holi', 'birthday', 'wedding', 'anniversary',
                        'graduation', 'valentine', 'mothersday', 'fathersday']  # default occasion
        if relationship is None:
            relationship = ['friend', 'father', 'mother',
                            'sibling', 'spouse', 'child']  # default relationship
        if interests is None:
            interests = ['sports', 'technology', 'travel',
                         'books', 'food']  # default interests

        result = RecommendationService.get_recommendations(
            age, gender, occasion, relationship, interests)

        return result
