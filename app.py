from flask import Flask, jsonify, request
import graphene
from graphql_server.flask import GraphQLView

app = Flask(__name__)



# Your existing books list
books = [
    {
        "id": "6",
        "name": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "status": "read"
    },
    {
        "id": "2",
        "name": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "status": "unread"
    },
    {
        "id": "3",
        "name": "1984",
        "author": "George Orwell",
        "status": "in progress"
    }
]

# helper function for ID generation
def generate_id():
    return len(books) + 1

# GraphQL schema
class Book(graphene.ObjectType):
    id = graphene.String(description = " number of the book", required = True)
    name = graphene.String(description="Name of the book", required=True)
    author = graphene.String(description="Author of the book", required=True)
    status = graphene.String(description="Status of the book", required=True)

class Query(graphene.ObjectType):
    all_books = graphene.List(Book)

    

    def resolve_all_books(self, info):
        return books

    book_by_id = graphene.Field(Book, book_id=graphene.Int(required=True))
    
    def resolve_book_by_id(self, info, book_id):
        for book in books:
            if book['id'] == str(book_id):
                return book
        return None

# class CreateBook(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         author = graphene.String(required=True)
#         status = graphene.String(required=True)

#     book = graphene.Field(Book)

#     def mutate(self, info, name, author, status):
#         book = {
#             'id': generate_id(),
#             'name': name,
#             'author': author,
#             'status': status
#         }
#         books.append(book)
#         return CreateBook(book=book)

# class Mutation(graphene.ObjectType):
#     create_book = CreateBook.Field()

# schema = graphene.Schema(query=Query, mutation=Mutation)

schema = graphene.Schema(query=Query)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema = schema,
        graphiql=True
    )
)


# GraphQL endpoint
@app.route('/graphql', methods=['GET', 'POST'])
def graphql_endpoint():
    if request.method == 'GET':
        # Handle GET request to fetch schema
        return jsonify({'schema': schema.to_dict()})
    elif request.method == 'POST':
        # Handle POST request for executing GraphQL queries
        data = request.get_json()
        result = schema.execute(data.get('query'))
        return jsonify(result.data)


if __name__ == '__main__':
    app.run()
