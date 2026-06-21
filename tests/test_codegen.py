import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.optimizer import ASTOptimizer
from src.codegen import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.builder = ASTBuilder()
        self.optimizer = ASTOptimizer()
        self.codegen = CodeGenerator()

    def get_generated_code(self, source_code):
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        cst = parser.parse_program()
        ast = self.builder.build(cst)
        optimized_ast = self.optimizer.optimize(ast)
        return self.codegen.generate(optimized_ast)

    def test_basic_translation(self):
        code = """
        x = 5 + 5
        cetak(x)
        """
        python_code = self.get_generated_code(code)
        expected = "x = 10\nprint(x)\n"
        self.assertEqual(python_code.strip(), expected.strip())

    def test_if_translation(self):
        # We use variables instead of static false so optimizer doesn't remove it
        code = """
        kalo (x == Bener) {
            cetak("Ya")
        } laennya {
            cetak("Tidak")
        }
        """
        python_code = self.get_generated_code(code)
        expected = "if (x == True):\n    print(\"Ya\")\nelse:\n    print(\"Tidak\")"
        self.assertEqual(python_code.strip(), expected.strip())

    def test_class_translation(self):
        code = """
        kelas Hewan {
            bikin test(gue, nama) {
                cetak(nama)
            }
        }
        """
        python_code = self.get_generated_code(code)
        expected = "class Hewan:\n    def test(self, nama):\n        print(nama)"
        self.assertEqual(python_code.strip(), expected.strip())

    def test_async_translation(self):
        code = """
        barengan bikin tes() {
            tungguin sleep(1)
        }
        """
        python_code = self.get_generated_code(code)
        expected = "async def tes():\n    await sleep(1)"
        self.assertEqual(python_code.strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()
