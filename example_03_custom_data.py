# READ THIS BLOG POST FIRST! IT EXPLAINS THIS FILE'S PROCESS
# https://github.com/ollama/ollama/blob/main/docs/tutorials/langchainpy.md

# https://python.langchain.com/docs/modules/data_connection/vectorstores/
# https://python.langchain.com/docs/get_started/quickstart/

import readline # allows arrow-key movement in input()
import os

# OLLAMA NEEDS TO BE RUNNING IN THE BACKGROUND ALREADY!

from langchain_community.llms import Ollama
llm = Ollama(model="llama2")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
   ("system", "Answer only based on the information in the context. Mention the chapters that you base the answers on and show a relevant quote from the context."),
    ("user", "{input}"),
])

chain = prompt | llm 

#########################
# Prepare the local data 
#########################

from langchain_community.document_loaders import WebBaseLoader, UnstructuredFileLoader
# Use a local copy
# loader = UnstructuredFileLoader("prince.txt")
# or... directly download The Prince by Machiavelli
loader = WebBaseLoader("https://www.gutenberg.org/files/1232/1232-h/1232-h.htm")
data = loader.load()

# a very naive splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
all_splits = text_splitter.split_documents(data)


from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
oembed = OllamaEmbeddings(model="nomic-embed-text")

print("Trying to load vector store")
# Delete the database manually to regenerate. TODO: improve this. 
if os.path.exists("db/chroma.sqlite3"):
    print("we have a database already, loading it")
    vectorstore = Chroma(
        persist_directory="./db", 
        embedding_function=oembed
    )
    print("Success")
else:
    print("Failed. Regenerating the database. This will take a while...")
    vectorstore = Chroma.from_documents(
        documents=all_splits, 
        embedding=oembed,
        persist_directory="./db"
    )
    print("Done")

################################
# Done preparing the local data
################################

# # Example use of the data store
# print("Similarity search")
# question="What should a prince without allies do?"
# docs = vectorstore.similarity_search(question)
# print(docs)
# exit()


from langchain.chains import RetrievalQA

print("Making retriever")
retriever = vectorstore.as_retriever()

print("Building chain")
qachain=RetrievalQA.from_chain_type(chain, retriever=retriever)


while True:
    question = input("Next question [leave blank to quit]: ")
    if not question: 
        break
    answer = qachain.invoke({"query": question})
    print(answer['result'])
    print()

# Try asking about the text, but also try things that are not mentioned:
# "Who is Angela Chase?" will give a different result here than 
# in default llama2
