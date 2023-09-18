# Topic based Empathetic Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the implementation of the paper:

## [**Topic Based Empathetic Chatbot Focusing on Sentiments**](https://drive.google.com/file/d/10EM9ng-kbrNWuSgi0y2rAqMqazvx1DaX/view?usp=drive_link).

[**Madhav Appaneni**](https://www.linkedin.com/in/madhav-appaneni/)

## Abstract

This paper presents the development of an empathetic chatbot that employs Natural Language Processing (NLP) techniques to engage in chitchat and topical conversations while providing empathetic responses. Chatbots have shown proficiency in specific tasks like providing information and personal assistance. However, their effectiveness in open-ended conversations requires improvement. This need has prompted the development of social bots that aim to communicate with users using human-like emotion, inflection, slang, and other qualities that contribute to a generous conversation.

This project aims to create an end-to-end conversational system capable of delivering empathetic interactions and effectively sharing opinions and factual information on Politics, Environment, Technology, Healthcare, and Education. The analysis presented in this paper provides insights into the components and approaches implemented in developing our chatbot.

### Training and Inference

All the models used are built on top of the models in the Huggingface transformers library.

The code for fine-tuning and evaluation for each component can be found in the respective folders in the models_evaluation and models_finetuning folders


### Datasets:

The following datasets were used for fine-tuning various pre-trained models 
1. [BYU-PCCL chitchat-dataset](https://github.com/BYU-PCCL/chitchat-dataset)
2. [Facebook Research - EmpatheticDialogues
](https://github.com/facebookresearch/EmpatheticDialogues)
3. [Microsoft Botframework - QnA Maker](https://github.com/microsoft/botframework-cli/blob/main/packages/qnamaker/docs/chit-chat-dataset.md)
4. [Custom sourced data from Reddit](https://drive.google.com/file/d/1ODMJmQzGKN5Y0AbSJrMgWBoolztgEx3_/view) with conversations from varied topics like Education, Politics, Healthcare, Environment, etc.

### Code
1. For each component that is described in the paper, the fine-tuning and evaluation Python notebooks can be found in the [Models Finetuning](./models_finetuning/) and [Models Evaluation](./models_evaluation/) sections.
2. A full stack application to interact with the solution developed, including user-context tracking, developed using ReactJS, and Flask is included in the [Application](./application/) directory. Instructions to start the application is present in the [Instructions](./application/README.md)


### Additional Models
To reproduce results published in the paper, use the following fine-tuned models

1. [T5-Small based chit chat conversation generator](https://huggingface.co/madhavappaneni/t5-small-chit-chat-conv)
2. [T5-Small based empathetic dialogue generator](https://huggingface.co/madhavappaneni/t5-small-empathetic-dialogue)
3. [GPT2 based topical dialogue generator](https://shuggingface.co/madhavappanenit5-small-empathetic-dialogue)

## References

Please cite if you found the resources in this repository useful.

```bibtex
@inproceedings{madhav2023topic,
    title = {Topic Based Empathetic Chatbot},
    author = {Madhav Appaneni},
    month = {may},
    year = {2023}
}
```
