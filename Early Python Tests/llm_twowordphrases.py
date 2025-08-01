from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

phrase1 = "water bottle"
phrase2 = "bottle water"
phrase3 = "hot topic"
phrase4 = "wet pizza"

emb1 = model.encode(phrase1)
emb2 = model.encode(phrase2)
emb3 = model.encode(phrase3)
emb4 = model.encode(phrase4)

# Compute similarities
print("water bottle vs bottle water:", util.cos_sim(emb1, emb2).item())
print("hot topic vs wet pizza:", util.cos_sim(emb3, emb4).item())