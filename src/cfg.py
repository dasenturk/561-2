import os


class CFG:
    def __init__(self):
        self.start_symbol = None   # Start symbol of the CFG
        self.rules = {}                    # key: LHS, value: list of lists of RHS
        self.lexicon = {}                  # key: word, value: properties (part of speech, etc.)
        self.terminals = set()             # Set of terminal symbols
        self.nonterminals = set()

    def set_start_symbol(self, symbol):
        self.start_symbol = symbol

    # Set of non-terminal symbols
    def add_rule(self, lhs, rhs):
        """ Add a CFG rule. """
        # Handle non-terminal symbols
        self.nonterminals.add(lhs)

        # Process RHS symbols
        for symbol in rhs:
            if symbol.isupper():
                self.nonterminals.add(symbol)
            else:
                self.terminals.add(symbol)

        # Add rule to grammar
        if lhs in self.rules:
            self.rules[lhs].append(rhs)
        else:
            self.rules[lhs] = [rhs]

    def add_rules_from_string(self, rule_string):
        """ Add multiple CFG rules from a string. """
        for rule in rule_string.split(','):
            parts = rule.split('→')
            lhs = parts[0].strip()
            rhs = parts[1].split('+')
            self.add_rule(lhs, rhs)

    def add_rules_from_file(self, file_path):
        """ Add multiple CFG rules from a file. """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Ensure the line is not empty
                    parts = line.split('→')
                    lhs = parts[0].strip()
                    rhs = [symbol.strip() for symbol in parts[1].split('+')]
                    self.add_rule(lhs, rhs)

    def add_lexicon_entry(self, word, properties):
        """ Add an entry to the lexicon with properties. """
        self.lexicon[word] = properties
        self.terminals.add(word)

    def get_rhs(self, lhs):
        """ Returns the RHS for a given LHS symbol. """
        return self.rules.get(lhs, [])

    def get_properties(self, word):
        """ Returns the properties of a given word. """
        return self.lexicon.get(word, None)

    def add_terminal(self, terminal):
        self.terminals.add(terminal)

    def add_nonterminal(self, non_terminal):
        self.nonterminals.add(non_terminal)
