import time


class WordReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.words_list = []

    def read_file(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            contents = file.read()
            self.words_list = contents.split()

    def get_next_word(self):
        if not self.words_list:
            return None

        return self.words_list.pop(0)

    def get_words_left(self):
        return len(self.words_list)

    def print_words(self):
        while self.words_list:
            word = self.get_next_word()
            print(word)
            time.sleep(1)


def main():
    file_path = "path/to/your/file.txt"
    reader = WordReader(file_path)
    reader.read_file()
    reader.print_words()


if __name__ == "__main__":
    main()
