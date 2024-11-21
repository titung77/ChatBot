from mongo_ingestor import MongoIngestor
from text_processor import TextProcessor
from config import configApp
from utils import load_dataset

INPUT_FILE = 'data/output.json'
THRESHOLD = 0.2
# Load dataset


def process_dataset():
    text_processor = TextProcessor(threshold=THRESHOLD)
    # Load and process dataset
    crawled_dataset_df = load_dataset(INPUT_FILE)
    print("Original dataset:")
    print(crawled_dataset_df.head(5))

    processed_df = text_processor.process_dataset(crawled_dataset_df)
    print("Processed dataset:")
    print(processed_df.head(5))

    # Generate embeddings
    processed_df["embedding"] = processed_df["content"].apply(
        text_processor.get_embedding,
    )
    # # save to json
    processed_df.to_json('data/output_processed.json', orient='records')

def ingest_to_mongo():
    processed_df = load_dataset("data/output_processed.json")
    mongo_ingestor = MongoIngestor(
        configApp.MONGO_URI,
        configApp.DB_NAME,
        configApp.DB_COLLECTION,
    )
    # Ingest data into MongoDB
    mongo_ingestor.ingest_to_mongodb(processed_df)

def main():
    # process_dataset()
    ingest_to_mongo()


if __name__ == "__main__":
    main()
