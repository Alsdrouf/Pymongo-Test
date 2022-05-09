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

        #Get the database named test
        testDB = client[self.dataBaseName]

        #Get the collection of the db
        personnes = testDB["personnes"]

        #Add a person
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        personne = { "firstname" : "Peter", "lastname" : "Pen", "created_at" : timestamp, "updated_at" : timestamp }

        id = personnes.insert_one(personne).inserted_id
        print(id)

        #Add persons
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        dictPersonnes = [
            {"firstname": "Jack", "lastname": "Sparrow", "created_at": timestamp, "updated_at": timestamp},
            {"firstname": "Orelsan", "lastname": "", "created_at": timestamp, "updated_at": timestamp},
            {"firstname": "Patrique", "lastname": "", "created_at": timestamp, "updated_at": timestamp},
            {"firstname": "Pomme", "lastname": "", "created_at": timestamp, "updated_at": timestamp}
        ]
        personnes.insert_many(dictPersonnes)

        #get the created person by id
        personne = personnes.find_one({"_id" : id})
        print("By id : ", personne)

        #get the created person by the name
        personne = personnes.find_one({ "firstname" : "Peter" })
        print("By name", personne)
        time.sleep(0.1)

        #get the created person by the first letter:
        personne = personnes.find_one({ "firstname" : { "$regex" : "^P" } })
        print("By first letter name", personne)

        #get all the person that have an id greater than 5
        group_of_personnes = personnes.find({ "firstname" : {"$gt" : 5 } })
        for personne in group_of_personnes:
            print(personne)

        #sort the result of a query
        print("Sorted Result")
        sorted_personnes = personnes.find().sort("firstname")
        for personne in sorted_personnes:
            print(personne)
        print("End Of Sorted Result")

        #delete the created personne
        personnes.delete_one({ "_id" : id })

        #delete all the personne that have a name that start with P
        count = personnes.delete_many({ "firstname" : { "$regex" : "^P" } }).deleted_count
        print("Deleted " + str(count) + " personnes")

        #update the person
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        personne = {"firstname": "Peter", "lastname": "Pen", "created_at": timestamp, "updated_at": timestamp}

        id = personnes.insert_one(personne).inserted_id
        print(id)

        personnes.update_one({ "_id" : id }, { "$set" : { "lastname" : "Pan" } })

        personnes.drop()

dbManager = DBManager()
dbManager.run()

