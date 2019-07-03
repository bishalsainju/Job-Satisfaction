import json
import config.config as config

config = config.Config()


def convert_txt_to_json(txt_file, json_file):
    texts = open(txt_file, mode='r', encoding='utf8').read().splitlines()
    dict = {}
    for term in texts:
        term = term[1:len(term)-1]
        word = term[:term.find(',')]
        count = term[term.find(',')+2:]
        dict[word] = count
    with open(json_file, 'w') as fp:
        json.dump(dict, fp)


if __name__ == '__main__':
    file_path = config.data_path + '/overall/term_frequency'
    txt_file = file_path + '/2_gram_satisfied.txt'
    json_file = file_path + '/2_gram_satisfied.json'
    convert_txt_to_json(txt_file, json_file)
