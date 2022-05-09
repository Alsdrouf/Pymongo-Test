import time

import pymongo
import datetime
import asyncio

class DBManager:
    def __init__(self):
        self.dataBaseName = "test"

    def run(self):
        #Get the mongo client from default port and ip
        client = pymongo.MongoClient()

        #Check if the db exist
        if self.dataBaseName in client.list_database_names():
            print("Retrieving the database")
        else:
            print("Creating the database")

        #Add a person
        personne = Personne(firstname="Peter", lastname="Pen")

        id = personne.id
        print(id)

        #Add persons
        timestamp = datetime.datetime.now().isoformat()
        dictPersonnes = [
            {"firstname": "Jack", "lastname": "Sparrow", "created_at": timestamp, "updated_at": timestamp},
            {"firstname": "Orelsan", "lastname": "", "created_at": timestamp, "updated_at": timestamp},
            {"firstname": "Patrique", "lastname": "", "created_at": timestamp, "updated_at": timestamp},
            {"firstname": "Pomme", "lastname": "", "created_at": timestamp, "updated_at": timestamp}
        ]
        Personne.insert_many(dictPersonnes)

        #get the created person by id
        personne = Personne.find_one({"_id": id})
        print("By id :", personne.toString())

        #get the created person by the name
        personne = Personne.find_one({ "firstname" : "Peter" })
        print("By name", personne.toString())

        #get the created person by the first letter:
        personne = Personne.find_one({ "firstname" : { "$regex" : "^P" } })
        print("By first letter name", personne.toString())

        #get all the person that have an id greater than 5
        group_of_personnes = Personne.find({ "firstname" : {"$gt" : 5 } })
        for personne in group_of_personnes:
            print(personne.toString())

        #sort the result of a query
        print("Sorted Result")
        sorted_personnes = Personne.find()
        for personne in sorted_personnes:
            print(personne.toString())
        print("End Of Sorted Result")

        #delete the created personne
        Personne.delete_one({ "_id" : id })

        #delete all the personne that have a name that start with P
        count = Personne.DB.delete_many({ "firstname" : { "$regex" : "^P" } }).deleted_count
        print("Deleted " + str(count) + " personnes")

        #update the person
        timestamp = datetime.datetime.now().isoformat()
        personne = {"firstname": "Peter", "lastname": "Pen", "created_at": timestamp, "updated_at": timestamp}

        id = Personne.DB.insert_one(personne).inserted_id
        print(id)

        Personne.DB.update_one({ "_id" : id }, { "$set" : { "lastname" : "Pan" } })

        personne = Personne.DB.find_one({ "_id": id })

        print("Updated Personne : ", personne)

        Personne.DB.drop()

class Personne:
    DB = pymongo.MongoClient()["test"]["Personnes"]

    def __init__(self, firstname=None, lastname=None, isCreated=False):
        self.firstname = firstname
        self.lastname = lastname
        self.created_at = None
        self.updated_at = None
        self.id = None

        if not isCreated:
            self.insertMe()

    @classmethod
    def createPersonneWith(cls, personne):
        _personne = cls(firstname=personne["firstname"], lastname=personne["lastname"], isCreated=True)
        _personne.id = personne["_id"]
        _personne.created_at = personne["created_at"]
        _personne.updated_at = personne["updated_at"]
        return _personne

    def insertMe(self):
        self.created_at = Personne.getTimeStamp()
        self.updated_at = Personne.getTimeStamp()
        self.id = Personne.DB.insert_one(
            {"firstname": self.firstname, "lastname": self.lastname, "created_at": self.created_at,
             "updated_at": self.updated_at}).inserted_id

    def toString(self):
        dict = {}
        dict["_id"] = self.id
        dict["firstname"] = self.firstname
        dict["lastname"] = self.lastname
        dict["created_at"] = self.created_at
        dict["updated_at"] = self.updated_at
        return str(dict)

    @staticmethod
    def find_one(query):
        resPersonne = Personne.DB.find_one(query)
        return Personne.createPersonneWith(resPersonne)

    @staticmethod
    def find(query={}):
        resPersonnes = Personne.DB.find(query)
        personneList = []
        for personne in resPersonnes:
            personneList.append(Personne.createPersonneWith(personne))
        return  personneList

    @staticmethod
    def delete_one(query):
        Personne.DB.delete_one(query)

    @staticmethod
    def getTimeStamp():
        return datetime.datetime.now().isoformat()

    @staticmethod
    def insert_many(dict):
        Personne.DB.insert_many(dict)



dbManager = DBManager()
dbManager.run()

