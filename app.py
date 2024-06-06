from flask import Flask, jsonify, request
import graphene
from graphene import ObjectType, String, Int, List, Field

app = Flask(__name__)

# Your existing books list
books = []

# Helper function to generate IDs
def generate_id():
    return len(books) + 1

# Define GraphQL schema
class KeyValue(ObjectType):
    name = String(description="Name of the item", required=True)
    author = String(description="Author of the item", required=True)
    status = String(description="Status of the item", required=True)

class Query(ObjectType):
    all_books = List(KeyValue)

    def resolve_all_books(self, info):
        return books

    book_by_id = Field(KeyValue, book_id=Int(required=True))

    def resolve_book_by_id(self, info, book_id):
        for book in books:
            if book['id'] == book_id:
                return book
        return None

class CreateBook(graphene.Mutation):
    class Arguments:
        name = String(required=True)
        author = String(required=True)
        status = String(required=True)

    book = Field(KeyValue)

    def mutate(self, info, name, author, status):
        book = {
            'id': generate_id(),
            'name': name,
            'author': author,
            'status': status
        }
        books.append(book)
        return CreateBook(book=book)

class Mutation(ObjectType):
    create_book = CreateBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# GraphQL endpoint
@app.route('/graphql', methods=['POST'])
def graphql_endpoint():
    data = request.get_json()
    result = schema.execute(data.get('query'))
    return jsonify(result.data)

if __name__ == '__main__':
    app.run()
