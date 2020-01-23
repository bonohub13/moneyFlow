#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import errno
import os

class MoneyFlow:
    def __init__(self, filepath=None, sheetname: str=None):
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if filepath != None:
            try:
                if '.csv' in filepath:
                    self.file = pd.read_csv(filepath, usecols=self.months)
                elif '.xlsx' in filepath:
                    self.file = pd.read_excel(filepath, sheetname, usecols=self.months)
            except FileNotFoundError:
                self.file = pd.DataFrame({})
                for month in self.months:
                    self.file[month] = [0 for i in range(32)]
        else:
            raise FileNotFoundError(errno.ENOENT, 
                                    os.strerror(errno.ENOENT), 
                                    filepath)
        self.filepath = filepath
        self.write()

    def add_data(self, date: int, used_money, month='Jan'):
        data = self.file[month]
        data[date] = used_money
        self.write()

    def write(self):
        for month in self.months:
            data = self.file[month]
            data[31] = sum(data[:30])
        self.file.to_csv(self.filepath, mode='w', columns=self.months)

    def __test__(self):
        print(self.file)

if __name__ == '__main__':
    money_flow = MoneyFlow(filepath='datas/', sheetname=None)
    month = input('input first 3 letters of month[ex. Jan]: ')
    date = int(input('date of input data: '))
    used_money = int(input('amount of money used: '))
    money_flow.add_data(date-1, used_money, month=month)
    print(money_flow.file)
