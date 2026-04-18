from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path ="documents/contrat_from29092025_to27122025.pdf"
loader = PyPDFLoader(file_path)

# Chargement de notre fichier associé au chemin file_path.
# La réponse renvoyée (docs) est un tableau contenant un document par page
# de notre fichier PDF.
docs = loader.load()

# Afficher le nombre de documents récupérés. Autrement dit le nombre de pages
# de notre fichier PDF.
# print(len(docs))

# Afficher les 200 premiers caractère de la première page de notre fichier PDF.
# print(f"{docs[0].page_content[:200]}\n")

# Afficher les metadata de la première page de notre fichier PDF.
# print(docs[0].metadata)

# Déclarer un splitter de texte découpant le texte en morceaux de 1000
# caractères, avec un chevauchement (nombre de caractères de fin d'un chunk
# présents au début du chunk suivant) de 200.
# add_start_index permet d'ajouter dans les metadata l'index du premier 
# caractère d'un chunk dans son document d'origine.
text_splitter = RecursiveCharacterTextSplitter(
   chunk_size=1000, chunk_overlap=200, add_start_index=True
)

# Découper les pages de notre fichier PDF avec notre splitter.
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))
print(all_splits[1].metadata)
print(f"chunk 1:\n\n{all_splits[0].page_content}\n")
print(f"chunk 2:\n\n{all_splits[1].page_content}\n")