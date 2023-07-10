import nltk
from nltk.corpus import brown
import sys
from logit_bias import LogitBias
import json
import time
import random
from tqdm import tqdm

nltk.download('brown')

def save_to_file(word_paths: dict, filename: str) -> None: 
    with open(filename, 'w') as f: 
        json.dump(word_paths, f)

def suppression_loop(API_KEY: str, MODEL: str, suppression_word: str, temperature: float=0, request_timeout: int=10, max_words: int=10) -> list:
    BIAS = -100
    suppressed_phrases = [suppression_word]
    logit_bias_generator = LogitBias(API_KEY, MODEL, suppressed_phrases, BIAS, request_timeout=request_timeout)
    word_path = []
    system_message = "You can only produce real single words. Repeat the word you see in the prompt."
    
    try: 
        for _ in range(max_words):
            PROMPT = f"{suppression_word}"
            response = logit_bias_generator.generate_response(PROMPT, temperature, system_message)
            word_path.append(response)
            suppressed_phrases.append(response)
            logit_bias_generator = LogitBias(API_KEY, MODEL, suppressed_phrases, BIAS, request_timeout=request_timeout)
            time.sleep(0.1) # sleep for 0.1 seconds to avoid hitting the API rate limit 
    except Exception as e:
        print(f"Exception for word {suppression_word}: {e}")
    
    return word_path

if __name__ == "__main__": 
    API_KEY = 'API_KEY' 
    MODEL = "gpt-3.5-turbo"
    word_freqs = nltk.FreqDist(w.lower() for w in brown.words())
    DICTIONARY = [word for word, freq in word_freqs.most_common(10000)] # using the 10000 most common words 
    random.shuffle(DICTIONARY)
    # save dictionary to file
    save_to_file(DICTIONARY, "dictionary.json")
    EXTRA_SUPPRESSED_TOKENS = [] 
    BIAS = -100 
    TEMPERATURE = 0 
    MAX_WORDS = 1 # Change this to control the number of words for each path (increases run time order something or whatever)
    
    word_paths = {} 
    for word in tqdm(DICTIONARY):
        word_path = suppression_loop(API_KEY, MODEL, word, TEMPERATURE, 10, MAX_WORDS)
        word_paths[word] = word_path
        if len(word_paths) % 5 == 0:
            save_to_file(word_paths, "word_paths_test.json")

    save_to_file(word_paths, "word_paths_test.json")


