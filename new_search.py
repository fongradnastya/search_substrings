from collections import deque


class TreeItem:
    def __init__(self, value=None, next_states=None, fail_state=0, output=None):
        self.value = value
        if not next_states:
            self.next_states = []
        else:
            self.next_states = next_states
        self.fail_state = fail_state
        if not output:
            self.output = []
        else:
            self.output = output

    def add_next_state(self, state: int):
        self.next_states.append(state)

    def get_states(self):
        return self.next_states

    def add_output(self, keyword):
        self.output.append(keyword)

    def get_output(self):
        return self.output

    def set_output(self, output):
        self.output = output

    def set_fail_state(self, fail_state):
        self.fail_state = fail_state

    def get_fail_state(self):
        return self.fail_state


class Tree:
    def __init__(self):
        self.items = []
        item = TreeItem()
        self.items.append(item)

    def add_item(self, value, next_states=None, output=None, fail_state=0):
        item = TreeItem(value, next_states, fail_state, output)
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def get_item(self, item_id):
        return self.items[item_id]

    def add_keywords(self, keywords):
        """ add all keywords in list of keywords """
        for keyword in keywords:
            current_state = 0
            j = 0
            keyword = keyword.lower()
            child = self.find_next_state(current_state, keyword[j])
            while child:
                current_state = child
                j = j + 1
                if j < len(keyword):
                    child = self.find_next_state(current_state, keyword[j])
                else:
                    break
            for i in range(j, len(keyword)):
                self.add_item(keyword[i])
                self.items[current_state].add_next_state(len(self.items) - 1)
                current_state = len(self.items) - 1
            self.items[current_state].add_output(keyword)

    def set_fail_transitions(self):
        q = deque()
        for node in self.items[0].get_states():
            q.append(node)
            self.items[node].set_fail_state(0)
        while q:
            r = q.popleft()
            for child in self.items[r].get_states():
                q.append(child)
                state = self.items[r].get_fail_state()
                while (not self.find_next_state(state, self.items[child].value)) and state != 0:
                    state = self.items[state].get_fail_state()
                self.items[child].set_fail_state(self.find_next_state(state, self.items[child].value))
                if self.items[child].get_fail_state() is None:
                    self.items[child].set_fail_state(0)
                id_n = self.items[child].get_fail_state()
                output = self.items[child].get_output() + \
                         self.items[id_n].get_output()
                self.items[child].set_output(output)

    def find_next_state(self, current_state, value):
        for node in self.items[current_state].get_states():
            if self.items[node].value == value:
                return node
        return None


def get_keywords_found(line, keywords):
    """ returns true if line contains any keywords in trie """
    tree = Tree()
    tree.add_keywords(keywords)
    line = line.lower()
    current_state = 0
    keywords_found = []
    for i in range(len(line)):
        while tree.find_next_state(current_state, line[i]) is None \
                and current_state != 0:
            current_state = tree.get_item(current_state).get_fail_state()
        current_state = tree.find_next_state(current_state, line[i])
        if current_state is None:
            current_state = 0
        else:
            for j in tree.get_item(current_state).get_output():
                keywords_found.append({"index": i - len(j) + 1, "word": j})
    return keywords_found


print(get_keywords_found("casheweww", ['cash', 'shew', 'ew']))
