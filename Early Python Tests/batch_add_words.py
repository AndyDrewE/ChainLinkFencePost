seed = []

def load_pairs(file_path):
	with open(file_path, "r", encoding="utf-8") as f:
		return f.read().splitlines()

def save_pairs(file_path, pairs):
	with open(file_path, "w", encoding="utf-8") as f:
		f.write("\n".join(pairs) + "\n")


file_path = "two_word_phrases.txt"
lines = set(load_pairs(file_path))

for pair in seed:
	lines.add(pair)

lines = sorted(list(lines))
save_pairs(file_path, lines)
