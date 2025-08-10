

def load_pairs(file_path):
	with open(file_path, "r", encoding="utf-8") as f:
		return f.read().splitlines()

def save_pairs(file_path, pairs):
	with open(file_path, "w", encoding="utf-8") as f:
		f.write("\n".join(pairs) + "\n")

def prompt_action():
	return input("Choose action - [r]emove, [a]dd new pair, [c]ontinue, [q]uit: ").strip().lower()

def main():
	file_path = "two_word_phrases.txt"
	lines = load_pairs(file_path)
	kept_pairs = []
	added_pairs = []
	index = 0
	while index < len(lines):
		line = lines[index]
		print(f"Current pair: {line}")
		action = prompt_action()
		if action == 'r':
			print("Pair removed.")
			index += 1
		elif action == 'a':
			new_pair = input("Enter new pair to add: ").strip()
			# Check for duplicates in all current and added pairs
			all_pairs = set(kept_pairs + added_pairs + lines[index:])
			if new_pair:
				if new_pair in all_pairs:
					print(f"Duplicate detected: '{new_pair}' is already in the list. Not added.")
					# Stay on the same line to allow further action
				else:
					added_pairs.append(new_pair)
					print(f"Added: {new_pair}")
			# Stay on the same line to allow further action
		elif action == 'c':
			kept_pairs.append(line)
			index += 1
		elif action == 'q':
			print("Quitting early.")
			# Add all remaining lines to kept_pairs
			kept_pairs.extend(lines[index:])
			break
		else:
			print("Invalid input. Please enter 'r', 'a', 'c', or 'q'.")
	final_pairs = kept_pairs + added_pairs
	# Sort the final pairs alphabetically
	final_pairs = sorted(final_pairs)
	# Save the final pairs to the file
	save_pairs(file_path, final_pairs)
	print(f"Done. Output written to {file_path}")

if __name__ == "__main__":
	main()
