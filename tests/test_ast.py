import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder

class TestAST(unittest.TestCase):
    def test_ast_generation(self):
        source = '''
        kalo (x > 5) {
            cetak("Gede")
        } laennya {
            x = (2 + 3) * 5
        }
        '''
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        cst = parser.parse_program()
        
        print("\n==================== FASE 3: PARSE TREE (CST) ====================")
        print(cst.print_tree())
        
        builder = ASTBuilder()
        ast = builder.build(cst)
        
        print("\n==================== FASE 4: ABSTRACT SYNTAX TREE (AST) ====================")
        print(ast.print_ast())
        
        self.assertEqual(ast.__class__.__name__, "Program")
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].__class__.__name__, "IfStmt")
        
        # Verify then_branch
        if_node = ast.statements[0]
        self.assertEqual(len(if_node.then_branch), 1)
        self.assertEqual(if_node.then_branch[0].__class__.__name__, "FunctionCall")
        
        # Verify else_branch
        self.assertEqual(len(if_node.else_branch), 1)
        self.assertEqual(if_node.else_branch[0].__class__.__name__, "Assignment")

if __name__ == '__main__':
    unittest.main()
