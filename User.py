"""
Queries sqlite database,
Executes sqlite database edits based on user edits
User-specific plan and
Queries/edits sqlite database
https://www.sqlitetutorial.net/sqlite-python/
"""
from datetime import datetime
import os
import sqlite3
from sqlite3 import Error
from Database import Database
from Library import Library

class User:
    """ For user-specific inforamtion, including current plan and pie chart """
    def __init__(self, Database, id, month=(datetime.now().month, datetime.now().year)):

        # initalize variables
        self.db = Database
        self.conn = Database.conn
        self.library = self.db.library.__dict__()
        self.cal_month = month # tup(month,year); defaults to today
        # create user if "New User" is selected
        if id == 'New User':
            self.id = self.create_user()
        else:
            self.id = id
        self.plan = []
        self.pie = {'Neck':0, 'Back':0, 'Thighs':0,
                'Hips':0, 'Chest':0, 'Calves':0,
                'Forearms':0, 'Upper Arms':0, 'Shoulders':0}
        self.update() #updates plan and pie

    def __repr__(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def __dict__(self):
        new = {}
        for record in self.plan:
            new[record[0]] = (record[1], record[2])
        return new

    def update(self, month = None):
        """ wrapper function to update User Plan and Pie Chart information"""
        self.updatePlan()
        self.updatePie(month)

    def updatePie(self, month = None):
        """ Updates pie chart based on user plan and calendar month """
        # update month if specified
        if month != None:
            self.cal_month = month
        self.pie = {'Neck':0, 'Back':0, 'Thighs':0,
                'Hips':0, 'Chest':0, 'Calves':0,
                'Forearms':0, 'Upper Arms':0, 'Shoulders':0, 'Waist':0}
        for item in self.plan:
            # add to pie if user plan is in selected calender month
            if (int(item[1][5:7]),int(item[1][:4])) == self.cal_month and item[2] in self.library.keys():
                for muscle in self.library[item[2]]:
                    self.pie[muscle] += 1
    ############################################################################
    ########################## QUERY DATABASE ##################################
    ############################################################################
    def updatePlan(self):
        """ query user's tasks from sqlite db """
        sql_plans = """ SELECT id,
                         date,
                         task
                  FROM plans
                  WHERE user_id = ?
              """
        # connect to database and execute sql code
        cur = self.conn.cursor()
        cur.execute(sql_plans, (self.id,))
        self.plan = cur.fetchall()
        return self.plan
        #[(plan_id, date, task)]

    ############################################################################
    ########################### EDIT DATABASE ##################################
    ############################################################################
    def create_user(self): # only called in init
        """ Create a new user in sqlite db and return user id """
        sql = ''' INSERT INTO users(id, numDays)
                  VALUES(NULL,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (3,))
        self.conn.commit()
        return cur.lastrowid

    def create_task(self, date, task):
        """
        Create a new task in sqlite db's plans table
        :param: (date, exercise, user_id)
        :return: task_id
        """
        sql = ''' INSERT INTO plans (id,
                                date,
                                task,
                                user_id)
                  VALUES(NULL,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (date, task, self.id))
        task_id  = cur.lastrowid
        self.conn.commit()
        self.update()
        return task_id

    def update_task(self, task, plan_id):
        """
        Change selected task
        :param: (task, plan_id)
        :return: None
        """
        sql_plans = ''' UPDATE plans
                  SET task = ?
                  WHERE id = ?'''
        task = (task, plan_id)
        cur = self.conn.cursor()
        cur.execute(sql_plans, task)
        self.conn.commit()
        self.update()
        return

    def delete_task(self, plan_id):
        """ Delete a task by plan_id
        :param: plan_id
        :return: None
        """
        sql_plans = 'DELETE FROM plans WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql_plans, (plan_id,))
        self.conn.commit()
        self.update()
