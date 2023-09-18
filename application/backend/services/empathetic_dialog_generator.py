from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class EmpatheticDialogGenerator:
    def __init__(
        self,
    ):
        self.empathetic_dialogue_model = AutoModelForSeq2SeqLM.from_pretrained(
            "madhavappaneni/t5-small-empathetic-dialogue",
            use_auth_token="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",
        )
        self.empathetic_dialogue_tokenizer = AutoTokenizer.from_pretrained(
            "madhavappaneni/t5-small-empathetic-dialogue",
            use_auth_token="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",
        )

    def generate_response(self, input_text, context):
        input_sequence = f"{' '.join(context)}</s>{input_text}"
        input_ids = self.empathetic_dialogue_tokenizer.encode(
            input_sequence, return_tensors="pt"
        )
        outputs = self.empathetic_dialogue_model.generate(input_ids, max_length=50)
        generated_text = self.empathetic_dialogue_tokenizer.decode(
            outputs[0], skip_special_tokens=True
        )
        return generated_text
