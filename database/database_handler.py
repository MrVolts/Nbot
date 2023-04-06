from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_, func, select
import datetime
import os

class DatabaseHandler:
    def __init__(self, index=None):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pinecone_blocks.db')
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.metadata = MetaData()
        self.pinecone_blocks = Table('pinecone_blocks', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('block_id', String),
                            Column('channel', String),
                            Column('namespace', String, nullable=False),
                            Column('created_at', DateTime)
                            )
        self.index = index

        # Create the table if it doesn't exist
        self.metadata.create_all(self.engine)

    def insert_block(self, block_id, channel, namespace=None, created_at=None):
        with self.engine.connect() as conn:
            # Use the current time as the default value for created_at if it's not provided
            if created_at is None:
                created_at = datetime.datetime.utcnow()

            # Insert the data into the database
            conn.execute(self.pinecone_blocks.insert().values(block_id=block_id, channel=channel, namespace=namespace, created_at=created_at))
            
    def fetch(self, start_datetime=None, end_datetime=None, namespace=None, category=None):
        with self.engine.connect() as conn:
            query = self.pinecone_blocks.select()

            if start_datetime is not None and end_datetime is not None:
                query = query.where(and_(self.pinecone_blocks.c.created_at >= start_datetime,
                                        self.pinecone_blocks.c.created_at <= end_datetime))

            if namespace is not None and namespace.strip():
                query = query.where(self.pinecone_blocks.c.namespace == namespace)

            if category is not None and category.strip():
                query = query.where(self.pinecone_blocks.c.channel == category)

            print("Generated SQL query:")
            print(str(query))

            result = conn.execute(query)
            block_data = [(row['block_id'], row['namespace'], row['channel'], row['created_at']) for row in result]

        return block_data


    def list_namespaces(self):
        with self.engine.connect() as conn:
            query = select([self.pinecone_blocks.c.namespace]).distinct()
            result = conn.execute(query)
            namespaces = [row['namespace'] for row in result]

        return namespaces

    def list_datetime_range(self):
        with self.engine.connect() as conn:
            query = select([func.min(self.pinecone_blocks.c.created_at).label('min_date'),
                            func.max(self.pinecone_blocks.c.created_at).label('max_date')])
            result = conn.execute(query)
            row = result.fetchone()
            min_date, max_date = row['min_date'], row['max_date']

        return min_date, max_date

    def list_categories(self):
        with self.engine.connect() as conn:
            query = select([self.pinecone_blocks.c.channel]).distinct()
            result = conn.execute(query)
            categories = [row['channel'] for row in result]

        return categories
    
    def get_namespace_for_block_id(self, block_id):
        with self.engine.connect() as conn:
            query = select([self.pinecone_blocks.c.namespace]).where(self.pinecone_blocks.c.block_id == block_id)
            result = conn.execute(query)
            row = result.fetchone()
            if row:
                return row['namespace']
            else:
                return None