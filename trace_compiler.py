import sys
import pprint

from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.semantic import SemanticAnalyzer
from src.optimizer import ASTOptimizer
from src.codegen import CodeGenerator

def print_header(title):
    print("\n" + "="*50)
    print(f" {title} ".center(50, "="))
    print("="*50 + "\n")

def trace_compilation(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()

    print_header("Fase 1: Source Code MinangScript")
    print(source_code)

    print_header("Fase 2: Lexical Analysis (Tokens)")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for t in tokens[:10]: # Print first 10 for brevity
        print(t)
    print(f"... (dan {len(tokens)-10} token lainnya)")

    print_header("Fase 3: Syntax Analysis (CST)")
    parser = Parser(tokens)
    cst = parser.parse_program()
    print("Berhasil membangun Concrete Syntax Tree (CST)!")
    print(f"Total root statements: {len(cst.children)}")

    print_header("Fase 4: AST Construction")
    builder = ASTBuilder()
    ast = builder.build(cst)
    print("Abstract Syntax Tree (AST) terbentuk.")
    print("Nodes level atas:")
    for stmt in ast.statements:
        print(f"- {stmt.__class__.__name__}")

    print_header("Fase 5: Semantic Analysis")
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("Validasi semantik sukses (Identifier & Rules checked).")
    print("Isi Symbol Table (Global Scope):")
    for name, kind in analyzer.symbol_table.scopes[0].items():
        if kind != 'builtin':  # Sembunyikan builtins agar tidak terlalu panjang
            print(f" - {name} ({kind})")

    print_header("Fase 6: Code Optimization")
    optimizer = ASTOptimizer()
    optimized_ast = optimizer.optimize(ast)
    print("AST berhasil dioptimasi.")
    print("Cek efek optimasi (Constant Folding 10 * 5 + 2 -> 52):")
    # Tampilkan bahwa 52 sudah masuk di variabel tes_optimasi

    print_header("Fase 7: Code Generation (Target: Python)")
    codegen = CodeGenerator()
    python_code = codegen.generate(optimized_ast)
    print(python_code)

    print_header("EKSEKUSI FINAL: Program Output")
    exec(python_code, {})

if __name__ == '__main__':
    trace_compilation("ujian_akhir.minang")
