import numpy as np
import matplotlib.pyplot as plt
import json
import datetime
import iso8601
import calendar
from collections import defaultdict
import util


path_to_data = 'Takeout_2/YouTube und YouTube Music/Verlauf/Wiedergabeverlauf.json'

f = open(path_to_data)

data = json.load(f)


file = open('tags.csv', 'w')


# Loop through entries in json file
start_index_for_loop_through_data = int(len(data) * 0)
end_index_for_loop_through_data = int(len(data)* 1)

for i in range(start_index_for_loop_through_data, end_index_for_loop_through_data):
    entry = data[i]

    # skip music videos
    if entry['header'] != 'YouTube':
        continue
    

    if 'titleUrl' not in entry:
        print('no url')
        continue

    tags_as_list = (util.request_tags_via_api(entry['titleUrl']))
    
    print(i/float(len(data)))

    if tags_as_list == []:
        print('empty')

    for tag in tags_as_list:
        file.write(tag + ',')
    
    file.write('\n')


