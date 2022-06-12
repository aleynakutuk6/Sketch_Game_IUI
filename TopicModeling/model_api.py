import numpy as np
import itertools
import json
from nltk.stem.porter import PorterStemmer

porter = PorterStemmer()
main_path = 'C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/TopicModeling/'
topic_word = np.load(main_path + 'data/topic_word_WITH_CONTEXT.npy')
quickdraw_classes = []
context_list = ["bakery", "sea", "bathroom", "school", "airport", "river", "cafe", "farm", "sports", "hospital"]

f = open(main_path + 'data/topic_img_mapping.json')
topic_img_mapping = json.load(f)
f.close()
max_topic_idx = None
max_img = None

with open("C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/Sketchformer/prep_data/quickdraw/list_quickdraw.txt") as file:
    quickdraw_classes = file.readlines()

quickdraw_classes = [c.replace("\n", "").strip() for c in quickdraw_classes]

quickdraw_dict = {}
for idx, cls in enumerate(quickdraw_classes + context_list):
    quickdraw_dict[cls] = idx


def find_unrelated(sketch_list, curr_context):
    global topic_word
    global porter,topic_img_mapping
    global max_topic_idx, max_img

    max_topic_prob = -1
    max_topic_idx = -1
    max_topic_subset = None
    for subset in itertools.combinations(sketch_list, len(sketch_list)-1):
        indices = []
        for cls in list(subset) + [curr_context]:
            indices.append(quickdraw_dict[cls])

        sub_mtx = topic_word[:, indices]
        # print(sub_mtx.shape)
        # print(sub_mtx)

        topic_prob = np.max(np.prod(sub_mtx, axis=1))
        topic_idx = np.argmax(np.prod(sub_mtx, axis=1))
        if (max_topic_prob < topic_prob):
            max_topic_prob = topic_prob
            max_topic_idx = topic_idx
            max_topic_subset = subset

    stemmed_subset = [porter.stem(obj) for obj in max_topic_subset]
    # print("max_topic_subset ", max_topic_subset)
    max_doc, max_img, max_ctr = None, None, -1
    for doc, img_pth in topic_img_mapping[str(max_topic_idx)]:
        ctr = 0
        for obj in stemmed_subset:
            if obj in doc:
                ctr += 1
        if ctr > max_ctr:
            max_doc = doc
            max_img = img_pth
            max_ctr = ctr

    # print("Doc:", max_doc)
    # print("Image:", str(max_topic_idx) + "/" + max_img)

    """
    rand_docs = random.sample(topic_img_mapping[str(max_topic_idx)], 3)

    for ctr, doc in enumerate(rand_docs):
        print(f"{ctr+1}) Doc:", doc[0])
        print(f"{ctr+1}) Image:", str(max_topic_idx) + "/" + doc[1])
    """

    for sketch in sketch_list:
        if sketch not in max_topic_subset:
            return sketch, max_topic_prob, max_topic_idx, max_img, max_doc
    return None, None

