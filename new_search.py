from collections import deque

AdjList = []


class TreeItem:
    def __init__(self):
        self.value = None
        self.next_states = []
        self.fail_state = 0
        self.output = []


class Tree:
    def __init__(self):
        self.items = []
        item = TreeItem()
        self.items.append(item)

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
                node = {'value': keyword[i], 'next_states': [],
                        'fail_state': 0,
                        'output': []}
                AdjList.append(node)
                AdjList[current_state]["next_states"].append(len(AdjList) - 1)
                current_state = len(AdjList) - 1
            AdjList[current_state]["output"].append(keyword)

    def set_fail_transitions(self):
        q = deque()
        child = 0
        for node in AdjList[0]["next_states"]:
            q.append(node)
            AdjList[node]["fail_state"] = 0
        while q:
            r = q.popleft()
            for child in AdjList[r]["next_states"]:
                q.append(child)
                state = AdjList[r]["fail_state"]
                while (not self.find_next_state(
                        state, AdjList[child]["value"])) and state != 0:
                    state = AdjList[state]["fail_state"]
                AdjList[child]["fail_state"] = \
                    self.find_next_state(state, AdjList[child]["value"])
                if AdjList[child]["fail_state"] is None:
                    AdjList[child]["fail_state"] = 0
                AdjList[child]["output"] = \
                    AdjList[child]["output"] + \
                    AdjList[AdjList[child]["fail_state"]]["output"]

    def find_next_state(self, current_state, value):
        for node in AdjList[current_state]["next_states"]:
            if AdjList[node]["value"] == value:
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
            current_state = AdjList[current_state]["fail_state"]
        current_state = tree.find_next_state(current_state, line[i])
        if current_state is None:
            current_state = 0
        else:
            for j in AdjList[current_state]["output"]:
                keywords_found.append({"index": i - len(j) + 1, "word": j})
    return keywords_found


print(get_keywords_found("casheweww"))
