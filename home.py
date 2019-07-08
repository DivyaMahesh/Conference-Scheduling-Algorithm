import numpy as np
import pandas as pd
import csv
import sys
from datetime import timedelta
import re


df = pd.read_csv('test.csv')  # reading the test input
df = df.sort_values('time', ascending=False)  # sorting the time in descending order; from highest to lowest
print('initial')
print(df)

# Creating two Tracks with default key-value parameters
output_track_1 = {16.00: ['Poster Session and Networking Event', 60], 10.45: ['Break', 15], 12.00: ['Lunch Break', 60], '14.30': ['Break', 15]}
output_track_2 = {16.00: ['Poster Session and Networking Event', 60], 10.45: ['Break', 15], 12.00: ['Lunch Break', 60], '14.30': ['Break', 15]}

# Initialising the track hour
track1_hour = 0

# Initialising track 1 - available time split up
track1_am1 = 165
track1_am2 = 60
track1_pm1 = 90
track1_pm2 = 75

# Initialising the flags- 0 or 1
track1_filled_am1 = 0
track1_filled_am2 = 0
track1_filled_pm1 = 0
track1_filled_pm2 = 0

# Initialising the default start time after every break
track1_start_am1 = 8.00
track1_start_am2 = 11.00
track1_start_pm1 = 13.00
track1_start_pm2 = 14.45

track2_hour = 0

# Initialising track 2 - available time split up
track2_am1 = 165
track2_am2 = 60
track2_pm1 = 90
track2_pm2 = 75

# Initialising the flags- 0 or 1
track2_filled_am1 = 0
track2_filled_am2 = 0
track2_filled_pm1 = 0
track2_filled_pm2 = 0

# Initialising the default start time after every break
track2_start_am1 = 8.00
track2_start_am2 = 11.00
track2_start_pm1 = 13.00
track2_start_pm2 = 14.45


def time_add(a, b):
    global c, d
    c = a+b
    c_dec = round(float(str(c-int(c))[1:]), 2)
    if c_dec > 0.59:
        c = str(int(c)+1)
        c_dec = round(c_dec - 0.6,2)
        c_dec = str(int(100*c_dec))
        d = c+'.'+c_dec
        d = float(d)
        return d
    return round(c, 2)


# Looping through the Input Event Duration and check if any value matches with the available time(combines) in track 1 and track 2
for index, row in df.iterrows():
    item_dropped = 0
    if row['time'] > track1_am1:
        print('greater than track1_am1_got_hit-- not valid')
    if row['time'] == track1_am1 and track1_filled_am1 != 1:
        output_track_1[track1_start_am1] = [row['topic_name'], row['time']]
        track1_filled_am1 = 1
        item_dropped = 1
        print('equal track1_am1_got_hit')
    if row['time'] == track1_am2 and track1_filled_am2 != 1:
        output_track_1[track1_start_am2] = [row['topic_name'], row['time']]
        track1_filled_am2 = 1
        item_dropped = 1
        print('equal track1_am2_got_hit')
    if row['time'] == track1_pm1 and track1_filled_pm1 != 1:
        output_track_1[track1_start_pm1] = [row['topic_name'], row['time']]
        track1_filled_pm1 = 1
        item_dropped = 1
        print('equal track1_pm1_got_hit')
    if row['time'] == track1_pm2 and track1_filled_pm2 != 1:
        output_track_1[track1_start_pm2] = [row['topic_name'], row['time']]
        track1_filled_pm2 = 1
        item_dropped = 1
        print('equal track1_pm2_got_hit')
    if item_dropped == 1:
        df.drop(index, axis=0, inplace=True)
print('after first check:')
print(df)
df = df.sort_values('time', ascending=False)
print(output_track_1)

