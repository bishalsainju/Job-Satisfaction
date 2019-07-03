import config.config as config
import json
import os
from txt_to_json import convert_txt_to_json

config = config.Config()


def jsonCount_to_doc(json_var, num_words=100):
    texts = ""
    min_count = json_var[list(json_var)[num_words-1]]
    for key, value in {k: json_var[k] for k in list(json_var)[:num_words]}.items():
        texts = texts + ((key+" ")*round((int(value)/(int(min_count))))) + "\n"
    return texts


if __name__ == '__main__':
    file_path = config.data_path + "/overall/term_frequency"
    txt_file = file_path + "/2_gram_unsatisfied.txt"
    json_file = file_path + "/2_gram_unsatisfied.json"
    convert_txt_to_json(txt_file, json_file)
    with open(json_file, "r") as f:
        json_var = json.load(f)
    os.remove(json_file)
    with open(config.data_path + "/wordcloud/wc_text.txt", mode="w+", encoding='utf8') as wc_file:
        wc_file.write(jsonCount_to_doc(json_var))

