from flask import Blueprint, jsonify, request

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/anomaly_analysis', methods=['GET'])
def get_all_anomalies():
  from app.models import get_all_anomalies  
  anomalies = get_all_anomalies()

  return jsonify(anomalies)

@api_blueprint.route('/api/anomaly_analysis', methods=['POST'])
def create_anomaly():
  data = request.get_json()
  return jsonify(data)