for index, row in df.iterrows():
    item_dropped = 0
    if row['time'] > track2_am1:
        print('greater than track2_am1_got_hit-- not valid')
    if row['time'] == track2_am1 and track2_filled_am1 != 1:
        output_track_2[track2_start_am1] = [row['topic_name'], row['time']]
        item_dropped = 1
        track2_filled_am1 = 1
        print('equal track2_am1_got_hit')
    if row['time'] == track2_am2 and track2_filled_am2 != 1:
        output_track_2[track2_start_am2] = [row['topic_name'], row['time']]
        item_dropped = 1
        track2_filled_am2 = 1
        print('equal track2_am2_got_hit')
    if row['time'] == track2_pm1 and track2_filled_pm1 != 1:
        output_track_2[track2_start_pm1] = [row['topic_name'], row['time']]
        item_dropped = 1
        track2_filled_pm1 = 1
        print('equal track2_pm1_got_hit')
    if row['time'] == track2_pm2 and track2_filled_pm2 != 1:
        output_track_2[track2_start_pm2] = [row['topic_name'], row['time']]
        item_dropped = 1
        track2_filled_pm2 = 1
        print('equal track2_pm2_got_hit')
    if item_dropped == 1:
        df.drop(index, axis=0, inplace=True)

print('after second check:')
print(df)
df = df.sort_values('time', ascending=False)
print(output_track_2)

# The remaining duration values in the input can be filled in an orderly fashion across Track 1 and Track 2

for index, row in df.iterrows():
    if row['time'] <= track1_am1 and track1_filled_am1 != 1:
        track1_am1 -= row['time']
        track1_am1_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track1_hour = float(re.sub("[:]", ".", track1_am1_time_convert))
        output_track_1[track1_start_am1] = [row['topic_name'], row['time']]
        print(track1_hour, ':track1_am1_hit and NOT full')
        track1_start_am1 = time_add(track1_start_am1, track1_hour)
        print('track1 start am1=', track1_start_am1)
        df.drop(index, axis=0, inplace=True)
        if track1_am1 < 5:
            track1_filled_am1 = 1
            print('track1_am1_hit and full')
        continue

    if row['time'] <= track1_am2 and track1_filled_am2 != 1:
        track1_am2 -= row['time']
        track1_am2_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track1_hour = float(re.sub("[:]", ".", track1_am2_time_convert))
        output_track_1[track1_start_am2] = [row['topic_name'], row['time']]
        print(track1_hour, ':track1_am2_hit and NOT full')
        track1_start_am2 = time_add(track1_start_am2, track1_hour)
        print('track1 start am2=', track1_start_am2)
        df.drop(index, axis=0, inplace=True)
        if track1_am2 < 5:
            track1_filled_am2 = 1
            print('track1_am2_hit and full')
        continue

    if row['time'] <= track1_pm1 and track1_filled_pm1 != 1:
        track1_pm1 -= row['time']
        track1_pm1_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track1_hour = float(re.sub("[:]", ".", track1_pm1_time_convert))
        output_track_1[track1_start_pm1] = [row['topic_name'], row['time']]
        print(track1_hour, ':track1_pm1_hit and NOT full')
        track1_start_pm1 = time_add(track1_start_pm1, track1_hour)
        print('track1 start pm1=', track1_start_pm1)
        df.drop(index, axis=0, inplace=True)
        if track1_pm1 < 5:
            track1_filled_pm1 = 1
            print('track1_pm1_hit and full')
        continue

    if row['time'] < track1_pm2 and track1_filled_pm2 != 1:
        track1_pm2 -= row['time']
        track1_pm2_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track1_hour = float(re.sub("[:]", ".", track1_pm2_time_convert))
        output_track_1[track1_start_pm2] = [row['topic_name'], row['time']]
        print(track1_hour, ':track1_pm2_hit and NOT full')
        track1_start_pm2 = time_add(track1_start_pm2, track1_hour)
        print('track1 start pm2=', track1_start_pm2)
        df.drop(index, axis=0, inplace=True)
        if track1_pm2 < 5:
            track1_filled_pm2 = 1
            print('track1_pm2_hit and full')
            continue

