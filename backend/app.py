from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.llm import OpenAIClient
from core.rag import RAG
from core.semantic_router import SemanticRouter, Route
from core.semantic_router.samples import productSample, chitchatSample
from core.reflection import Reflection
from core.semantic_cache.core import SemanticCache
from core.embeddings import EmbeddingModel
from config import configApp
from models import ChatRequest

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize embedding model
embedding_model = EmbeddingModel()

# Initialize RAG
llm = OpenAIClient(configApp.OPENAI_API_KEY)
rag = RAG(
    mongodb_uri=configApp.MONGO_URI,
    db_name=configApp.DB_NAME,
    db_collection=configApp.DB_COLLECTION,
    vector_index_name=configApp.VECTOR_INDEX_NAME,
    keyword_index_name=configApp.KEYWORD_INDEX_NAME,
)

# Setup Semantic Router
PRODUCT_ROUTE_NAME = 'products'
CHITCHAT_ROUTE_NAME = 'chitchat'

productRoute = Route(name=PRODUCT_ROUTE_NAME, samples=productSample)
chitchatRoute = Route(name=CHITCHAT_ROUTE_NAME, samples=chitchatSample)
semanticRouter = SemanticRouter(routes=[productRoute, chitchatRoute])

# Setup Reflection
reflection = Reflection(
    llm=llm,
    mongodbUri=configApp.MONGO_URI,
    dbName=configApp.DB_NAME,
    dbChatHistoryCollection=configApp.DB_CHAT_HISTORY_COLLECTION,
    semanticCacheCollection=configApp.SEMANTIC_CACHE_COLLECTION,
)

# Setup Semantic Cache
semantic_cache = SemanticCache(
    mongodb_uri=configApp.MONGO_URI,
    db_name=configApp.DB_NAME,
    db_collection=configApp.SEMANTIC_CACHE_COLLECTION,
    index_name=configApp.SEMANTIC_CACHE_INDEX_NAME,
)

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id
    query = request.query

    # Find semantic router of the query
    guided_route = semanticRouter.guide(query)[1]
    print(f"semantic route: {guided_route}")

    # Semantic router is products, so we will use RAG
    if guided_route == PRODUCT_ROUTE_NAME:
        # Get query embedding
        query_embedding = embedding_model.get_embedding(query)

        # Check semantic cache
        cached_result = semantic_cache.retrieve_cached_result(query_embedding)
        if cached_result:
            print(f'Cache hit: {cached_result}')
            response = cached_result
        else:
            source_information = rag.enhance_prompt(query, query_embedding).replace('<br>', '\n')
            combined_information = f"Câu hỏi : {query}, \ntrả lời khách hàng sử dụng thông tin sản phẩm sau:\n###Sản Phẩm###\n{source_information}."
            response = reflection.chat(
                session_id=session_id,
                enhanced_message=combined_information,
                original_message=query,
                cache_response=True,
                query_embedding=query_embedding
            )
    else:
        # Semantic router is chitchat, so just call LLM
        response = reflection.chat(
            session_id=session_id,
            enhanced_message=query,
            original_message=query,
            cache_response=False,
        )

    return {"role": "assistant", "content": response}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
