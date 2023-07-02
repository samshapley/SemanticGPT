import nltk
from nltk.corpus import brown
from SemanticGPT.logit_bias import LogitBias
import json
import time
import random
from tqdm import tqdm

nltk.download('brown')

def get_word_paths(API_KEY: str, MODEL: str, DICTIONARY: list, EXTRA_SUPPRESSED_TOKENS: list[int], BIAS: int, TEMPERATURE: float, MAX_WORDS: int) -> dict: 
    word_paths = {} 

    # Randomize the order of the words in the dictionary
    # random.shuffle(DICTIONARY)

    
    for word in tqdm(DICTIONARY): 

        suppressed_phrases = [word]
        logit_bias_generator = LogitBias(API_KEY, MODEL, suppressed_phrases, EXTRA_SUPPRESSED_TOKENS, BIAS) 
        word_path = [] 

        system_message = "Repeat the word. Only respond with a real word. Assume all words entered are real words."

        
        try: 
            for _ in range(MAX_WORDS): 
                PROMPT = f"{word}" 
                response = next(logit_bias_generator.generate_responses(PROMPT, 1, TEMPERATURE, system_message)) 
                if response == word:
                    print(f"word duplicated, {word}")
                word_path.append(response) 
                suppressed_phrases.append(response)
                logit_bias_generator = LogitBias(API_KEY, MODEL, suppressed_phrases, EXTRA_SUPPRESSED_TOKENS, BIAS)

                time.sleep(0.1) # sleep for 0.1 seconds to avoid hitting the API rate limit 
        except Exception as e:
            print(f"Exception for word {word}: {e}")

        word_paths[word] = word_path 

        # every 100 words, save the word paths to a file, appending new words, not overwriting
        if len(word_paths) % 100 == 0:
            save_to_file(word_paths, "word_paths.json")



    return word_paths

def save_to_file(word_paths: dict, filename: str) -> None: 
    with open(filename, 'w') as f: 
        json.dump(word_paths, f)

if __name__ == "__main__": 
    API_KEY = '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' 
    MODEL = "gpt-4-0613"
    word_freqs = nltk.FreqDist(w.lower() for w in brown.words())
    DICTIONARY = [word for word, freq in word_freqs.most_common(10000)] # using the 10000 most common words 
    # save dictionary to file
    save_to_file(DICTIONARY, "dictionary.json")
    EXTRA_SUPPRESSED_TOKENS = [] 
    BIAS = -100 
    TEMPERATURE = 0 
    MAX_WORDS = 3 # Change this to control the number of words for each path (increases run time order something or whatever)
    word_paths = get_word_paths(API_KEY, MODEL, DICTIONARY, EXTRA_SUPPRESSED_TOKENS, BIAS, TEMPERATURE, MAX_WORDS) 
    save_to_file(word_paths, "word_paths_gpt-4.json")
