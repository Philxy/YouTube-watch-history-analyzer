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


num_videos_total = 0
num_videos_per_month = np.zeros(12, dtype=int)
num_videos_per_month_and_year = {'2020': np.zeros(12, dtype=int)}
num_videos_per_hour = np.zeros(24, dtype=int)

file = open('request_results.csv', 'w')

# Loop through entries in json file
for entry in data:

    # skip music videos
    if entry['header'] != 'YouTube':
        continue

    tags_as_list = (util.request_tags_via_api(entry['titleUrl']))
    
    for tag in tags_as_list:
        file.write

    file.write(str(util.request_tags_via_api(entry['titleUrl'])))

    time_obj = iso8601.parse_date(entry['time'])

    if not time_obj.year in num_videos_per_month_and_year:
        num_videos_per_month_and_year[time_obj.year] = np.zeros(12, dtype=int)

    num_videos_total += 1
    num_videos_per_month_and_year[time_obj.year][time_obj.month-1] += 1
    num_videos_per_month[time_obj.month-1] += 1
    num_videos_per_hour[time_obj.hour-1] += 1


month_names = [calendar.month_abbr[i] for i in range(1, 13)]


for year in num_videos_per_month_and_year:
    plt.plot(month_names, num_videos_per_month_and_year[year], label=year)

plt.plot()

print('Total number of YT videos: ' + str(num_videos_total))

# plot number of videos over months
plt.ylabel('Number of videos')
plt.plot(month_names, num_videos_per_month, label='all time')
plt.legend()
plt.savefig('Figures/num_vids_over_month.png')
plt.clf()

# plot number of videos over hour
plt.plot(num_videos_per_hour)
plt.xlabel('Hour')
plt.ylabel('Number of videos')
plt.savefig('Figures/num_vids_over_hour.png')
