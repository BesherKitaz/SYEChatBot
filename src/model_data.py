from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama          
from langchain_community.embeddings import HuggingFaceEmbeddings  
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough    
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
import os    


# --- 1) Ingest & chunk (use your own texts/files here) ---
texts = []
for file in os.listdir("../preprocessed_text"):
    with open(os.path.join("../preprocessed_text", file), "r", encoding="utf-8") as f:
        content = f.read()
        if len(content) > 5:
            texts.append(content)

docs = [Document(page_content=t) for t in texts]
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)


# --- 2) Embed + index ---


# Embed and store
embeddings = HuggingFaceEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- 3) Prompt + LLM ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the provided context to answer concisely."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])
llm = Ollama(model="llama3", temperature=0)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

# --- 4) Chain (Runnable graph) ---
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 5) Run ---
print(rag_chain.invoke("What is RAG and how does LangChain 1.x support it?"))




