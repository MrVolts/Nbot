import datetime
import pinecone
import os
from dotenv import load_dotenv
from database_handler import DatabaseHandler

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index = pinecone_index_name
index = pinecone.GRPCIndex(index)

def display_main_menu():
    print("Main Menu:")
    print("1. List categories")
    print("2. Fetch block IDs")
    print("3. Delete block IDs")
    print("0. Exit")


def display_categories_menu(db_handler):
    print("Categories:")
    categories = db_handler.list_categories()
    for category in categories:
        print(f" - {category}")


def display_namespaces_menu(db_handler):
    print("Namespaces:")
    namespaces = db_handler.list_namespaces()
    for namespace in namespaces:
        print(f" - {namespace}")


def display_datetime_range_menu(db_handler):
    print("Datetime range:")
    min_date, max_date = db_handler.list_datetime_range()
    print(f"From: {min_date}")
    print(f"To:   {max_date}")


def display_list_menu(db_handler):
    while True:
        print("\nList Menu:")
        print("1. Categories")
        print("2. Namespaces")
        print("3. Datetime range")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_categories_menu(db_handler)
        elif choice == '2':
            display_namespaces_menu(db_handler)
        elif choice == '3':
            display_datetime_range_menu(db_handler)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


def fetch_block_ids(db_handler):
    print("Fetch block IDs:")

    try:
        start_datetime_str = input("Enter start datetime (YYYY-MM-DD hh:mm:ss) or leave blank: ")
        if start_datetime_str:
            start_datetime = datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
        else:
            start_datetime = None

        end_datetime_str = input("Enter end datetime (YYYY-MM-DD hh:mm:ss) or leave blank: ")
        if end_datetime_str:
            end_datetime = datetime.datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
        else:
            end_datetime = None

        namespace = input("Enter namespace or leave blank: ")
        category = input("Enter category or leave blank: ")

        block_data = db_handler.fetch(start_datetime, end_datetime, namespace, category)

        print("\nBlock IDs:")
        for block_id, block_namespace, block_category, block_created_at in block_data:
            print(f"{block_id} (namespace: {block_namespace}, category: {block_category}, date added: {block_created_at})")

        return block_data

    except ValueError:
        print("Invalid datetime format. Please try again.")
        return []



def delete_block_ids(db_handler, block_data):
    for block_id, namespace, _, _ in block_data:
        response = index.delete(ids=[block_id], namespace=namespace)
        db_handler.delete_block(block_id, namespace)
        print(f"Deleted block ID {block_id} in namespace {namespace}.")



def main():
    # Initialize the database handler
    db_handler = DatabaseHandler()

    while True:
        display_main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            display_list_menu(db_handler)
        elif choice == '2':
            fetched_block_data = fetch_block_ids(db_handler)
            while True:
                delete_choice = input("\nDo you want to delete the fetched block IDs? (y/n): ")
                if delete_choice.lower() == 'y':
                    delete_block_ids(db_handler, fetched_block_data)
                    break
                elif delete_choice.lower() == 'n':
                    break
                else:
                    print("Invalid choice. Please enter 'y' or 'n'.")
        elif choice == '3':
            block_ids = input("Enter block IDs separated by a comma: ").split(',')
            block_data = [(block_id, db_handler.get_namespace_for_block_id(block_id), None, None) for block_id in block_ids]
            delete_block_ids(db_handler, block_data)
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
