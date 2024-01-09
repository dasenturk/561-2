from src.cfg import CFG
from src.grammar_converter import CFGtoCNFConverter
from src.cky_parser import CKYParser


if __name__ == '__main__':
    cfg = CFG()
    cfg.set_start_symbol('S')

    # Add terminals and non-terminals
    cfg.add_terminal('arkadaşıma')
    cfg.add_nonterminal('SUBP')
    cfg.add_nonterminal('DESP')

    # Add rules
    cfg.add_rule('S', ['SUBP', 'DESP', 'PRED'])
    cfg.add_rules_from_string('S → SUBP+NOBJP+PRED, S → SUBP+DESP+NOBJP')

    # Load rules from a file
    cfg.add_rules_from_file('data/grammar_rules.txt')
    print(cfg.rules.items())

      # Assuming cfg is already populated with rules
    converter = CFGtoCNFConverter(cfg)
    cnf = converter.convert()

    cky_parser = CKYParser(cnf)  # Assuming the parser is already initialized
    sentence = "Ben hediye aldım"
    cky_parser.parse(sentence)
    cky_parser.print_parse_table()

    print(cfg)


