from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity


# Load the data
jobs_data = pd.read_csv("data/dice_com-job_us_sample.csv")
new_data = pd.read_csv("data/cleaned_jobs_data.csv")
ps = PorterStemmer()

# Vectorize the "jobdescription" column using CountVectorizer
cv = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1,2))
vectors = cv.fit_transform(new_data['jobdescription']).toarray()
def give_rec(user_info, data=new_data, vectors=vectors):
    # Preprocess the user input
    user_info_processed = " ".join([ps.stem(word) for word in user_info.lower().split()])

    # Vectorize the user input
    user_info_vector = cv.transform([user_info_processed]).toarray()

    # Append the user_info vector to the existing vectors array
    vectors_with_user_info = np.vstack((vectors, user_info_vector))

    # Compute pairwise cosine similarity between vectors
    similarity = cosine_similarity(vectors_with_user_info)

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(similarity[-1]))

    # Sort the scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top 5 most similar jobs
    top_job_indices = [i[0] for i in sim_scores[1:6]]

    # Get the job titles, companies, and job descriptions of the top 5 most similar jobs
    top_job_titles = data['jobtitle'].iloc[top_job_indices].tolist()
    top_job_companies = data['company'].iloc[top_job_indices].tolist()
    top_job_descriptions = data['jobdescription'].iloc[top_job_indices].tolist()

    # Return the results as a tuple of lists
    return top_job_titles, top_job_companies, top_job_descriptions
print(give_rec('C++, Developer, Development, JavaScript, User Interface,HTML'))