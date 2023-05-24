from flask import Flask, render_template ,jsonify , request
from flask_pymongo import PyMongo
import openai

openai.api_key = "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"


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://Joshua_Immanuel9:Cj7india@cluster0.m4yngft.mongodb.net/chat"
mongo = PyMongo(app)
@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    mychats=[chat for chat in chats]
    print(mychats)
    return render_template('index.html')

@app.route("/api",methods=["GET","POST"])
def qa():
    if request.method=="POST":
        question=request.json.get("question")
        chat=mongo.db.chats.find_one({"question":question})
        if(chat):
            data={"question":question,"answer":chat['answer']}
            return jsonify(data)
        else:
          
          response = openai.Completion.create(
              model="text-davinci-003",
              prompt=question,
              temperature=1,
              max_tokens=256,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )
          data={"question":question,"answer":response['choices'][0]['text']}
          mongo.db.chats.insert_one({"question":question,"answer":response['choices'][0]['text']})
          return jsonify(data)
    data={"result":"thank you i am a machine."}
    return jsonify(data)

app.run(debug=True)