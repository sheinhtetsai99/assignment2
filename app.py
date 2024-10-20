from flask import Flask,render_template,request
import os
from dotenv import load_dotenv, dotenv_values 
import openai
from textblob import TextBlob
import pickle
from sentence_transformers import SentenceTransformer

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
client = openai.OpenAI()

# Load the ML model
with open('spam_classifier/logistic_regression_model.pkl', 'rb') as model_file:
    spam_classifier_model = pickle.load(model_file)

bert_model = SentenceTransformer('bert-base-nli-mean-tokens')

# with open('spam_classifier/sentence_transformer_bert.pkl', 'rb') as model_file:
#     bert_model = pickle.load(model_file)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/ai_agent", methods=["GET","POST"])
def ai_agent():
    return(render_template("ai_agent.html"))

@app.route("/spam_classifier", methods=["GET","POST"])
def spam_classifier():
    return(render_template("model_input_page.html"))

@app.route("/ai_agent_reply", methods=["GET","POST"])
def ai_agent_reply():
    q = request.form.get("q")
    r = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": q}],
    )
    r = r.choices[0].message.content
    return(render_template("ai_agent_reply.html",r=r))

@app.route("/prediction", methods=["GET","POST"])
def prediction():
    return(render_template("index.html"))

@app.route("/joke", methods=["GET","POST"])
def joke():
    return(render_template("joke.html"))

@app.route("/sentiment_analysis", methods=["GET","POST"])
def sentiment_analysis():
    return render_template("sentiment_analysis.html")


@app.route("/sentiment_analysis_reply", methods=["GET","POST"])
def sentiment_analysis_reply():
    text = request.form.get("text")
    analysis = TextBlob(text).sentiment
    return render_template("sentiment_analysis_reply.html", 
                           text=text, 
                           polarity=round(analysis.polarity, 2), 
                           subjectivity=round(analysis.subjectivity, 2))

@app.route("/spam_classifier", methods=["GET"])
def spam_classifier_input():
    return render_template("model_input_page.html")

@app.route("/ml_model_predict", methods=["POST"])
def ml_model_predict():
    user_input = request.form.get("user_input")
    
    # Preprocess the input if necessary
    new_string_vec = bert_model.encode([user_input])

        # Reshape the input to 2D array
    new_string_vec_2d = new_string_vec.reshape(1, -1)
    
    # Make prediction using the loaded model
    prediction = spam_classifier_model.predict(new_string_vec_2d)

    print(f"Prediction: {prediction[0]}")
    
    # Convert prediction to human-readable format

    return render_template("model_output_page.html", input=user_input, prediction=prediction[0])

if __name__ == "__main__":
    app.run()