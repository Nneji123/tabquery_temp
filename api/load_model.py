from transformers import TapasTokenizer, TFTapasForQuestionAnswering

def main():
    """
    The main function is the entry point of the program.
    It creates a model and tokenizer, then runs an interactive loop so you can 
    interactively input a question. It will print the answer from the model.
    
    Args:
    
    Returns:
        The model and tokenizer objects
    """
    model_name = "google/tapas-base-finetuned-wtq"
    model = TFTapasForQuestionAnswering.from_pretrained(model_name)
    tokenizer = TapasTokenizer.from_pretrained(model_name)
    print("Model loaded")
    
main()
