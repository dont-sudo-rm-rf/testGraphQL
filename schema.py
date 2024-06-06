import graphene


class Key(graphene.ObjectType):
    id = graphene.String(description="Unique identifier for the key")

class Status(graphene.ObjectType):
    status = graphene.String(description="Status of the item")

class KeyValue(graphene.ObjectType):
    name = graphene.String(description="Name of the item", required=True)
    author = graphene.String(description="Author of the item", required=True)
    status = graphene.String(description="Status of the item", required=True)

class StringArray(graphene.List(graphene.String)):
    pass


class Query(graphene.ObjectType):
    all_books = graphene.List(KeyValue)

    def resolve_all_books(self, info):
        # Fetch data from your existing 'books' list
        return books


class CreateBook(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        author = graphene.String(required=True)
        status = graphene.String(required=True)

    book = graphene.Field(KeyValue)

    def mutate(self, info, name, author, status):
        # Create a new book and add it to the 'books' list
        book = {
            'id': generate_id(),
            'name': name,
            'author': author,
            'status': status
        }
        books.append(book)
        return CreateBook(book=book)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()



class Query(graphene.ObjectType):
    book_by_id = graphene.Field(KeyValue, book_id=graphene.Int(required=True))

    def resolve_book_by_id(self, info, book_id):
        # Find the book with the specified ID
        for book in books:
            if book['id'] == book_id:
                return book
        return None


class DeleteBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, book_id):
        # Remove the book with the specified ID
        global books
        books = [book for book in books if book['id'] != book_id]
        return DeleteBook(success=True)

class Mutation(graphene.ObjectType):
    delete_book = DeleteBook.Field()



class UpdateBookStatus(graphene.Mutation):
    class Arguments:
        book_id = graphene.Int(required=True)
        status = graphene.String(required=True)

    book = graphene.Field(KeyValue)

    def mutate(self, info, book_id, status):
        # Update the status of the book with the specified ID
        for book in books:
            if book['id'] == book_id:
                book['status'] = status
                return UpdateBookStatus(book=book)
        return None

class Mutation(graphene.ObjectType):
    update_book_status = UpdateBookStatus.Field()

