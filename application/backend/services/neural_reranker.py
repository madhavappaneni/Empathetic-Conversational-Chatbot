from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_card = "microsoft/DialogRPT-human-vs-rand"
tokenizer = AutoTokenizer.from_pretrained(model_card)
model = AutoModelForSequenceClassification.from_pretrained(model_card)


def score(cxt, hyp):
    model_input = tokenizer.encode(cxt + "<|endoftext|>" + hyp, return_tensors="pt")
    result = model(model_input, return_dict=True)
    return torch.sigmoid(result.logits)


def rerank(intent_probs, results, query):
    # required list is list of reranked responses in order
    search_results = results
    # search_results = [(score(query, response).squeeze().item() * intent_probs[i], response) for i, response in enumerate(results)]
    # search_results = sorted(search_results, key=lambda x: -x[0])
    # print(search_results)
    search_results = [
        (score(query, response).squeeze().item(), response) for response in results
    ]
    search_results = sorted(search_results, key=lambda x: -x[0])
    print(search_results)

    return search_results


# docs=[
#      "idk what to say if this is first time maybe just new account, or if it's funding\n\nmaybe try other places eg. Coinbase/Coinbase Pro(what I use) I've never used Blockchain(.com) before.",
#      "You're fine, it'll show up.\n\nGet the TX ID from the sender to see -- maybe they put a low fee on it and it'll take a bit to confirm." ,
#      'Contact blockchain man, instead of repeating this question here.',
#      "But in the spirit of an AMA, favorite video game? And WHY?  :"]
# query='tell me about Blockchain'
# rerank(docs, query)
