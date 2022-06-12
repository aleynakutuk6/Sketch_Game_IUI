import os
import json
import random
from tqdm import tqdm
main_path = 'C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/TopicModeling/'

f = open(main_path + 'data/image_ids.json')
img_data = json.load(f)
f.close()

f = open(main_path + 'data/topics_docs.json')
docs_data = json.load(f)
f.close()

retry_cnt = 500
selected_docs = []
topic_list = []
for tidx, topic in enumerate(docs_data.keys()):
    print("Processing topic:", tidx+1, "/", len(docs_data.keys()), "| Out of", len(docs_data[topic]), "documents.")
    topic_list.append(topic)
    ctr = min(10000, len(docs_data[topic]) // 2)
    failed = 0
    selected_docs_per_topic = []
    while ctr > 0:
        doc = random.choice(docs_data[topic])
        image_id, dataset_name = img_data[doc]
        if "coco" in dataset_name or "flickr30k" in dataset_name:
            # print("Here!")
            if doc not in selected_docs_per_topic:
                selected_docs_per_topic.append(doc)
                failed = 0
                ctr -= 1
            else:
                failed += 1
                if failed == retry_cnt:
                    ctr = 0
        else:
            failed += 1
            if failed == retry_cnt:
                ctr = 0

    selected_docs.append(selected_docs_per_topic)

# scp akutuk21@login.kuacc.ku.edu.tr:/datasets/COCO/train2017/{numzeros}{id}.jpg {topic_list}/

f = open(main_path + 'data/image_copier_script.sh', "w")

for topic, docs in zip(topic_list, selected_docs):
    coco_str = "cp /datasets/COCO/train2017/"
    flickr_str = "cp /datasets/flickr30k/flickr30k-images/"
    for doc in docs:
        str_to_write = ""
        image_id, dataset_name = img_data[doc]
        if "coco" in dataset_name:
           str_to_write = coco_str + "0"*(12-len(image_id)) + image_id + ".jpg " + topic + "/"
        elif "flickr30k" in dataset_name:
            str_to_write = flickr_str + image_id + ".jpg " + topic + "/"
        f.write(str_to_write + "\n")

f.close()

result_dict = {}

for tidx, topic in enumerate(docs_data.keys()):
    result_dict[topic] = []
    for doc in selected_docs[tidx]:
        image_id, dataset_name = img_data[doc]
        if "coco" in dataset_name:
            str_to_write = "0" * (12 - len(image_id)) + image_id + ".jpg"
        elif "flickr30k" in dataset_name:
            str_to_write = image_id + ".jpg"
        result_dict[topic].append([doc, str_to_write])


with open(main_path + "data/topic_img_mapping.json", "w") as outfile:
    json.dump(result_dict, outfile)





