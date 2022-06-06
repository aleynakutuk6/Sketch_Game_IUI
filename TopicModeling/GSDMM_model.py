from gsdmm import MovieGroupProcess
import pickle
import numpy as np
from nltk.stem.porter import PorterStemmer

num_topics = 3
main_path = 'C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/TopicModeling/'
docs = []

def stemmer_porter(text_list):
    porter = PorterStemmer()
    return_list = []
    for i in range(len(text_list)):
        return_list.append(porter.stem(text_list[i]))
    return(return_list)

def display_doc(docs):
    i=0
    for d in docs:
        #print("docs number {} includes words: {}".format(i, d))
        i +=1

def top_words(distribution, top_index, num_words):
 for topic in top_index:
  pairs = sorted([(k, v) for k, v in distribution[topic].items()], key=lambda x: x[1], reverse=True)
  #print(f"Cluster {topic} : {pairs[:num_words]}")
  #print('-' * 30)

with open(main_path + "data/csv_files/open_images_Small.csv", encoding="utf-8") as file:
    data = file.readlines()
    i=0
    for d in data[1:]:
        line = d.split(",")[0].split(" ")
        docs.append(line)
        if i == 10:
            break
        i += 1

display_doc(docs)
mgp = MovieGroupProcess(K=num_topics, alpha=0.1, beta=0.1, n_iters=30)
vocab = set(x for doc in docs for x in doc)
n_terms = len(vocab)
y = mgp.fit(docs, n_terms)

# Save model
with open( main_path + 'model/open_images_Small.model', "wb") as f:
 pickle.dump(mgp, f)
 f.close()

doc_count = np.array(mgp.cluster_doc_count)
print('Number of documents per topic :', doc_count)
print('*'*20)
# Topics sorted by the number of document they are allocated to
top_index = doc_count.argsort()[-10:][::-1]
print('Most important clusters (by number of docs inside):', top_index)
print('*'*20)
# Show the top 4 words in term frequency for each cluster
top_words(mgp.cluster_word_distribution, top_index, 4)

quickdraw_classes = []
with open("C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/Sketchformer/prep_data/quickdraw/list_quickdraw.txt") as file:
    quickdraw_classes = file.readlines()

quickdraw_classes = [stemmer_porter([c[:-1]])[0] for c in quickdraw_classes]
len_quickdraw = len(quickdraw_classes)
#print("Number of quickdraw classes is:", len_quickdraw)

topic_word_matrix = np.zeros((num_topics, len_quickdraw))
t = 0
for d in mgp.cluster_word_distribution:
  i = 0
  for c in quickdraw_classes:
    if c in d.keys():
      count = d[c]
      print("Class {} ({}th class in 345) appeared {} times in topic number {}".format(c, i, count, t))
      topic_word_matrix[t][i] = count
    i += 1
  t += 1

total_matrix = np.sum(topic_word_matrix, axis=0)
topic_word = np.divide(topic_word_matrix, total_matrix, out=np.zeros_like(topic_word_matrix), where=total_matrix!=0)

np.save(main_path + 'data/topic_word_new.npy', topic_word)
