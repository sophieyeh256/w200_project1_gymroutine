"""
References:
https://docs.scrapy.org/en/latest/
https://exrx.net/
"""
import json
from os.path import exists
import scrapy
from scrapy.crawler import CrawlerProcess
import re
from LibrarySpider import LibrarySpider

class Library:
    """ Class for dictionary of exercises, reformatted for application """
    def __init__(self):
        self.categories = set([]) # categories for exercises
        libraryFilePath = 'library.json'
        # initalizes web crawler if no json file
        if not exists(libraryFilePath):
            self.extract_library()
            with open(libraryFilePath) as f:
                self.library = json.loads(f.read())
            with open(libraryFilePath, 'wt') as f:
                self.library = json.dump(self.reformat(), f, indent=4)
        # opens existing json file
        with open(libraryFilePath, 'rt') as f:
            self.library = json.loads(f.read())
        # replaces a single ampersand due to json file
        self.library['Lunge and Rear Lunge'] = self.library.pop(" Lunge &amp; Rear Lunge  And")
        # creates sorted list of unique categories based on json
        for item in self.library:
            for muscle in self.library[item]:
                self.categories.add(muscle)
        self.categories = sorted(list(self.categories))


    def extract_library(self):
        """ starts scrapy crawl """
        process = CrawlerProcess(settings={
                                "FEEDS": {
                                    "library.json": {"format": "json",
                                                    "overwrite":True,
                                                    'indent': 4},
                                                    },
                                })
        process.crawl(LibrarySpider)
        process.start()


    def reformat(self):
        """ Reformats dictionary so that {exercise:[muscle categories]} """
        newDict = {}
        for item in self.library:
            for key in item.keys():
                for task in item[key]:
                    # task = ["Neck Extension",
                    # "https://exrx.net/WeightExercises/Splenius/STNeckExtension"]
                    name = task[0]
                    link = task[1]
                    # get task name from last part of url
                    match_link = re.compile(r'\/[A-Za-z\d]+$').search(link)[0][1:]
                    # separate words in name
                    caps = re.compile(r'[A-Z][a-z]*').finditer(match_link)
                    prefix = '' #capture 'ST' part
                    before = True # match_link words before name
                    isPrefix = True
                    # loop helps retain unicodes in name
                    # while adding information from url name
                    for cap in caps:
                        if cap[0].isupper() and isPrefix == True:
                            prefix += cap[0]
                        elif cap[0] in name: # keep name part
                            before = False
                            isPrefix = False
                        elif before == False: # append words before name
                            name += " " + (cap[0])
                            isPrefix = False
                        else: # append words following name
                            name = cap[0] + " " + name

                    name = prefix + ' ' + name
                    # result becomes ['LV 45° Calf Raise P L']
                    # inverting dictionary to {exercise:[categories]}
                    if name not in newDict:
                        newDict[name] = [key]
                    elif key not in newDict[name]:
                        newDict[name].append(key)
        return newDict


    def __repr__(self):
        return self.library


    def __str__(self):
        return str(self.library)


    def __dict__(self):
        return self.library
