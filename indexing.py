from langchain_community.document_loaders import PyPDFLoader

file_path ="documents/contrat_from29092025_to27122025.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))