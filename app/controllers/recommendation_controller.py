from flask import Blueprint, request
from app.services.recommendation_service import RecommendationService

recommendation_controller = Blueprint('recommendation_controller', __name__)

@recommendation_controller.route('/recommendation', methods=['POST'])
def get_recommendations():
    req_data = request.json
    age = req_data.get('age')
    gender = req_data.get('gender')
    occasion = req_data.get('occasion')
    relationship = req_data.get('relationship')
    interests = req_data.get('interests')

    # check if inputs are None, set default values if necessary
    if age is None:
        age = 25 # default age
    if gender is None:
        gender = 'unspecified' # default gender
    if occasion is None:
        occasion = 'any' # default occasion
    if relationship is None:
        relationship = 'any' # default relationship
    if interests is None:
        interests = [] # default interests

    result = recommendation_service.get_recommendations(age, gender, occasion, relationship, interests)

    return result