print('after third check:')
print(df)
df = df.sort_values('time', ascending=False)
print(output_track_1)

for index, row in df.iterrows():
    # item_dropped == 0
    # If the input is still available to be filled in the conference schedule it makes use of the track 2 - parallel event
    if row['time'] <= track2_am1 and track2_filled_am1 != 1:
        track2_am1 -= row['time']
        track2_am1_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track2_hour = float(re.sub("[:]", ".", track2_am1_time_convert))
        output_track_2[track2_start_am1] = [row['topic_name'], row['time']]
        print(track2_hour, ':track2_am1_hit and NOT full')
        track2_start_am1 = time_add(track2_start_am1, track2_hour)
        print('track2 start am1=', track2_start_am1)
        df.drop(index, axis=0, inplace=True)
        if track2_am1 < 5:
            track2_filled_am1 = 1
            print('track2_am1_hit and full')
        continue

    if row['time'] <= track2_am2 and track2_filled_am2 != 1:
        track2_am2 -= row['time']
        track2_am2_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track2_hour = float(re.sub("[:]", ".", track2_am2_time_convert))
        output_track_2[track2_start_am2] = [row['topic_name'], row['time']]
        print(track2_hour, ':track2_am2_hit and NOT full')
        track2_start_am2 = time_add(track2_start_am2, track2_hour)
        print('track2 start am2=', track2_start_am2)
        df.drop(index, axis=0, inplace=True)
        if track2_am2 < 5:
            track2_filled_am2 = 1
            print('track2_am2_hit and full')
        continue

    if row['time'] <= track2_pm1 and track2_filled_pm1 != 1:
        track2_pm1 -= row['time']
        track2_pm1_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track2_hour = float(re.sub("[:]", ".", track2_pm1_time_convert))
        output_track_2[track2_start_pm1] = [row['topic_name'], row['time']]
        print(track2_hour, ':track2_pm1_hit and NOT full')
        track2_start_pm1 = time_add(track2_start_pm1, track2_hour)
        print('track2 start pm1=', track2_start_pm1)
        df.drop(index, axis=0, inplace=True)
        if track2_pm1 < 5:
            track2_filled_pm1 = 1
            print('track2_pm1_hit and full')
        continue

    if row['time'] <= track2_pm2 and track2_filled_pm2 != 1:
        track2_pm2 -= row['time']
        track2_pm2_time_convert = str(timedelta(minutes=row['time']))[:-3]
        track2_hour = float(re.sub("[:]", ".", track2_pm2_time_convert))
        output_track_2[track2_start_pm2] = [row['topic_name'], row['time']]
        print(track2_hour, ':track2_pm2_hit and NOT full')
        track2_start_pm2 = time_add(track2_start_pm2, track2_hour)
        print('track2 start pm2=', track2_start_pm2)
        df.drop(index, axis=0, inplace=True)
        if track2_pm2 < 5:
            track2_filled_pm2 = 1
            print('track2_pm2_hit and full')
        continue

print('after fourth check:')
print(df)
# df = df.sort_values('time', ascending=False)
print(output_track_2)

print('final outputs')
print(output_track_1)
print(output_track_2)

pd.set_option('display.max_colwidth', -1)
df_track1_op = pd.DataFrame(output_track_1.items(), columns=list('ab'))
df_track1_op["a"] = pd.to_numeric(df_track1_op["a"])
df_track1_op_sorted = df_track1_op.sort_values('a')
df_track1_op_sorted.reset_index(drop=True, inplace=True)
print(df_track1_op_sorted)

df_track2_op = pd.DataFrame(output_track_2.items(), columns=list('ab'))
df_track2_op["a"] = pd.to_numeric(df_track2_op["a"])
df_track2_op_sorted = df_track2_op.sort_values('a')
df_track2_op_sorted.reset_index(drop=True, inplace=True)
print(df_track2_op_sorted)
