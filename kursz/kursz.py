# -*- coding: cp1251 -*-
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # для отрисовки 3D проекции
matplotlib.rc("font", size=8) # для увеличения шрифта подписей графиков
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import statistics
from tkinter import *

import tkinter as tk
from tkinter import ttk

class DashboardApp:
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Аналитика по Yes Online")
        '''
        # Create a Frame to hold the dashboard widgets
        self.dashboard_frame = ttk.Frame(parent)
        self.dashboard_frame.grid(sticky="nsew")
        '''
        #canvas0 = Canvas(parent, width = 500, height = 500, bg = 'white', bd = 0, borderwidth = 0, highlightthickness = 0) 
        #canvas0.grid(row=0, column=1, pady=0)
        # Create and place widgets on the dashboard using the Grid geometry manager
        self.create_widgets()
        

    def create_widgets(self):
        groups = pd.read_csv('groups.csv')
        lessons = pd.read_csv('lessons.csv')
        attendances = pd.read_csv('attendances.csv')
        
        num1 = 0 
        num2 = 0
        
        bd2 = pd.merge(lessons, attendances, left_on=lessons['_id'], right_on=attendances['lessonId'], how='inner')
        del bd2['key_0']
        
        bd3 = pd.merge(bd2, groups, left_on=bd2['groupId'], right_on=groups['_id'], how='inner')
        del bd3['key_0']
        
        bd_filter = bd3[bd3['filial'] == '63c63702397ca6783eb57fa2']
        
        ##################################
        ##################################
        ##################################

        bd_month = pd.DataFrame({'date': bd_filter['date'].astype("datetime64[ns]")})
        bd_month = pd.DataFrame({'date': bd_month['date'], 'month': bd_month['date'].dt.month})
        bd_month.groupby( bd_month['month'])['month']
        bd_count = pd.DataFrame({'date': bd_month['date'], 'year': bd_month['date'].dt.year, 'month': bd_month['date'].dt.month})
        bd_count4 = pd.DataFrame(columns=['date', 'count'])
        i = 0
        for year in range(2021, 2024):
            for month in range(1, 13):
                bd_count2 = bd_count[bd_count['year'] == year]
                bd_count3 = bd_count2[bd_count2['month'] == month]
                count = bd_count3['date'].count()
                bd_count4.loc[i, 'date'] = str(year) + '-' + str(month)
                bd_count4.loc[i, 'count'] = count
                i = i + 1
        bd_count5 = bd_count4[bd_count4['count'] > 0]
        bd_count6 = bd_count5[1:23]
        counter = 0
        for j in range(len(bd_count6)):
            counter = counter + bd_count6['count'].iloc[j]
        num1 = counter/len(bd_count6)
        num1 = round(num1, 1)
        def addlabels(x,y):
            for i in range(len(x)):
                plt.text(i,y[i],y[i])

        fig = plt.figure(figsize=(6, 3)) # создаем картинку
        ax = plt.axes()
        #featureOne = 'Месяц'
        #featureTwo = 'Количество уроков'
        featureOne = ''
        featureTwo = ''
        # помещаем точки на график
        ax.scatter(bd_count6['date'], bd_count6['count'], s=10)
        plt.plot(bd_count6['date'], bd_count6['count'], '-')
        mean1 = round(statistics.mean(bd_count6['count']), 1)
        median1 = statistics.median(bd_count6['count'])
        plt.axhline (y=mean1, color='red', linestyle='--', label = 'Среднее')
        plt.axhline (y=median1, color='green', linestyle='--', label = 'Медиана')
        
        plt.legend()
        
        # отображаем картинку
        ax.set_xlabel(featureOne)
        ax.set_ylabel(featureTwo)
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.3)
        #addlabels(bd_count4['date'], bd_count4['count'])
        plt.grid()
        #plt.show()
        canvas1 = FigureCanvasTkAgg(fig, master = parent)
        canvas1.get_tk_widget().grid(row=5, column=3)
        canvas1.draw()
        
        ##################################
        ##################################
        ##################################
        

        students = pd.DataFrame(columns=['_id'])
        for i, x in enumerate(bd_filter['studentId']):
            students.loc[i, '_id'] = x
        students2 = students.drop_duplicates(subset=['_id'])

        students3 = pd.DataFrame(columns=['studentId', 'date', 'count'])
        bd_filter_date = pd.DataFrame({'date': bd_filter['date'].astype("datetime64[ns]")})
        bd_filter_date1 = pd.DataFrame({'lessonId': bd_filter['lessonId'], 'studentId': bd_filter['studentId'], 'date': bd_filter_date['date'], 'year': bd_filter_date['date'].dt.year, 'month': bd_filter_date['date'].dt.month})
        bd_true_date = pd.DataFrame({'date': bd_count6['date'] })
        
        import re
        i = 0
        for l, z in enumerate(students2['_id']):
            for t, d in enumerate(bd_true_date['date']):
                    date = re.split("-", str(d))
                    year = date[0]
                    month = date[1]
                    students_count = bd_filter_date1[bd_filter_date1['year'] == int(year)]
                    students_count = students_count[students_count['month'] == int(month)]
                    students_count = students_count[students_count['studentId'] == z]
                    count = students_count['lessonId'].count()
                    students3.loc[i, 'studentId'] = z
                    students3.loc[i, 'date'] = str(year) + '-' + str(month)
                    students3.loc[i, 'count'] = count
                    students3.loc[i, 'year'] = year
                    students3.loc[i, 'month'] = month
                    i = i + 1
        students4 = students3[students3['count'] > 0]

        i = 0
        students7 = pd.DataFrame(columns=['students_in_month', 'date', 'count'])
        count = 0
        for t, d in enumerate(bd_true_date['date']):
            date = re.split("-", str(d))
            year = date[0]
            month = date[1]
            students5 = students4[students4['year'] == year]
            students6 = students5[students5['month'] == month]
            students_in_month = students6['count'].count()
            students7.loc[i, 'date'] = str(year) + '-' + str(month)
            students7.loc[i, 'students_in_month'] = students_in_month

            for j, c in enumerate(students6['count']):
                count = count + c

            students7.loc[i, 'count'] = count
            i = i + 1

        i = 0
        students8 = pd.DataFrame(columns=['date', 'count'])

        for i, d in enumerate(students7['date']):
            students8.loc[i, 'date'] = d
            count = students7.loc[i, 'count']/students7.loc[i, 'students_in_month']
            students8.loc[i, 'count'] = round(count/11, 1)

        students_ids = pd.DataFrame({'_id': students4['studentId']})
        students_ids = students_ids.drop_duplicates(subset=['_id'])

        studentss = pd.DataFrame(columns=['studentId', 'count'])
        i = 0
        count = 0
        for l, z in enumerate(students_ids['_id']):
                    bd_num = students4[students4['studentId'] == z]
                    for m, c in enumerate(bd_num['count']):
                        count = count + c
                    leng = bd_num['date'].count()
                    count = int(count)/int(leng)
                    studentss.loc[i, 'studentId'] = z
                    studentss.loc[i, 'count'] = round(count, 1)
                    i = i + 1
        count = 0
        for m, c in enumerate(studentss['count']):
                        count = count + c
        #num2 = round(count/len(studentss), 1)

        fig = plt.figure(figsize=(6, 3)) # создаем картинку
        ax = plt.axes()
        #featureOne = 'Месяц'
        #featureTwo = 'Среднее кол-во уроков на 1 студента'
        featureOne = ''
        featureTwo = ''
        # помещаем точки на график
        ax.scatter(students8['date'], students8['count'], s=10)
        plt.plot(students8['date'], students8['count'], '-')
        
        mean2 = round(statistics.mean(students8['count']), 1)
        median2 = statistics.median(students8['count'])
        num2 = mean2
        plt.axhline (y=mean2, color='red', linestyle='--', label = 'Среднее')
        plt.axhline (y=median2, color='green', linestyle='--', label = 'Медиана')
        plt.legend()
        
        # отображаем картинку
        ax.set_xlabel(featureOne)
        ax.set_ylabel(featureTwo)
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.3)
        plt.grid()
        
        canvas1 = FigureCanvasTkAgg(fig, master = parent)
        canvas1.get_tk_widget().grid(row=7, column=3)
        canvas1.draw()
        
        ##################################
        ##################################
        ##################################


        
        ##################################
        ##################################
        ##################################
        
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=0, column=0)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=0, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=0, column=2)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=0, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=0, column=4)
        
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=1, column=0)
        label2 = tk.Label(text="Статистика", font=("Helvetica", 14))
        label2.grid(row=1, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=1, column=2)
        label2 = tk.Label(text="График", font=("Helvetica", 14))
        label2.grid(row=1, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=1, column=4)
        """
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=2, column=0)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=2, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=2, column=2)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=2, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=2, column=4)

        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=3, column=0)
        stat_label1 = tk.Label(text="Среднее кол-во уроков в месяц: " + str(num0), font=("Helvetica", 12)) #lessons
        stat_label1.grid(row=3, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=3, column=2)
        # ГРАФИК grid(row=3, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=3, column=4)
        """

        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=4, column=0)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=4, column=1)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=4, column=2)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=4, column=3)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=4, column=4)

        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=5, column=0)
        stat_label1 = tk.Label(text="Среднее кол-во посещений \nстудентами в месяц: " + str(num1), font=("Helvetica", 12)) #attendance
        stat_label1.grid(row=5, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=5, column=2)
        # ГРАФИК grid(row=5, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=5, column=4)

        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=6, column=0)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=6, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=6, column=2)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=6, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=6, column=4)

        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=7, column=0)
        stat_label1 = tk.Label(text="Среднее кол-во посещений \nна одного студента в месяц: " + str(num2), font=("Helvetica", 12)) #attendance
        stat_label1.grid(row=7, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=7, column=2)
        # ГРАФИК grid(row=7, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=7, column=4)
        
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=8, column=0)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=8, column=1)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=8, column=2)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=8, column=3)
        label2 = tk.Label(text=" ", font=("Helvetica", 14))
        label2.grid(row=8, column=4)
        
        """
        # Create and place labels
        label2 = tk.Label(self.dashboard_frame, text="Статистика", font=("Helvetica", 12))
        label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        label3 = tk.Label(self.dashboard_frame, text="График", font=("Helvetica", 12))
        label3.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # Create and place statistics widgets (placeholders)
        stat_label1 = tk.Label(self.dashboard_frame, text="Среднее кол-во уроков в месяц: ")
        stat_label1.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        stat_value1 = tk.Label(self.dashboard_frame, text=str(num1))
        stat_value1.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        stat_label2 = tk.Label(self.dashboard_frame, text="Среднее кол-во уроков на одного студента в месяц: ")
        stat_label2.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        stat_value2 = tk.Label(self.dashboard_frame, text=str(""))
        stat_value2.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Create and place graph widgets (placeholders)
        # You can use Matplotlib or other libraries for more advanced graphs
        
        graph1 = fig
        graph1.grid(row=2, column=2, padx=10, pady=5, sticky="nsew")
       
        graph2 = tk.Canvas(self.dashboard_frame, bg="white", width=300, height=150)
        graph2.grid(row=3, column=2, padx=10, pady=5, sticky="nsew")
        """

        # Configure grid layout weights to make the dashboard responsive
        """
        self.dashboard_frame.columnconfigure(0, weight=1)
        self.dashboard_frame.columnconfigure(1, weight=1)
        self.dashboard_frame.columnconfigure(2, weight=1)
        self.dashboard_frame.rowconfigure(2, weight=1)
        self.dashboard_frame.rowconfigure(3, weight=1)
        """
        

if __name__ == "__main__":
    
    parent = tk.Tk()
    app = DashboardApp(parent)
    parent.mainloop()

