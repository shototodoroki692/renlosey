import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

file_path ="documents/contrat_from29092025_to27122025.pdf"
loader = PyPDFLoader(file_path)

# Chargement de notre fichier associé au chemin file_path.
# La réponse renvoyée (docs) est un tableau contenant un document par page
# de notre fichier PDF.
docs = loader.load()

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

# Initialisation de notre fournisseur d'embeddings.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


# embedding de nos deux premiers chunks.
vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

# Vérifier que les deux vecteurs ont effectivement la même taille.
assert len(vector_1) == len(vector_2)

print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])

# Chargement des variables d'environnement.
load_dotenv()

# Récupération des informations de notre base de données postgres
postgres_db = os.environ['POSTGRES_DB']
postgres_user = os.environ['POSTGRES_USER']
postgres_password = os.environ['POSTGRES_PASSWORD']
postgres_conn_str = f"postgresql+psycopg://{postgres_user}:{postgres_password}@localhost:5432/{postgres_db}"
print(postgres_db, postgres_user, postgres_password)

# Connexion à notre base de données vectorielle PostgreSQL.
vector_store = PGVector(
   embeddings=embeddings,
   collection_name="my_docs",
   connection=postgres_conn_str,
)

# Ajouter nos chunks à la base de données.
ids = vector_store.add_documents(documents=all_splits)

# Faire une recherche par similarité entre le prompt ci-dessous et
# les chunks figurants dans notre base de données.
results = vector_store.similarity_search_with_score("Quel est le nom des assurés ?")

# Pour chaque résultat, afficher le score de similarité
for result in results:
   document, score = result
   print(f"document: {document.metadata}...; score: {score}\n")