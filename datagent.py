import random
import pandas as pd


class DataGen:
    dayOfWeekChoice = ['MON', "TUE", 'WED', 'THU', "FRI"]
    workTimeChoice = [1, 2, 3, 4, 5, 6, 7, 8]
    checkInTimeChoice = ["8:00", "8:30", "9:00",
                         "9:30", "10:00", "10:30", "11:00", "11:30", "12:00"]

    def __init__(self, n_data=2000, n_employee=50):
        self.row = n_data
        self.n_employee = n_employee
        self.employeeID = []
        self.dayOfWeek = []
        self.checkInTime = []
        self.workTime = []

    def genData(self):
        for i in range(self.row//self.n_employee):
            for id in range(self.n_employee):
                self.employeeID += [id]
                self.dayOfWeek += [random.choice(self.dayOfWeekChoice)]
                self.checkInTime += [random.choice(self.workTimeChoice)]
                self.workTime += [random.choice(self.checkInTimeChoice)]

    def saveCSV(self, filename):
        variables = [self.employeeID,
                     self.dayOfWeek,
                     self.checkInTime,
                     self.workTime]
        df = pd.DataFrame(variables).transpose()
        df.columns = ["ID", "day of week",
                      "check in time", "work time"]
        df.to_csv(filename, index=False)


if __name__ == '__main__':
    dg = DataGen()
    dg.genData()
    dg.saveCSV("employeedata.csv")
