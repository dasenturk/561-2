from itertools import combinations
from src.cfg import CFG


class CFGtoCNFConverter:
    def __init__(self, cfg):
        self.cfg = cfg
        self.cnf = CFG()  # Assuming CFG is the class defined previously

    def convert(self):
        self.eliminate_start_symbol_from_rhs()
        self.remove_null_productions()
        self.remove_unit_productions()
        self.remove_long_productions()
        self.move_terminals_to_separate_rules()
        return self.cnf

    def eliminate_start_symbol_from_rhs(self):
        # Create a new start symbol and rule to prevent the original start symbol from appearing on RHS
        new_start_symbol = 'S0'
        self.cnf.set_start_symbol(new_start_symbol)
        self.cnf.add_rule(f'{new_start_symbol}', [f'{self.cfg.start_symbol}'])

    def remove_null_productions(self):
        nullables = self.find_nullables()
        new_rules = {}

        # Iterate over all rules
        for lhs, rhs_list in self.cfg.rules.items():
            new_rhs_list = []
            for rhs in rhs_list:
            # If the rule is a nullable production, skip it
                if rhs == ['ε']:
                    continue

            # Find all nullable symbols in the RHS
                nullable_positions = [pos for pos, symbol in enumerate(rhs) if symbol in nullables]

            # Generate all combinations of nullable symbols being present or absent
                for count in range(1, len(nullable_positions) + 1):
                    for positions in combinations(nullable_positions, count):
                        new_rhs = [symbol for pos, symbol in enumerate(rhs) if pos not in positions]
                        new_rhs_list.append(new_rhs)

            # Add the original rule as well
                new_rhs_list.append(rhs)
            new_rules[lhs] = new_rhs_list

        # Update the CFG rules
        self.cfg.rules = new_rules

    def find_nullables(self):
        # Find all non-terminals that can produce ε directly or indirectly
        nullables = set()

        # Direct ε-productions
        for lhs, rhs_list in self.cfg.rules.items():
            for rhs in rhs_list:
                if rhs == ['ε']:
                    nullables.add(lhs)

        # Indirect ε-productions
        changes = True
        while changes:
            changes = False
            for lhs, rhs_list in self.cfg.rules.items():
                for rhs in rhs_list:
                    if all(symbol in nullables for symbol in rhs) and lhs not in nullables:
                        nullables.add(lhs)
                        changes = True

        return nullables

    def remove_unit_productions(self):
        # A dictionary to keep track of unit pairs (A, B) where A -> B
        unit_pairs = self.find_unit_pairs()

        # Now for each unit pair (A, B), add all rules of B to A
        new_rules = {lhs: list(rhs_list) for lhs, rhs_list in self.cfg.rules.items()}  # Start with all existing rules
        for A, B in unit_pairs:
            for rhs in self.cfg.rules.get(B, []):
                if [B] != rhs:  # Avoid adding the unit production itself
                    new_rules[A].append(rhs)

        # Update the CFG rules
        self.cfg.rules = new_rules

    def find_unit_pairs(self):
        unit_pairs = set()

        # Direct unit productions
        for lhs, rhs_list in self.cfg.rules.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] in self.cfg.nonterminals:
                    unit_pairs.add((lhs, rhs[0]))

        # Transitive closure of unit productions
        changes = True
        while changes:
            changes = False
            for A, B in list(unit_pairs):
                for C, D in list(unit_pairs):
                    if B == C and (A, D) not in unit_pairs:
                        unit_pairs.add((A, D))
                        changes = True

        return unit_pairs

    def remove_long_productions(self):
        new_rules = {}

        for lhs, rhs_list in self.cfg.rules.items():
            new_rhs_list = []
            for rhs in rhs_list:
                # Skip rules that are already in CNF
                if len(rhs) == 2 and all(symbol in self.cfg.nonterminals for symbol in rhs):
                    new_rhs_list.append(rhs)
                elif len(rhs) == 1 and rhs[0] in self.cfg.terminals:
                    new_rhs_list.append(rhs)
                else:
                    # Break down longer productions
                    new_rhs = self.break_down_rhs(rhs)
                    for sub_rhs in new_rhs:
                        new_rhs_list.append(sub_rhs)

            new_rules[lhs] = new_rhs_list

        # Update the CFG rules
        self.cfg.rules = new_rules

    def break_down_rhs(self, rhs):
        # This method breaks down right-hand sides longer than 2 symbols
        new_rhs = []
        while len(rhs) > 2:
            # Create a new non-terminal
            new_nonterminal = self.generate_new_nonterminal()
            new_rhs.append((new_nonterminal, rhs[-2:]))
            rhs = rhs[:-2] + [new_nonterminal]

        new_rhs.append(rhs)
        return new_rhs

    def generate_new_nonterminal(self):
        # Generate a new non-terminal symbol that doesn't already exist in the grammar
        new_nonterminal = f"X{len(self.cfg.nonterminals)}"
        while new_nonterminal in self.cfg.nonterminals:
            new_nonterminal = f"X{len(self.cfg.nonterminals) + 1}"
        self.cfg.nonterminals.add(new_nonterminal)
        return new_nonterminal

    def move_terminals_to_separate_rules(self):
        new_rules = {}
        terminal_mappings = {}  # To store new non-terminals for terminals

        for lhs, rhs_list in self.cfg.rules.items():
            new_rhs_list = []
            for rhs in rhs_list:
                if len(rhs) == 1:
                    new_rhs_list.append(rhs)
                else:
                    new_rhs = []
                    for symbol in rhs:
                        if symbol in self.cfg.terminals:
                            # If it's a terminal, replace it with a corresponding non-terminal
                            if symbol not in terminal_mappings:
                                # Create a new non-terminal for this terminal
                                new_nonterminal = self.generate_new_nonterminal()
                                terminal_mappings[symbol] = new_nonterminal
                                self.cfg.nonterminals.add(new_nonterminal)
                                new_rules.setdefault(new_nonterminal, []).append([symbol])
                            new_rhs.append(terminal_mappings[symbol])
                        else:
                            new_rhs.append(symbol)
                    new_rhs_list.append(new_rhs)

            new_rules[lhs] = new_rhs_list

        # Update the CFG rules
        self.cfg.rules = new_rules


