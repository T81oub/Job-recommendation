from flask import Flask, jsonify, request
from recommendationsystem import give_rec
app = Flask(__name__)
@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the user info from the request body
    user_info = request.json['user_info']

    # Call the give_rec function to get job recommendations
    top_job_titles, top_job_companies, top_job_descriptions = give_rec(user_info)

    # Create a dictionary to store the recommendations
    results = {
        'job_titles': top_job_titles,
        'job_companies': top_job_companies,
        'job_descriptions': top_job_descriptions
    }

    # Return the results as JSON
    return jsonify(results)

if __name__ == "__main__":

    app.run(debug=True)
