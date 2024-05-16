import re
import collections


def load_dictionary():

    file_path = 'words.txt'
    dictionary = []

    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()  # Strip leading/trailing whitespace
            if len(word) > 2:  # Charlottery only accepts words longer than 2 letters
                dictionary.append(word.lower())
    return dictionary


def find_words_by_length(letters, dictionary):

    lengths = {}

    for i in range(1, len(letters) + 1):

        pattern = ".*".join(letters[0:i])  # This makes a regex pattern like the following: a.*b.*c
        if i < len(letters) - 1:
            pattern = pattern + f"(?!.*{letters[i]})"
        regex = re.compile(pattern)

        word_not_found = True
        for word in dictionary:
            if regex.match(word):
                word_not_found = False
                lengths[i] = word
                break

        if word_not_found:  # if we can't find a word, we won't be able to find more with more letters
            break

    return lengths


class Node:

    def __init__(self, starting_index, word):
        self.starting_index = starting_index
        self.word = word
        self.children = []
        self.path = []


def solve(letters):

    dictionary = load_dictionary()

    root = Node(0, None)

    q = collections.deque()
    q.append(root)

    visited = set()

    while q:

        for _ in range(len(q)):

            parent = q.popleft()
            lengths = find_words_by_length(letters[parent.starting_index:], dictionary)

            i = 0
            for length, word in lengths.items():

                new_starting_index = parent.starting_index + length

                if new_starting_index not in visited:
                    node = Node(new_starting_index, word)
                    node.path = parent.path + [i]
                    parent.children.append(node)
                    q.append(node)
                    visited.add(new_starting_index)
                    i += 1

                if new_starting_index == len(letters):
                    return root, node.path

# method to print out tree
def level_order_traversal(node):

    q = collections.deque()
    q.append(node)
    level = 0
    while q:
        s = f"Level {level}: "
        for _ in range(len(q)):
            node = q.popleft()
            print(node.word, node.starting_index)

            for child in node.children:
                q.append(child)
        level += 1

#level_order_traversal(root)


letters = "sgfbvwudkiltapzyeoqxnchjrm"
#letters = "wskypeirvtmaouhqclngfjbzdx"
tree, path = solve(letters)
root = tree

print("Solving:", letters)
print("Path:", path)
for i in path:
    start = tree.starting_index
    tree = tree.children[i]
    end = tree.starting_index
    print(tree.word, tree.starting_index, letters[start:end])

print("Number of words:", len(path))


























