from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from nltk.stem import WordNetLemmatizer
from transformers import AutoTokenizer, AutoModel
from transformers import PreTrainedTokenizerFast

from vtb_hack.src.preprocessors import clean_text, text_to_vec

if __name__ == "__main__":
    # nltk.download('stopwords')
    ru_stop_list = stopwords.words('russian')
    eng_stop_list = stopwords.words('english')
    ru_morph = MorphAnalyzer()
    eng_lemmatizer = WordNetLemmatizer()

    text = 'abc'
    text_prep = clean_text(text, ru_stop_list, eng_stop_list, ru_morph, eng_lemmatizer)

    model = AutoModel.from_pretrained("cointegrated/rubert-tiny2")
    tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
    text_to_vec(text_prep, model, tokenizer)
