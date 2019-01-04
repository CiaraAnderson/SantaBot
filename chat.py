from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import random
#from chatterbot.trainers import ChatterBotCorpusTrainer

##Experimental Date Time
from dateTime import getTime, getDate 

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

bot = ChatBot(
    "ChatBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'IDKnull'
        }
    ],
    response_selection_method=get_random_response, #Comment this out if you want best response
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)

bot.read_only=True #Comment this out if you want the bot to learn based on experience
print("Bot Learn Read Only:" + str(bot.read_only))


#You can comment these out for production later since you won't be training everytime:
#bot.set_trainer(ChatterBotCorpusTrainer)
#bot.train("data/trainingdata.yml")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(bot.get_response(userText))
    if botReply == "IDKnull":
        # Create a list of non-responses:
        noResponse = ["I don't know.", "I'm not sure about that.", "Is there a different way you can ask that?","I don't have a response for that.","I will have to give that some thought.","I don't really know what you are asking."]
        botReply = random.choice(noResponse)
    elif botReply == "getTIME":
        botReply = getTime()
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        print(getDate())
    return botReply

if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=80)
