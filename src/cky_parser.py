import json

class CKYParser:
    def __init__(self, grammar):
        self.grammar = grammar  # CNF grammar
        self.lexicon = self.load_lexicon()  # Dictionary of word: POS
        self.table = None

    @staticmethod
    def load_lexicon():
        with open('data/lexicon.json', 'rb') as handle:
            lexicon = json.load(handle)
        return lexicon

    def parse(self, sentence):
        words = sentence.split()
        n = len(words)

        # Initialize the parse table
        self.table = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

        # Fill in the table for single words (lexical rules)
        for i, word in enumerate(words):
            if word not in self.lexicon:
                print(f"Unknown word: {word}")
                return False
            for pos in self.lexicon[word]:
                self.table[i][i + 1].add(pos)

        # Fill in the table for phrases and sentences
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length
                for k in range(i + 1, j):
                    for A in self.grammar.nonterminals:
                        for B, C in self.grammar.rules:
                            if B in self.table[i][k] and C in self.table[k][j]:
                                self.table[i][j].add(A)

        # Check if the start symbol covers the entire sentence
        return self.grammar.start_symbol in self.table[0][n]

    def is_grammatically_correct(self, sentence):
        if not self.parse(sentence):
            return False

        words = sentence.split()
        n = len(words)

        # Verb agreement and other grammatical checks
        for i in range(n - 1):
            current_word, next_word = words[i], words[i + 1]
            current_pos = self.lexicon.get(current_word, set())
            next_pos = self.lexicon.get(next_word, set())

            # Example check: if current word is a subject (Noun), check if next word is a correctly agreeing verb
            if 'Noun' in current_pos and not self.verb_agrees_with_subject(current_word, next_word):
                return False

        return True

    def verb_agrees_with_subject(self, subject, verb):
        # This method checks if the verb agrees with the subject in terms of person and number.
        # Example implementation for a simplified case

        # Assuming subject and verb are provided in a format like "word+feature1+feature2"
        # For instance, "köpek+3rd+singular" for a singular third-person subject (the dog)

        subject_features = self.extract_features(subject)
        verb_features = self.extract_features(verb)

        # Check for agreement in person and number
        if subject_features["person"] != verb_features["person"]:
            return False
        if subject_features["number"] != verb_features["number"]:
            return False

        # Add more checks if needed for tense or other grammatical aspects

        return True

    def extract_features(self, word):
        # This method extracts grammatical features from the word.
        # This is a placeholder function and should be implemented to suit the specifics of the language's grammar.
        parts = word.split('+')
        features = {}
        if len(parts) > 1:
            for feature in parts[1:]:
                key, value = feature.split('=')
                features[key] = value
        return features

    def print_parse_table(self):
        if self.table is None:
            print("No parse table available. Please run the parser first.")
            return

        n = len(self.table)
        for row in range(n):
            for col in range(n):
                if col < row:
                    print("\t", end="")  # Fill lower triangular part with tabs
                else:
                    cell = self.table[row][col]
                    cell_str = "{" + ", ".join(cell) + "}" if cell else "{}"
                    print(f"{cell_str}\t", end="")
            print()




