from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


# from transformers import pipeline

# A docstring usada pelos agentes para entender a funcão
def get_sentimento(topic: str):
    """
        Retorna o sentimento do texto. POSITIVE para sentimento bom. NEGATIVE sentimento ruim.
        
        Args:
        topic (str): Texto a ser realizado a análise de sentimento.
    """
    # Usando NLTK. Baixar recursos do VADER
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    
    result = sia.polarity_scores(topic)
    
    # Usando recurso do HuggingFace    
    #model_id = "distilbert-base-uncased-finetuned-sst-2-english"
    #nlp = pipeline("sentiment-analysis", model=model_id)
    #resp = nlp(topic)

    return result
