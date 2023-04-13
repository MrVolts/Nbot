from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, and_, func, select
from sqlalchemy.orm import declarative_base, Session
import datetime
import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index = pinecone_index_name
index = pinecone.GRPCIndex(index)

Base = declarative_base()

class PineconeBlock(Base):
    __tablename__ = 'pinecone_blocks'

    id = Column(Integer, primary_key=True)
    block_id = Column(String, nullable=False)
    source = Column(String, nullable=False)
    chunk = Column(Integer, nullable=False)
    namespace = Column(String, nullable=True)  # Add the namespace column
    index = Column(Integer, nullable=True)  # Add the index column
    created_at = Column(DateTime)

class DatabaseHandler:
    def __init__(self, index=None):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pinecone_blocks.db')
        self.engine = create_engine(f'sqlite:///{db_path}')
        
        Base.metadata.create_all(self.engine)
        self.index = index

    def insert_block(self, block_id, source, chunk, namespace=None, index=None, created_at=None):
        with self.engine.connect() as conn:
            # Create a session bound to the connection
            session = Session(bind=conn)

            # Use the current time as the default value for created_at if it's not provided
            if created_at is None:
                created_at = datetime.datetime.utcnow()

            # Create a PineconeBlock instance
            block = PineconeBlock(block_id=block_id, source=source, chunk=chunk, namespace=namespace, index=index, created_at=created_at)

            # Add and commit the PineconeBlock instance to the database
            session.add(block)
            session.commit()

            # Close the session
            session.close()
            
    def list_sources(self):
        with self.engine.connect() as conn:
            result = conn.execute(select(PineconeBlock.source).distinct())
            sources = [row[0] for row in result]
            return sources
        
    def list_namespaces(self):
        with self.engine.connect() as conn:
            result = conn.execute(select(PineconeBlock.namespace).distinct())
            namespaces = [row[0] for row in result]
            return namespaces
        
    def list_indices(self):
        with self.engine.connect() as conn:
            result = conn.execute(select(PineconeBlock.index).distinct())
            indices = [row[0] for row in result if row[0] is not None]
            return indices
        
    def list_datetime_range(self):
        with self.engine.connect() as conn:
            query = select([func.min(PineconeBlock.created_at).label('min_date'),
                            func.max(PineconeBlock.created_at).label('max_date')])
            result = conn.execute(query)
            row = result.fetchone()
            min_date, max_date = row['min_date'], row['max_date']
        return min_date, max_date
        
    def delete_block_by_id(self, block_ids):
        with self.engine.connect() as conn:
            # Fetch the namespace for the given block IDs from the database
            query = select(PineconeBlock.namespace).where(PineconeBlock.block_id.in_(block_ids))
            result = conn.execute(query)
            namespaces = set(row[0] for row in result)

            # Delete the blocks from the database and Pinecone index
            conn.execute(PineconeBlock.__table__.delete().where(PineconeBlock.block_id.in_(block_ids)))

            # Process block IDs in chunks of 1000 or fewer
            max_ids_per_request = 1000
            for namespace in namespaces:
                for i in range(0, len(block_ids), max_ids_per_request):
                    chunk = block_ids[i:i + max_ids_per_request]
                    index.delete(ids=chunk, namespace=namespace)
            
    def list_block_ids(self, source=None, namespace=None, index=None, start_time=None, end_time=None):
        with self.engine.connect() as conn:
            query = select(PineconeBlock.block_id)
            if source:
                query = query.where(PineconeBlock.source == source)
            if namespace:
                query = query.where(PineconeBlock.namespace == namespace)
            if index is not None:
                query = query.where(PineconeBlock.index == index)
            if start_time and end_time:
                query = query.where(and_(PineconeBlock.created_at >= start_time, PineconeBlock.created_at <= end_time))
            result = conn.execute(query)
            block_ids = [row[0] for row in result]
            return block_ids

db_handler = DatabaseHandler()



#block_id = db_handler.list_block_ids(source="⚫-general-internal")
 
#print(block_id)