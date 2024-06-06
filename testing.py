import graphene
import json


from graphene import ObjectType, String


class Person(ObjectType):
    name = String(description = "first name of a person")
    age = String()


class Query(ObjectType):
    name = String(description = "first name of a person")




    def resolve_n(root, )