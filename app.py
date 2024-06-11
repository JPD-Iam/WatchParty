from flask import Flask, render_template,request,jsonify
from app_requests import get_recommendations
application= Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/recommend', methods=['POST'])
def recommend_route():
    user_input=request.json.get('description','')
    if not user_input:
        return jsonify({"error": "Invalid input"}), 400
    recommendations = get_recommendations(user_input)
    return jsonify(recommendations)
if  __name__=="__main__":
    application.run(host="0.0.0.0",debug=False)

