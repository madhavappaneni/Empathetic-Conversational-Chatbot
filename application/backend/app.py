from flask import Flask, request
from flask_cors import CORS
from services.facts import summarize
from services.dialog_manager import DialogManager
from services.empathetic_dialog_generator import EmpatheticDialogGenerator
from services.chitchat_generator import ChitChatGenerator
from services.reddit_generator import RedditGenerator
from services.neural_reranker import rerank

app = Flask(__name__)
CORS(app)
dialog_manager = DialogManager()
empathetic_dialog_generator = EmpatheticDialogGenerator()
chitchat_generator = ChitChatGenerator()
reddit_generator = RedditGenerator()


app.debug = True  # Turn on debug mode


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("user_message")

    dialog_manager_response = dialog_manager.process_user_message(user_message)
    user_query_topic = dialog_manager_response["topic"]
    user_query_intent = dialog_manager_response["intent"]
    print(dialog_manager_response, "dialog_manager_response")
    empathetic_dialog_response = empathetic_dialog_generator.generate_response(
        user_message, dialog_manager_response["context"]
    )

    print(dialog_manager_response["context"], "context")
    print(dialog_manager_response["context"], "cache")

    chitchat_response = chitchat_generator.generate_response(
        user_message, dialog_manager_response["context"]
    )
    fact_response = ""
    reddit_responses = reddit_generator.generate_multiple_responses(user_message, "")
    for ind, redd_response in enumerate(reddit_responses):
        reranked_responses = rerank(
            dialog_manager_response["intent_probs"],
            [chitchat_response, reddit_responses[0], empathetic_dialog_response],
            user_message,
        )
        current_topic = dialog_manager.inferTopic(redd_response)
        if reranked_responses[0] == redd_response:  # if best reddit response
            if ind == len(reddit_responses) - 1:
                # trigger factual response
                fact_responses = summarize(" ".join(dialog_manager_response["context"]))
                if len(fact_responses) > 0:
                    fact_response = fact_responses[0]["summary_text"]
                    reranked_responses = rerank(
                        [dialog_manager_response["intent_probs"][1]],
                        [fact_response],
                        user_message,
                    )
                print(
                    "Topic Drift "
                    + "user_query_topic: "
                    + user_query_topic
                    + "current_topic: "
                    + current_topic
                )
                break
            if current_topic == user_query_topic:
                break
            else:
                continue
        else:
            break

    chat_bot_response = reranked_responses[0][1]
    if user_query_intent == "empathetic":
        chat_bot_response = empathetic_dialog_response

    return {
        "chat_bot_response": chat_bot_response,
        "dialog_manager_response": dialog_manager_response,
        "reranked_response": reranked_responses[0][1],
        "empathetic_dialog_response": empathetic_dialog_response,
        "chitchat_response": chitchat_response,
        "reddit_response": reddit_responses[0],
        "fact_response": fact_response,
    }


if __name__ == "__main__":
    app.run(port=8080)


# curl -X POST -H "Content-Type: application/json" -d '{"user_message": "How does climate change effect us?"}' http://127.0.0.1:8080/chat
