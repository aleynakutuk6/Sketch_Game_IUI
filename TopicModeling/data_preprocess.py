import string
import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist
import gensim

nltk.download('stopwords')
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'the', 'a', 'image', 'picture', 'see'])

def w_tokenizer(text):
    tokenizer = WhitespaceTokenizer()
    tokenized_list = tokenizer.tokenize(text)
    return(tokenized_list)

def stemmer_porter(text_list):
    porter = PorterStemmer()
    return_list = []
    for i in range(len(text_list)):
        return_list.append(porter.stem(text_list[i]))
    return(return_list)

paths = []
all_words = []
dataset_words = []
dataset = []

main_path = 'C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/TopicModeling/data/'
p_list = ['jsonl_files/open_images_train_v6_captions.jsonl', 'jsonl_files/ade20k_train_captions.jsonl', 'jsonl_files/coco_train_captions.jsonl', 'jsonl_files/flickr30k_train_captions.jsonl']
csv_list = ['csv_files/open_images_train_v6_captions.csv', 'csv_files/ade20k.csv', 'csv_files/coco.csv', 'csv_files/flickr30k.csv']
for p in p_list:
  paths.append(main_path + p)


def extract_individual_csv_files():
    global paths
    global csv_list
    global stop_words
    global all_words
    global dataset_words
    global dataset

    j = 0
    for path in paths:

        data = []
        with open(path) as f:
            for line in f:
                data.append(json.loads(line))

        dataset = []
        #for i in range(0, len(data)):
        for i in range(0, 10):
            dataset.append(data[i]['caption'])

        print("Captions len: ", len(dataset))

        all_words = []
        dataset_words = []
        fields = "sentences,ctr\n"

        with open(main_path + csv_list[j], 'w', encoding="utf-8") as f:
            f.write(fields)
            for sentence in dataset:
                for punc in string.punctuation:
                    sentence = sentence.replace(punc, " ")
                sentence_words = ""
                ctr = 0
                new_sent = []
                for word in sentence.split():
                    word = word.lower()
                    if (word != ""):
                        if word not in stop_words:
                            word = stemmer_porter(w_tokenizer(word))[0]
                            all_words.append(word)
                            new_sent.append(word)
                            sentence_words += word + " "
                            ctr += 1
                dataset_words.append(new_sent)
                sentence_words = sentence_words[:-1] + "," + str(ctr) + "\n"
                if (len(sentence_words) > 2):
                    f.write(sentence_words)
        j += 1

def extract_total_csv_file():
    global paths
    global stop_words
    global all_words
    global dataset_words
    global dataset

    for path in paths:
        data = []
        with open(path) as f:
            for line in f:
                data.append(json.loads(line))

        for i in range(0, len(data)):
            dataset.append(data[i]['caption'])

    print("Captions len: ", len(dataset))

    fields = "sentences,ctr\n"
    with open(main_path + 'csv_files/open_images_Small.csv', 'w', encoding="utf-8") as f:
        f.write(fields)
        for sentence in dataset:
            for punc in string.punctuation:
                sentence = sentence.replace(punc, " ")
            sentence_words = ""
            ctr = 0
            new_sent = []
            for word in sentence.split():
                word = word.lower()
                if (word != ""):
                    if word not in stop_words:
                        word = stemmer_porter(w_tokenizer(word))[0]
                        all_words.append(word)
                        new_sent.append(word)
                        sentence_words += word + " "
                        ctr += 1
            dataset_words.append(new_sent)
            sentence_words = sentence_words[:-1] + "," + str(ctr) + "\n"
            if (len(sentence_words) > 2):
                f.write(sentence_words)

extract_individual_csv_files()
dataset = pd.read_csv(main_path + 'csv_files/open_images_Small.csv', error_bad_lines=False)

vocab = sorted(list(set(all_words)))
print('{} words total, with a vocabulary size of {}'.format(len(all_words), len(vocab)))
docs = dataset_words
print("Number of documents: ", len(docs))
max_value = dataset["ctr"].max()
max_id = int(dataset[["ctr"]].idxmax())

print('Max caption length: {}'.format(max_value))
print("Max caption id: ", max_id)
max_caption = dataset["sentences"][max_id]
print('Max caption: \n {} '.format(max_caption))

word_freq = FreqDist(all_words)
word_freq.most_common(20)

most_common_count = [x[1] for x in word_freq.most_common(20)]
most_common_word = [x[0] for x in word_freq.most_common(20)]

top_20_dictionary = dict(zip(most_common_word, most_common_count))

dictionary = gensim.corpora.Dictionary(dataset_words)
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break

corpus = [dictionary.doc2bow(text) for text in dataset_words]