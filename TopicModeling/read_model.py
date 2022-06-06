import pickle
import json
import numpy as np

main_path = 'C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/TopicModeling/'

eps = 1e-8

infile = open(main_path + 'model/all_captions.model', 'rb')
mgp = pickle.load(infile)
infile.close()

print(mgp.__dict__.keys())
# print(mgp.cluster_doc_count)

topic_words = mgp.cluster_word_distribution

word_ids = {}
last_id = 0
for t in range(len(topic_words)):
 for word in topic_words[t].keys():
  if word not in word_ids.keys():
   word_ids[word] = last_id
   last_id += 1

word_topic_mtx = np.zeros((len(topic_words), last_id))

for t in range(len(topic_words)):
 for word in topic_words[t].keys():
  word_id = word_ids[word]
  word_topic_mtx[t, word_id] += 1

total_matrix = np.sum(word_topic_mtx, axis=0)
word_topic_mtx = np.divide(word_topic_mtx, total_matrix, out=np.zeros_like(word_topic_mtx), where=total_matrix!=0)

# print(word_topic_mtx)

f = open(main_path + 'data/image_ids.json')
data = json.load(f)
f.close()

topics_list = {}
for i in range(len(topic_words)):
 topics_list[i] = []

for doc in data.keys():
 words = doc.split(" ")
 indices = []
 for word in words:
  indices.append(word_ids[word])

 sub_mtx = word_topic_mtx[:, indices] + eps
 best_topic_id = np.argmax(np.prod(sub_mtx, axis=1))
 topics_list[best_topic_id].append(doc)

with open(main_path + "data/topics_docs.json", "w") as outfile:
 json.dump(topics_list, outfile)