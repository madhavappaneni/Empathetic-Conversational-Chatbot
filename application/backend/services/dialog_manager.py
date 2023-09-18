# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 17:46:03 2023

@author: Madhav Appaneni
"""
from transformers import (
    AutoTokenizer,
    DistilBertForSequenceClassification,
    AutoModelForSequenceClassification,
    RobertaTokenizer,
    RobertaForSequenceClassification,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    pipeline,
)
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers import SentenceTransformer, util
from scipy.special import expit
import torch

# from textblob import TextBlob
from functools import reduce

# Enitity types
label_names = ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]
id2label = {
    0: "O",
    1: "B-PER",
    2: "I-PER",
    3: "B-ORG",
    4: "I-ORG",
    5: "B-LOC",
    6: "I-LOC",
}
label2id = {
    "O": 0,
    "B-PER": 1,
    "I-PER": 2,
    "B-ORG": 3,
    "I-ORG": 4,
    "B-LOC": 5,
    "I-LOC": 6,
}
# Label to dataset map
label2intent = {0: "chitchat", 1: "reddit", 2: "empathetic"}

# Label to topic map
label2topic = {
    0: "education",
    1: "politics",
    2: "healthcare",
    3: "environment",
    4: "technology",
    5: "unknown",
}

# correct spelling and combine corrected spelling with the original spelling.
# def spellFix(utterance):
#     sentence = TextBlob(utterance)
#     result = sentence.correct()
#     utterance = utterance.split(" ")
#     result = result.split(" ")
#     updated_sentence=[]
#     for i,w in enumerate(utterance):
#         updated_sentence.append(w)
#         if w != result[i]:
#             updated_sentence.append(result[i])
#     return reduce(lambda a,b: a+" "+b,updated_sentence)


# align tokenized words and entity tags with original words.
def wordEntityAlignment(entities):
    # print(entities)
    entities = {e["word"]: e["entity_group"] for e in entities}
    # words = list(entities.keys())
    # i = 0
    # entity_spans = {}
    # print(entities)
    # while i < len(words)-1:
    #     if int(entities[words[i]]) == int(entities[words[i+1]])-1:
    #         print("here")
    #         entity_spans[words[i]+" "+words[i+1]] = label_names[int(entities[words[i]])][-3:]
    #         i+=2
    #     else:
    #         print(i)
    #         entity_spans[words[i]] = label_names[int(entities[words[i]])][-3:]
    #         i+=1
    # if int(entities[words[-1]]) in [1,3,5]:
    #     entity_spans[words[-1]] = label_names[int(entities[words[-1]])][-3:]
    return entities


class DialogManager:
    def __init__(
        self,
    ):
        # Init tokenizers
        self.topic_tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        # self.intent_tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        self.intent_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.ner_tokenizer = AutoTokenizer.from_pretrained(
            "sentientconch/final_ner",
            use_auth_token="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",
        )

        # Init models
        self.topic_model = AutoModelForSequenceClassification.from_pretrained(
            "sentientconch/topic_classifier",
            num_labels=6,
            use_auth_token="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",
        )
        # self.intent_model = RobertaForSequenceClassification.from_pretrained('sentientconch/intent_classifier_short_sent', num_labels=3, use_auth_token='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')
        self.intent_model = DistilBertForSequenceClassification.from_pretrained(
            "sentientconch/intent_classifier_large",
            num_labels=3,
            use_auth_token="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",
        )
        # self.ner_model = AutoModelForTokenClassification.from_pretrained("sentientconch/final_ner", use_auth_token='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')

        # self.ner_pipeline = pipeline(model=self.ner_model, tokenizer=self.ner_tokenizer,  aggregation_strategy="simple")
        self.ner_pipeline = pipeline(
            "ner",
            model="sentientconch/final_ner",
            aggregation_strategy="first",
            use_auth_token="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",
        )
        # bi-encoder to measure sentence similarity
        self.besm = SentenceTransformer("all-mpnet-base-v2")

        self.context = []  # running context, flushed after detecting discontinuity
        self.cache = (
            []
        )  # context cache, flushed at the end of the program, can be used to fetch previous context if elements in running context match an entry in cache
        self.last_input = None  # Last user utterance to track continuity

    # Fetch entites from text.
    def entitiesFromText(self, utterance):
        entities = self.ner_pipeline(utterance)
        entities = wordEntityAlignment(entities)
        # print(entities)
        return entities

    # Infer the topic of conversation from user utterance (applies only to Reddit generator)
    def inferTopic(self, utterance):
        encodings = self.topic_tokenizer(
            [utterance], padding=True, truncation=True, return_tensors="pt"
        )
        result = self.topic_model(
            encodings["input_ids"], attention_mask=encodings["attention_mask"]
        )[0].argmax(1)
        return label2topic[result.item()]

    # Infer Intent from user utterance to select the appropriate generator.
    def inferIntent(self, utterance):
        encodings = self.intent_tokenizer(
            [utterance], padding=True, truncation=True, return_tensors="pt"
        )
        # print(self.intent_model(encodings["input_ids"], attention_mask=encodings["attention_mask"])[0])
        logits = self.intent_model(
            encodings["input_ids"], attention_mask=encodings["attention_mask"]
        )[0]
        result = logits.argmax(1)
        # print(logits)
        probs = logits.softmax(1)
        result = self.intent_model(
            encodings["input_ids"], attention_mask=encodings["attention_mask"]
        )[0].argmax(1)
        return label2intent[result.item()], probs[0].tolist()

    # Compute similarity between consecutive user utterances
    def biencoder(self, inputs):
        return abs(
            float(
                util.cos_sim(self.besm.encode(inputs[0]), self.besm.encode(inputs[1]))[
                    0
                ][0]
            )
        )

    # Fill, flush running context and cache.
    def track_context(self, text):
        if not self.last_input:
            self.last_input = text
            entities = self.entitiesFromText(text)
            entity_list = [
                k
                for k, v in entities.items()
                if v != "O" and "[CLS]" not in k and "[SEP]" not in k
            ]
            # print(entity_list)
            list(map(lambda x: self.context.append(x), entity_list))
            return

        related = self.biencoder([text, self.last_input])
        # print(related)
        if related >= 0.3:
            entities = self.entitiesFromText(text)
            entity_list = [
                k
                for k, v in entities.items()
                if v != "O" and "[CLS]" not in k and "[SEP]" not in k
            ]
            # print(entities)
            list(map(lambda x: self.context.append(x), entity_list))
            # return
        else:
            if len(self.context):
                self.cache.append(self.context)
            self.context = []
            entities = self.entitiesFromText(text)
            entity_list = [
                k
                for k, v in entities.items()
                if v != "O" and "[CLS]" not in k and "[SEP]" not in k
            ]
            # print(entities)
            list(map(lambda x: self.context.append(x), entity_list))
            # return None

    def process_user_message(self, utterance):
        intent, intent_probs = self.inferIntent(utterance)
        topic = self.inferTopic(utterance)
        self.track_context(utterance)
        cache = self.cache.copy()
        context = self.context.copy()

        output = {
            "intent": intent,
            "intent_probs": intent_probs,
            "topic": topic,
            "context": context,
            "cache": cache,
        }

        # self.track_context(utterance)
        # print(output)
        return output


if __name__ == "__main__":
    dm = DialogManager()
    while 1:
        utterance = input("prompt:\n")
        entities = dm.entitiesFromText(utterance)
        # for k,v in entities.items():
        #     print(k+" : "+v)
        print("Entities")
        print(entities)
        print("----------")
        output = dm.process_user_message(utterance)
        for k, v in output.items():
            print(k)
            print(v)
            print("---------")
        print(output)
        # i, ip = dm.inferIntent(utterance)
        # t = dm.inferTopic(utterance)
        # dm.track_context(utterance)
        # print(dm.context)
        # print(dm.cache)
        # print(i)
        # print(ip)
        # print(t)
