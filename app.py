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

# GraphQL schema for a book
class Book(graphene.ObjectType):
    id = graphene.String(description="Number of the book", required=True)
    name = graphene.String(description="Name of the book", required=True)
    author = graphene.String(description="Author of the book", required=True)
    status = graphene.String(description="Status of the book", required=True)

# Defines the available Queries
class Query(graphene.ObjectType):
    # What you wish to query
    all_books = graphene.List(Book)

    # Resolver function (required. To my understand it needs to follow structure 'resolve'_'name')
    def resolve_all_books(self, info):
        return books

    book_by_id = graphene.Field(Book, book_id=graphene.Int(required=True))

    def resolve_book_by_id(self, info, book_id):
        for book in books:
            if book['id'] == str(book_id):
                return book
        return None

# Define the CreateBook mutation
class CreateBook(graphene.Mutation):
    class Arguments:
        # Input arguments for the mutation
        name = graphene.String(required=True)
        author = graphene.String(required=True)
        status = graphene.String(required=True)

    # The response of the mutation
    book = graphene.Field(Book)

    # The mutate method handles the mutation logic
    def mutate(self, info, name, author, status):
        new_book = {
            'id': generate_id(),
            'name': name,
            'author': author,
            'status': status
        }
        books.append(new_book)
        return CreateBook(book=new_book)

# Mutation class that includes the CreateBook mutation
class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()

# Include both Query and Mutation in the schema
schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema = schema,
        graphiql=True
    )
)


# Alternative to app.add_url_rule (app.add_url_rule works just as well) 

# # GraphQL endpoint
# @app.route('/graphql', methods=['GET', 'POST'])
# def graphql_endpoint():
#     if request.method == 'GET':
#         # Handle GET request to fetch schema
#         return jsonify({'schema': schema.to_dict()})
#     elif request.method == 'POST':
#         # Handle POST request for executing GraphQL queries
#         data = request.get_json()
#         result = schema.execute(data.get('query'))
#         return jsonify(result.data)


if __name__ == '__main__':
    app.run()
