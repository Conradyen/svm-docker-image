# from cassandra.cluster import Cluster
from timeParser import timeParser
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
# for testing
import csv


class DataPreprocessor:
    timeChoice = ["8:00", "8:30", "9:00",
                  "9:30", "10:00", "10:30", "11:00",
                  "11:30", "12:00", "12:30", "13:00",
                  "13:30", "14:00", "14:30", "15:00",
                  "15:30", "16:00", "16:30",
                  "17:00", "17:30", "18:00",
                  "18:30", "19:00", "19:30", '20:00']

    def __init__(self):
        self.dummy = 0
        # self.cluster = Cluster(['0.0.0.0'], port=9042)
        # self.session = self.cluster.connect(
        #     'employee', wait_for_all_pools=True)
        # self.session.execute('USE employee')

    def getData(self, onehot=True):
        self._countByGroup()
        dayOfWeek = []
        time = []
        count = []

        for r in self.group_count.keys():
            # print(r)
            sp = r.split('#')
            dayOfWeek += [sp[0]]
            time += [sp[1]]
            count += [self.group_count[r]]

        variables = [dayOfWeek,
                     time,
                     count]
        df = pd.DataFrame(variables).transpose()
        df.columns = ["dayOfWeek", "time", "count"]
        print(df.head())
        if onehot:
            # times_encoder = OneHotEncoder().fit(
            #     df['time'].unique().reshape(-1, 1))
            # print(df['time'])
            # transformed_time = times_encoder.transform(
            #     df['time'].to_numpy().reshape(-1, 1))
            # print(transformed_time)
            times_df = pd.get_dummies(df.time, prefix='time')

            # dayOfWeek_encoder = OneHotEncoder().fit(
            #     df['dayOfWeek'].to_numpy().reshape(-1, 1))
            # transformed_dayOfWeek = dayOfWeek_encoder.transform(
            #     df['dayOfWeek'].to_numpy().reshape(-1, 1))
            dayOfWeek_df = pd.get_dummies(df.dayOfWeek, prefix='dayOfWeek')
            df = pd.concat([times_df, dayOfWeek_df, df], axis=1).drop(
                ['dayOfWeek', 'time'], axis=1)
        return df

    def _countByGroup(self):
        self.group_count = {}
        # rows = self.session.execute('SELECT * FROM employee')
        with open('employeedata.csv', newline='\n') as csvfile:
            rows = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(rows)
            for row in rows:
                for t in self.timeChoice:
                    # key = row.DAY_OF_WEEK + ':' + t
                    key = row[4] + '#' + t
                    # outTime = timeParser(row.CHECKIN_DATETIME) + \
                    #     timeParser(row.DURATION)
                    outTime = timeParser(row[5]) + \
                        timeParser(row[6])
                    if outTime > timeParser(t):
                        if key not in self.group_count.keys():
                            self.group_count[key] = 1
                        else:
                            self.group_count[key] += 1
