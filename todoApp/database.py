from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://areebstudent567:g4bOtYWUfE9s@ep-fancy-glitter-82049478.us-east-2.aws.neon.tech/todos?sslmode=require', echo=True)



Base = declarative_base()


SessionLocal = sessionmaker(bind=engine)

#SessionLocal is often used as a dependency in FastAPI applications (as you can seen in main.py) to manage the lifecycle of
#database sessions. It ensures that each request gets its own database session and that the sessions are properly closed 
#when the request is finished.

