from pymongo import MongoClient

def get_db(connection_string, database):
    """
    Establishes and returns a database connection to MongoDB Atlas.

    This function creates a connection to a MongoDB Atlas cluster using the provided
    connection string and returns a reference to the 'oneclick_brm' database.

    Note: In a production environment, consider:
    1. Moving the connection string to environment variables or a config file
    2. Implementing connection pooling for better performance
    3. Adding error handling for connection issues

    Input:
        Connection String

    Returns:
        Database: A database instance for the requested database
    """
    # Create a MongoClient to the running MongoDB instance
    # This handles connection pooling automatically
    client = MongoClient(connection_string)

    # Get a reference to the requested database
    # If the database doesn't exist, MongoDB will create it when you first store data
    db = client[database]

    return db

