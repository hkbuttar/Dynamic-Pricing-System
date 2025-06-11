from flask import Blueprint, jsonify, request
from .pricing_engine import get_adjusted_prices

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/api/prices", methods=["POST"])
def adjust_prices():
    data = request.get_json()
    result = get_adjusted_prices(data)
    return jsonify(result)