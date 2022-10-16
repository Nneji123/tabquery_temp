from transformers import TapasTokenizer, TFTapasForQuestionAnswering

model_name = "google/tapas-base-finetuned-wtq"
model = TFTapasForQuestionAnswering.from_pretrained(model_name)
tokenizer = TapasTokenizer.from_pretrained(model_name)
print("Model loaded")