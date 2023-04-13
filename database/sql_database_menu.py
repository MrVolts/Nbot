from sql_database_handler import DatabaseHandler, index

class SQLDatabaseMenu:
    def __init__(self):
        self.handler = DatabaseHandler(index)

    def display_menu(self):
        while True:
            print("Select an option:")
            print("1. List Categories")
            print("2. Fetch Block")
            print("3. Delete Block ID")
            print("4. Exit")
            choice = input()
            if choice == '1':
                self.display_categories()
            elif choice == '2':
                self.fetch_block()
            elif choice == '3':
                self.delete_block()
            elif choice == '4':
                break
            else:
                print("Invalid input. Please try again.")

    def display_categories(self):
        while True:
            print("Select a category:")
            print("1. Sources")
            print("2. Namespaces")
            print("3. Index")
            print("4. Time Range")
            print("5. Back")
            choice = input()
            if choice == '1':
                self.list_sources()
            elif choice == '2':
                self.list_namespaces()
            elif choice == '3':
                self.list_indices()
            elif choice == '4':
                self.list_time_range()
            elif choice == '5':
                break
            else:
                print("Invalid input. Please try again.")


    def list_sources(self):
        sources = self.handler.list_sources()
        print("Sources:")
        for source in sources:
            print(source)
        print("")

    def list_namespaces(self):
        namespaces = self.handler.list_namespaces()
        print("Namespaces:")
        for namespace in namespaces:
            print(namespace)
        print("")

    def list_indices(self):
        indices = self.handler.list_indices()
        print("Indices:")
        for index in indices:
            print(index)
        print("")

    def list_time_range(self):
        min_date, max_date = self.handler.list_datetime_range()
        print("Datetime range:")
        print(f"Min: {min_date}")
        print(f"Max: {max_date}")
        print("")

    def fetch_block(self):
        source = input("Enter source: ")
        namespace = input("Enter namespace (optional): ")
        index = input("Enter index (optional): ")
        start_time = input("Enter start time (optional - format: YYYY-MM-DD HH:MM:SS): ")
        end_time = input("Enter end time (optional - format: YYYY-MM-DD HH:MM:SS): ")
        block_ids = self.handler.list_block_ids(source=source or None, 
                                                namespace=namespace or None, 
                                                index=index or None, 
                                                start_time=start_time or None, 
                                                end_time=end_time or None)
        if len(block_ids) == 0:
            print("No blocks found.\n")
            return
        print("Blocks:")
        for block_id in block_ids:
            print(block_id)
        print("")
        choice = input("Do you want to delete these blocks? (y/n): ")
        if choice == 'y':
                block_ids = [str(block_id) for block_id in block_ids]
                self.handler.delete_block_by_id(block_ids)
                print("Blocks deleted.")
                print("")
        elif choice == 'n':
                return
        else:
                print("Invalid input. Please try again.")
                return

    def delete_block(self):
        block_ids = input("Enter block IDs separated by commas: ")
        block_ids = block_ids.split(",")
        block_ids = [block_id.strip() for block_id in block_ids]
        self.handler.delete_block_by_id(block_ids)
        print("Blocks deleted.")
        print("")
        
if __name__ == "__main__":
    menu = SQLDatabaseMenu()
    menu.display_menu()