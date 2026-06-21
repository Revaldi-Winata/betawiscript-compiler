import unittest
from src.lexer import Lexer
from src.parser import Parser, ParserError
from src.token import TokenType

class TestParser(unittest.TestCase):
    def test_assignment(self):
        source = 'x = 5'
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        tree = parser.parse_program()
        
        self.assertEqual(tree.name, "program")
        self.assertEqual(len(tree.children), 1)
        self.assertEqual(tree.children[0].name, "assignment_stmt")
        
        assign_node = tree.children[0]
        self.assertEqual(assign_node.children[0].value, 'x')
        self.assertEqual(assign_node.children[1].value, '=')
        # Since logic -> equality -> comparison -> term -> factor -> primary
        # Let's not strict assert deeply since the tree is nested.
        # Just ensure no exception.
        
        print("\n--- Parse Tree: Assignment ---")
        print(tree.print_tree())

    def test_complex_expression(self):
        source = 'x = (2 + 3) * 5'
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        tree = parser.parse_program()
        
        print("\n--- Parse Tree: Complex Math ---")
        print(tree.print_tree())

    def test_if_block(self):
        source = '''
        kalo (x > 5) {
            cetak("Gede")
        } laennya {
            cetak("Kecil")
        }
        '''
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        tree = parser.parse_program()
        
        self.assertEqual(tree.children[0].name, "if_stmt")
        print("\n--- Parse Tree: If Statement ---")
        print(tree.print_tree())
        
    def test_syntax_error(self):
        source = 'x = (5 + 3'
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        
        with self.assertRaises(ParserError):
            parser.parse_program()

if __name__ == '__main__':
    unittest.main()
