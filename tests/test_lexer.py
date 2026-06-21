import unittest
from src.lexer import Lexer, LexerError
from src.token import TokenType

class TestLexer(unittest.TestCase):
    def test_variable_assignment(self):
        source = 'x = 5'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(len(tokens), 4) # ID, =, NUMBER, EOF
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, 'x')
        self.assertEqual(tokens[1].type, TokenType.OPERATOR)
        self.assertEqual(tokens[1].value, '=')
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, '5')
        self.assertEqual(tokens[3].type, TokenType.EOF)

    def test_keywords_and_blocks(self):
        source = '''
        kalo (x > 5) {
            cetak("Gadang")
        }
        '''
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Expected tokens: 
        # kalo, (, x, >, 5, ), {, cetak, (, "Gadang", ), }, EOF
        expected_types = [
            TokenType.KEYWORD, TokenType.LPAREN, TokenType.IDENTIFIER,
            TokenType.OPERATOR, TokenType.NUMBER, TokenType.RPAREN,
            TokenType.LBRACE, TokenType.BUILTIN, TokenType.LPAREN,
            TokenType.STRING, TokenType.RPAREN, TokenType.RBRACE,
            TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for t, expected in zip(tokens, expected_types):
            self.assertEqual(t.type, expected)

    def test_illegal_character(self):
        source = 'x = 5 @ 3'
        lexer = Lexer(source)
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        
        self.assertIn("Karakter Ilegal '@'", str(context.exception))

if __name__ == '__main__':
    unittest.main()
