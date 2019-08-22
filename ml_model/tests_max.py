import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 150)
pd.set_option('display.max_columns', 20)

df = pd.read_csv(
    f'/Users/maxvonborch/Documents/Master_Thesis/Good-Bad_Dialogue/Data/Cleaned Data/test_django.csv', sep=";",
    header=None)

# df = df.drop([0], axis=1)

df = df.T.set_index([0, 1]).unstack()
df.index = df.index.map(int)
df.sort_index(inplace=True)

df.columns = df.columns.get_level_values(1)

# new_header = df.iloc[0] #grab the first row for the header
# df = df[1:] #take the data less the header row
# df.columns = new_header #set the header row as the df header
# df = df.drop(df.index[0])

# df = df.MultiIndex.droplevel(0)
# df.rename(columns={"1": "Label"})

# number of words per conversation
words = []
for i in range(0, len(df["TimeTo"])):
    row = [float(j) for j in df["TimeTo"].iloc[i]]
    len_row = len(row)
    word = np.isnan(row).argmax()
    if word == 0:
        words.append(len_row)
    else:
        words.append(word)


# get durations of conversations

# end = df["TimeTo"]
# start = df["TimeFrom"]
#
#
# def duration(start, end):
#     durations = []
#     for i in range(0, len(end)):
#         ends = [float(j) for j in end.iloc[i]]
#         starts = float(start.iloc[i].iloc[0])
#         durations.append(max(ends) - starts)
#     print(durations)




# end = [float(j) for j in end.iloc[i]]
# duration(start,end)

# gives you segment size
def words_per_segment(dataframe):
    '''Pass in dataframe containing only "speaker" colums. Dataframe should have n rows
      (where n is # of conversations in dataset) and m columns (where m is # of words in longest conversation in dataset)'''
    segment_size = []
    for i in range(0, len(dataframe)):
        conversation = dataframe.iloc[i]
        init = conversation.iloc[0]
        counter = 0
        segments = []
        if np.isnan(dataframe.iloc[i].values).argmax() == 0:
            length = len(dataframe.columns)
        else:
            length = np.isnan(dataframe.iloc[i].values).argmax() + 1
        for j in range(0, length):
            if j == length - 1:
                segments.append(counter)
            elif conversation.iloc[j] == init:
                counter = counter + 1
            else:
                if counter > 0:
                    segments.append(counter)
                    counter = 1
                init = conversation.iloc[j]
        segment_size.append(segments)
    return segment_size


t = df["Speaker"].astype(float)
segment_size = words_per_segment(t)

# starting and ending words
start_ends = []
for conversation in segment_size:
    start_end = []
    init = 1
    for segment in conversation:
        start_end.append([init, segment + init - 1])
        init = init + segment
    start_ends.append(start_end)

# starting and ending times
start_end_times = []
counter = 0
for conversation in start_ends:
    start_end_time = []
    for segment in conversation:
        start_end_time.append(
            [float(df["TimeFrom"].iloc[counter].iloc[segment[0] - 1]),
             float(df["TimeTo"].iloc[counter].iloc[segment[1] - 1])])
    counter = counter + 1
    start_end_times.append(start_end_time)

# calculate segment duration
durations = []
for i in range(0, len(start_end_times)):
    duration = []
    for j in range(0, len(start_end_times[i])):
        duration.append(start_end_times[i][j][1] - start_end_times[i][j][0])
    durations.append(duration)

# calculate segment speed
speeds = []
for i in range(0, len(start_end_times)):
    speed = []
    for j in range(0, len(start_end_times[i])):
        speed.append(segment_size[i][j] / durations[i][j])
    speeds.append(speed)

# get speaker of segment
speakers = []
counter = 0
for i in range(0, len(df)):
    speaker = []
    for j in start_ends[i]:
        speaker.append(df["Speaker"].iloc[counter].iloc[j[0] - 1])
    counter = counter + 1
    speakers.append(speaker)

# get gaps of segment
gaps = []
counter = 0
for i in range(0, len(df)):
    gap = []
    for j in range(1, len(start_ends[i])):
        gap.append(float(df["Gap between speakers"].iloc[counter].iloc[start_ends[i][j][0] - 1]))
    counter = counter + 1
    gaps.append(gap)

new_features = pd.DataFrame()

analysis = pd.DataFrame()
analysis["Segment Size"] = segment_size
analysis["Speed"] = speeds
analysis["Speakers"] = speakers
analysis["Gaps"] = gaps

#########
# calculate average gap size
average_gaps = []
for i in gaps:
    if len(i) > 0:
        average_gaps.append(sum(i) / len(i))
    else:
        average_gaps.append(np.nan)




# calculate average segment size
average_segments = []
for i in segment_size:
    average_segments.append(sum(i) / len(i))




# calculate # of interruptions

x = 0.1
interruptions = []
for i in gaps:
    interruption = []
    if len(i) > 0:
        interruptions.append(sum(j < x for j in i) / len(i))
    else:
        interruptions.append(np.nan)





# clean duration (duration-length of all gaps ooooorrr: sum of all gap lengths)
clean_duration = [sum(i) for i in durations]

# number of words per conversation
words = []
for i in range(0, len(df["TimeTo"])):
    row = [float(j) for j in df["TimeTo"].iloc[i]]
    len_row = len(row)
    word = np.isnan(row).argmax()
    if word == 0:
        words.append(len_row)
    else:
        words.append(word)


# calculate speed

words_second = [words[i]/clean_duration[i] for i in range(len(df))]



###########################################################################
# final dataframe

features = pd.DataFrame()
features["Words/Second"] = words_second
features["Average Gaps"] = average_gaps
features["Average Segment Size"] = average_segments
features["% of Interruptions"] = interruptions
print(features)
