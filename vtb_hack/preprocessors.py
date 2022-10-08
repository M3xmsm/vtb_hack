from typing import List
import re

import numpy as np
from pymorphy2 import MorphAnalyzer
from nltk.stem import WordNetLemmatizer
import torch
from transformers import AutoModel, PreTrainedTokenizerFast


def clean_text(
    text: str,
    ru_stop_list: List[str],
    eng_stop_list: List[str],
    ru_morph: "MorphAnalyzer",
    eng_lemmatizer: "WordNetLemmatizer"
) -> str:
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'http?://\S+|www\.\S+', '', text)
    text = re.sub('[^а-яa-z0-9]+', ' ', text)
    text = " ".join([word for word in text.split(' ') if word not in ru_stop_list])
    text = " ".join([word for word in text.split(' ') if word not in eng_stop_list])
    text = " ".join([ru_morph.parse(word)[0].normal_form for word in text.split(' ')])
    text = " ".join([eng_lemmatizer.lemmatize(word) for word in text.split(' ')])

    # words = []
    # for word in text.split(' '):
    #     parsed_word = ru_morph.parse(word)[0]
    #     if ('NOUN' in parsed_word.tag) or ('LATN' in parsed_word.tag) or ('NUMB' in parsed_word.tag):
    #         words.append(parsed_word.normal_form)
    # text = " ".join(words)

    return text


def text_to_vec(
    text: str,
    model: "AutoModel",
    tokenizer: "PreTrainedTokenizerFast"
) -> np.ndarray:
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()


