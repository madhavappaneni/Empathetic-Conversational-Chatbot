from transformers import AutoModelWithLMHead, AutoTokenizer
import string
import traceback


def generate_with_question_stop(
    prompt, model, tokenizer, input_ids, attention_mask, **kwargs
):
    beam_outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_mask, **kwargs
    )
    final_outputs = []
    for beam_output in beam_outputs:
        decoded_output = tokenizer.decode(beam_output, skip_special_tokens=True)[
            len(prompt) :
        ]
        try:
            if decoded_output:
                while decoded_output and decoded_output[0] in string.punctuation:
                    decoded_output = decoded_output[1:].lstrip()
                first_sentence = decoded_output.split(".")[0].strip()
                # print("'?' in first_sentence:" +  decoded_output)
                # print('?' in first_sentence)
                if "?" in first_sentence:
                    continue
                while decoded_output and decoded_output[0] in string.punctuation:
                    decoded_output = decoded_output[1:].lstrip()
                sentences = decoded_output.split(".")
                last_sentence = ".".join(sentences[:-1]).strip()
                final_outputs.append(last_sentence)
        except:
            traceback.print_exc()
    return final_outputs


class RedditGenerator:
    def __init__(
        self,
    ):
        self.reddit_tokenizer = AutoTokenizer.from_pretrained(
            "skunusot/finetuned-reddit-gpt2",
            use_auth_token="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",
        )
        self.reddit_model = AutoModelWithLMHead.from_pretrained(
            "skunusot/finetuned-reddit-gpt2",
            use_auth_token="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",
        )

    def generate_response_from_generator(self, input_text, multiple=True):
        inp = self.reddit_tokenizer(input_text, return_tensors="pt")
        input_ids = inp["input_ids"]
        a = inp["attention_mask"]
        # outputs = self.reddit_model.generate(input_ids, max_length=75, no_repeat_ngram_size=2)
        # generated_text = self.reddit_tokenizer.decode(outputs[0], skip_special_tokens=True)[len(input_text):]
        # while generated_text and generated_text[0] in string.punctuation:
        #     generated_text = generated_text[1:].lstrip()
        # sentences = generated_text.split('.')
        # generated_text = '.'.join(sentences[:-1]).strip()
        # return generated_text
        beam_outputs = generate_with_question_stop(
            prompt=input_text,
            model=self.reddit_model,
            tokenizer=self.reddit_tokenizer,
            input_ids=input_ids,
            attention_mask=a,
            num_beams=5,
            early_stopping=True,
            do_sample=True,
            min_length=50,
            num_return_sequences=2,
            max_length=75,  # 100 + len(input_ids[0]),
            no_repeat_ngram_size=2,
        )
        if multiple:
            return beam_outputs
        else:
            if len(beam_outputs) > 0:
                return beam_outputs[0]
            else:
                return ""

    def generate_response(self, input_text, context):
        input_sequence = f"{' '.join(context)}</s>{input_text}"
        return self.generate_response_from_generator(
            input_text=input_sequence, multiple=False
        )

    def generate_multiple_responses(self, input_text, context):
        input_sequence = f"{' '.join(context)}</s>{input_text}"
        return self.generate_response_from_generator(input_text=input_sequence)
