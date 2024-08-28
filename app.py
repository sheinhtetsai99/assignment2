from flask import Flask,render_template,request
import os
import openai

os.environ["OPENAI_API_KEY"] = "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"
client = openai.OpenAI()

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/ai_agent", methods=["GET","POST"])
def ai_agent():
    return(render_template("ai_agent.html"))

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

if __name__ == "__main__":
    app.run()