import nltk
import re
from SymbolTable import SymbolTable
from FA import FiniteAutomata, read_FA_file

class Token:
    def __init__(self, token, line_nr):
        self._token = token
        self._line_nr = line_nr

    def get_token(self):
        return self._token

    def get_line_nr(self):
        return self._line_nr

    def set_token(self, new_token):
        self._token = new_token


def write_to_file(file_name, list):
    textfile = open(file_name, "w")
    for element in list:
        textfile.write(str(element) + "\n")
    textfile.close()

def check_tokens_from_file(file_name):
    identifier_symbol_tale = SymbolTable()
    constant_symbol_tale = SymbolTable()
    tokens = open('token.in')
    tokens = tokens.read()
    PIF = []
    identifier_regex = '^_?[a-zA-Z]+[a-zA-Z0-9_]*$'
    integer_regex = '0|^[1-9]+[0-9]*$'
    rational_regex = '^([1-9]+[0-9]*|0)(\.[0-9]*)+$'
    token_list = []
    line_nr = 1
    FA_integer_file = 'FA_integer.in'
    FA_identifier_file = 'FA_identifier.in'
    FA_integer = read_FA_file(FA_integer_file)
    FA_identifier = read_FA_file(FA_identifier_file)
    with open(file_name) as f:
        for line in f:
            for token in nltk.tokenize.word_tokenize(line):
                token_list = token_list + [Token(token, line_nr)]
            line_nr += 1

    for index in range(len(token_list)):
        if not token_list[index].get_token():
            continue
        if re.search('\n'+re.escape(token_list[index].get_token()) + '\n', tokens):
            # check if not identifier or constant
            PIF.append([token_list[index].get_token(), -1])

        # elif re.search(identifier_regex, token_list[index].get_token()):
        elif FA_identifier.checkSequence(token_list[index].get_token()):
            # check if identifier
            PIF.append(['identifier', identifier_symbol_tale.add(token_list[index].get_token())])
        # elif re.search(integer_regex, token_list[index].get_token()):
        elif FA_integer.checkSequence(token_list[index].get_token()):
            # check if integer
            PIF.append(['constant', constant_symbol_tale.add(token_list[index].get_token())])
        elif re.search(rational_regex, token_list[index].get_token()):
            # check if rational
            PIF.append(['constant', constant_symbol_tale.add(token_list[index].get_token())])
        elif re.search('^\'[^\']*$', token_list[index].get_token()):
            # check if string
            look_ahead_index = index + 1
            while look_ahead_index < len(token_list) and re.search('^[^\']*$', token_list[look_ahead_index].get_token()):
                token_list[index].set_token(token_list[index].get_token() + ' ' + token_list[look_ahead_index].get_token())
                token_list[look_ahead_index].set_token(None)
                look_ahead_index += 1
            if look_ahead_index < len(token_list) and token_list[look_ahead_index].get_token() == "'":
                token_list[index].set_token(token_list[index].get_token() + token_list[look_ahead_index].get_token())
                token_list[look_ahead_index].set_token(None)
                PIF.append(['constant', constant_symbol_tale.add(token_list[index].get_token())])
            else:
                print('unexpected EOF, expected "\'" ; error line: ', token_list[index].get_line_nr())
                return None, None, None
        else:
            print('lexical error - invalid token, line:', token_list[index].get_line_nr(), ' ; token:', token_list[index].get_token())
            return None, None, None
    print('lexically correct')
    # write_to_file('PIF.out', PIF)
    # write_to_file('IST.out', ['symbol table represented as tree\ninorder traversal:\n'] + identifier_symbol_tale.inorder_traversal())
    # write_to_file('CST.out', ['symbol table represented as tree\ninorder traversal:\n'] + constant_symbol_tale.inorder_traversal())
    return PIF, identifier_symbol_tale, constant_symbol_tale

PIF, identifier_symbol_tale, constant_symbol_tale = check_tokens_from_file('p1.txt')

print(PIF)
print(identifier_symbol_tale)
print(constant_symbol_tale)