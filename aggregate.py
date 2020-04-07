#!/usr/bin/env python3

import csv

csvfile = open("COVID19_Fallzahlen_CH_total.csv")
csvreader= csv.reader(csvfile)
csvfile.readline()
date_counter = {}
dates = []
numbers_by_date_canton = []
for row in csvreader:
    date, canton = row[0], row[2]
    
    data_vec = [(0 if len(row[i]) == 0 else int(row[i])) for i in range(3, 10)]
    if len(dates) == 0 or dates[-1] != date:
        new_today = {}
        if len(dates) > 0: 
            yesterday = numbers_by_date_canton[-1]
            yesterday_canton = yesterday.get(canton, [0] * 7)
            new_today.update(yesterday)
        else:
            yesterday_canton = [0] * 7
        numbers_by_date_canton.append(new_today)
        dates.append(date)
    else:
        if len(numbers_by_date_canton) > 1:
            yesterday_canton = numbers_by_date_canton[-2].get(canton, [0]*7)
        else:
            yesterday_canton = [0] * 7

    for i in range(7):
        # 0 means no data for today yet, use yesterday's
        if data_vec[i] == 0:
            data_vec[i] = yesterday_canton[i]
    numbers_by_date_canton[-1][canton] = data_vec
        
    date_cantons = date_counter.get(date, set())
    date_cantons.add(canton)
    date_counter[date] = date_cantons

prev_sum = [0] * 7
date_idx = 0
for numbers_by_canton in numbers_by_date_canton:
    date = dates[date_idx]
    date_idx += 1
    sum = [0] * 7
    for canton, data_vec in numbers_by_canton.items():
        for i in range(7):
            sum[i] += data_vec[i]
    print(f"cantons: {len(numbers_by_canton)}")
    tested, confirmed, hospitalized, icu, vent, released, dead = sum[0], sum[1], sum[2], sum[3], sum[4], sum[5], sum[6], 
    reported_cantons = len(date_counter[date])
    inc_confirmed = confirmed - prev_sum[1]
    in_progress = confirmed - released
    print(f"{reported_cantons} {date}: in_progress: {in_progress}, confirmed: (+{inc_confirmed}, {confirmed}), cured: {released}, dead: {dead}, hospitalized: {hospitalized}, icu: {icu}, vent: {vent}")
    prev_sum = sum
