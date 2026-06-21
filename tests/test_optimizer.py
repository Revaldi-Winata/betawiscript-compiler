import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.optimizer import ASTOptimizer
from src.ast_nodes import *

class TestOptimizer(unittest.TestCase):
    def setUp(self):
        self.builder = ASTBuilder()
        self.optimizer = ASTOptimizer()

    def get_optimized_ast(self, source_code):
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        cst = parser.parse_program()
        ast = self.builder.build(cst)
        return self.optimizer.optimize(ast)

    def test_constant_folding_math(self):
        code = "x = 5 + 10 * 2"
        ast = self.get_optimized_ast(code)
        
        assignment = ast.statements[0]
        self.assertIsInstance(assignment, Assignment)
        # Should be completely folded to Literal(25)
        self.assertIsInstance(assignment.value, Literal)
        self.assertEqual(assignment.value.value, 25)

    def test_constant_folding_logical(self):
        code = "hasil = bukan Kaga atawa Bener"
        ast = self.get_optimized_ast(code)
        
        assignment = ast.statements[0]
        self.assertIsInstance(assignment.value, Literal)
        self.assertEqual(assignment.value.value, True)

    def test_dead_code_elimination_return(self):
        code = """
        bikin tes() {
            balikin 100
            cetak("Halo")
            x = 5
        }
        """
        ast = self.get_optimized_ast(code)
        function_def = ast.statements[0]
        
        # The body should only contain the return statement
        self.assertEqual(len(function_def.body), 1)
        self.assertIsInstance(function_def.body[0], ReturnStmt)

    def test_dead_code_elimination_break(self):
        code = """
        selagi (Bener) {
            berenti
            x = 5
        }
        """
        ast = self.get_optimized_ast(code)
        while_stmt = ast.statements[0]
        
        # Body should only contain break
        self.assertEqual(len(while_stmt.body), 1)
        self.assertIsInstance(while_stmt.body[0], BreakStmt)

    def test_dead_code_elimination_if_false(self):
        code = """
        kalo (Kaga) {
            cetak("Ini tidak muncul")
        } laennya {
            cetak("Ini muncul")
        }
        """
        ast = self.get_optimized_ast(code)
        if_stmt = ast.statements[0]
        
        # Condition should be optimized to Literal(True) and then_branch should hold the else block
        self.assertIsInstance(if_stmt.condition, Literal)
        self.assertEqual(if_stmt.condition.value, True)
        self.assertIsInstance(if_stmt.then_branch[0], FunctionCall)
        self.assertEqual(if_stmt.else_branch, None)
        
    def test_dead_code_elimination_while_false(self):
        code = """
        selagi (Kaga) {
            cetak("Loop tidak jalan")
        }
        x = 5
        """
        ast = self.get_optimized_ast(code)
        
        # The While loop should be completely deleted, leaving only assignment x = 5
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], Assignment)

if __name__ == '__main__':
    unittest.main()
