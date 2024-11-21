from dotenv import load_dotenv
import os

load_dotenv() 

class ConfigApp:
    MONGO_URI = os.getenv('MONGO_URI')
    DB_NAME = os.getenv('DB_NAME')
    DB_COLLECTION = os.getenv('DB_COLLECTION')
    DB_CHAT_HISTORY_COLLECTION = os.getenv('DB_CHAT_HISTORY_COLLECTION')
    SEMANTIC_CACHE_COLLECTION = os.getenv('SEMANTIC_CACHE_COLLECTION')
    VECTOR_INDEX_NAME = os.getenv('VECTOR_INDEX_NAME')
    KEYWORD_INDEX_NAME = os.getenv('KEYWORD_INDEX_NAME')
    SEMANTIC_CACHE_INDEX_NAME = os.getenv('SEMANTIC_CACHE_INDEX_NAME')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    
configApp = ConfigApp()
os.environ["OPENAI_API_KEY"] = configApp.OPENAI_API_KEY
