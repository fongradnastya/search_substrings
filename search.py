import time
from collections import deque


class TreeItem:
    """Элемент префиксного дерева"""
    def __init__(self, value=None, next_states=None, fail_state=0,
                 output=None):
        """
        Создание экземпляра элемента дерева
        :param value: значение текущего элемента
        :param next_states: следующие значения
        :param fail_state: связи для перехода при отсутствии следующего
        :param output: ключевые слова, которые можно получить в вершине
        """
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


class Tree:
    """Префиксное дерево"""
    def __init__(self):
        """
        Создание нового префиксного дерева
        """
        self._items = []
        item = TreeItem()
        self._items.append(item)

    def add_item(self, value: object, next_states: list = None,
                 output: list = None, fail_state: int = 0) -> None:
        """
        Добавление нового элемента к дереву
        :param value: значение текущего элемента
        :param next_states: следующие значения
        :param fail_state: связи для перехода при отсутствии следующего
        :param output: ключевые слова, которые можно получить в вершине
        """
        item = TreeItem(value, next_states, fail_state, output)
        self._items.append(item)

    def get_item(self, item_id: int) -> "TreeItem":
        """
        Получение элемента очереди по номеру
        :param item_id: номер искомого элемента
        :return: элемент префиксного дерева
        """
        return self._items[item_id]

    def add_keywords(self, keywords: tuple) -> None:
        """
        Добавление ключевых слов в дерево
        :param keywords: кортеж ключевых слов
        """
        for keyword in keywords:
            self.add_keyword(keyword)

    def add_keyword(self, keyword: str) -> None:
        """
        Добавление одного ключевого слова к дереву
        :param keyword: ключевое слово
        :return:
        """
        current_state = 0
        j = 0
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
            self._items[current_state].next_states.append(len(self._items) - 1)
            current_state = len(self._items) - 1
        self._items[current_state].output.append(keyword)

    def set_fail_transitions(self) -> None:
        """
        Установка перехода, используемого в случае отсутствия прямого пути по
        дереву
        """
        q = deque()
        for node in self._items[0].next_states:
            q.append(node)
            self._items[node].fail_state = 0
        while q:
            r = q.popleft()
            for child in self._items[r].next_states:
                q.append(child)
                state = self._items[r].fail_state
                while self.find_next_state(state, self._items[child].value) \
                        is None and state != 0:
                    state = self._items[state].fail_state
                self._items[child].fail_state = \
                    self.find_next_state(state, self._items[child].value)
                if self._items[child].fail_state is None:
                    self._items[child].fail_state = 0
                id_n = self._items[child].fail_state
                output = self._items[child].output + self._items[id_n].output
                self._items[child].output = output

    def find_next_state(self, current_state, value):
        """
        Ищет следующий элемент дерева
        :param current_state: текущий элемент
        :param value: значение искомого элемента
        :return:
        """
        for node in self._items[current_state].next_states:
            if self._items[node].value == value:
                return node
        return None

    def get_keywords_found(self, line):
        """
        Ищет ключевые слова в переданном тексте
        :param line: текст для поиска подстрок
        :return: массив найденных ключевых слов и их индексов
        """
        current_state = 0
        keywords_found = []
        if not line:
            return None
        for i in range(len(line)):
            while self.find_next_state(current_state, line[i]) is None and \
                    current_state != 0:
                current_state = self.get_item(current_state).fail_state
            current_state = self.find_next_state(current_state, line[i])
            if current_state is None:
                current_state = 0
            else:
                for j in self.get_item(current_state).output:
                    keywords_found.append((j, i - len(j) + 1))
        return keywords_found


def logger(func):
    """
    Логирует время рабыты функции и переданные ей аргументы
    :param func: функция для логирования времени
    :return:
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"Function {func.__name__} completed in {run_time:.9f} seconds.")
        print(f"Arguments: {args}, {kwargs}.")
        return res
    return wrapper


@logger
def search(string, sub_string, case_sensitivity=False, method='first',
           count=None):
    """
    Ищет в наборе строк ключевые слова
    :param string: строки для поиска
    :param sub_string: ключевые слова
    :param case_sensitivity: чувствительность поиска к регистру
    :param method: метод поиска ('first' или 'last')
    :param count: искомое число вхождений
    :return: Индексы найденных в тексте подстрок
    """
    tree = Tree()
    if not case_sensitivity:
        string = string.lower()
        if isinstance(sub_string, tuple):
            sub_string = list(sub_string)
            for i in range(len(sub_string)):
                sub_string[i] = sub_string[i].lower()
            sub_string = tuple(sub_string)
        else:
            sub_string = sub_string.lower()
    if isinstance(sub_string, tuple):
        tree.add_keywords(sub_string)
    else:
        tree.add_keyword(sub_string)
    tree.set_fail_transitions()
    items = tree.get_keywords_found(string)
    if items:
        if method == 'last':
            items = items[::-1]
        if count and len(items) > count:
            items = items[:count]
    else:
        return None
    if not isinstance(sub_string, tuple):
        t = []
        for i in items:
            t.append(i[1])
        return tuple(t)
    else:
        found = dict()
        for string in sub_string:
            found[string] = []
        for i in items:
            found[i[0]].append(i[1])
        for key, value in found.items():
            if not value:
                found[key] = None
            else:
                found[key] = tuple(value)
        return found
