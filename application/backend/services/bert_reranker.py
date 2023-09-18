import pandas as pd
import numpy as np
from tqdm import tnrange
from sklearn.metrics import jaccard_score
import scipy


from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("bert-base-nli-mean-tokens")  # BERT BASE
# embedder = SentenceTransformer('bert-large-nli-stsb-mean-tokens') # LARGE BERT


def rerank(results, query):
    corpus_embeddings = embedder.encode(results)

    query_embeddings = embedder.encode([query])
    search_results = results

    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    closest_n = 5
    distances = scipy.spatial.distance.cdist(
        query_embeddings, corpus_embeddings, "cosine"
    )[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    for idx, distance in results[0:closest_n]:
        print(idx, results[idx], "(Score: %.4f)" % (1 - distance))

    print(results)
    required_list = []
    for i, r in enumerate(results):
        print(search_results[i])
        required_list.append(search_results[i])
        if search_results[i] != required_list[i]:
            print("mismatched:")

    return required_list


# docs=[
#      "idk what to say if this is first time maybe just new account, or if it's funding\n\nmaybe try other places eg. Coinbase/Coinbase Pro(what I use) I've never used Blockchain(.com) before.",
#      "You're fine, it'll show up.\n\nGet the TX ID from the sender to see -- maybe they put a low fee on it and it'll take a bit to confirm." ,
#      'Contact blockchain man, instead of repeating this question here.',
#      "But in the spirit of an AMA, favorite video game? And WHY?  :"]
# query='tell me about Blockchain'
# rerank(docs, query)

# pip3 install torch==1.2.0 torchvision==0.4.0
