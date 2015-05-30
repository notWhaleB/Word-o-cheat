# Python 3.4

from http import server
from urllib.parse import unquote

UnicodeRuMinOrd = 1072
UnicodeRuMaxOrd = 1105
UnicodeRuRange = UnicodeRuMaxOrd - UnicodeRuMinOrd + 1


def zip_ord(char):
    return ord(char) - UnicodeRuMinOrd


class TrieNode:
    def __init__(self):
        self.child = [0] * UnicodeRuRange
        self.leaf = False

    def add_child(self, node_id):
        self.child.append(node_id)

    def is_leaf(self):
        return self.leaf


class Trie:
    def __init__(self):
        self._data = []
        self._data.append(TrieNode())

    def add_new_node(self):
        self._data.append(TrieNode())
        return len(self._data) - 1

    def add_word(self, word):
        current_node_id = 0
        for sym in word:
            if self._data[current_node_id].child[zip_ord(sym)] != 0:
                current_node_id = self._data[current_node_id].child[zip_ord(sym)]
            else:
                self._data[current_node_id].child[zip_ord(sym)] = self.add_new_node()
                current_node_id = self._data[current_node_id].child[zip_ord(sym)]
        self._data[current_node_id].leaf = True

    def get_node(self, node_id):
        return self._data[node_id]


def dfs_for_line(dictionary, current_id, letter_line, word, result):
    for idx, sym in enumerate(letter_line):
        next_node_id = dictionary.get_node(current_id).child[zip_ord(sym)]
        if next_node_id != 0:
            dfs_for_line(dictionary, next_node_id, letter_line[:idx] + letter_line[idx + 1:], word + sym, result)
    if dictionary.get_node(current_id).is_leaf():
        result.add(word)


def get_words_in_line(dictionary, letter_line):
    result = set()
    dfs_for_line(dictionary, 0, letter_line, "", result)

    return result


trie_dictionary = Trie()

print("Dictionary loading...")
with open("dictionary.txt") as file:
    lines = file.readlines()
    size = len(lines)
    for idx, line in enumerate(lines):
        trie_dictionary.add_word(line.strip().lower())
        if idx % 10000 == 0:
            print(int((idx / size) * 100), '%')
print("Dictionary loaded.")


class HttpProcessor(server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        _output = '{"data": ['
        _answer = list(get_words_in_line(trie_dictionary, unquote(self.path[2:18]).lower()))
        _answer = sorted(_answer, key=lambda _word: len(_word), reverse=True)[:16]

        for idx, _word in enumerate(_answer):
            if _word:
                _output += '"' + _word + '"'
                if idx != len(_answer) - 1:
                    _output += ","
        _output += "]}"
        self.wfile.write(bytes(_output, "UTF-8"))

web_server = server.HTTPServer(("localhost", 80), HttpProcessor)  # Put ip instead of localhost for external access
web_server.serve_forever()
