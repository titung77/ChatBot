import pandas as pd
from models import LoadDocumentRequest

def load_dataset(input_file: str) -> pd.DataFrame:
    return pd.read_json(input_file)


def load_dataset_from_json(load_document_request: list[LoadDocumentRequest]) -> pd.DataFrame:
    return pd.DataFrame([doc.model_dump() for doc in load_document_request])