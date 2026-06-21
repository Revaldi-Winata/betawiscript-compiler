import sys
import os

from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.semantic import SemanticAnalyzer
from src.optimizer import ASTOptimizer
from src.codegen import CodeGenerator

def compile_betawi(source_code: str, optimize: bool = True) -> str:
    # Fase 2: Lexical Analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Fase 3: Syntax Analysis
    parser = Parser(tokens)
    cst = parser.parse_program()

    # Fase 4: AST Construction
    builder = ASTBuilder()
    ast = builder.build(cst)

    # Fase 5: Semantic Analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # Fase 6: Code Optimization
    if optimize:
        optimizer = ASTOptimizer()
        ast = optimizer.optimize(ast)

    # Fase 7: Code Generation
    codegen = CodeGenerator()
    python_code = codegen.generate(ast)
    
    return python_code

def main():
    if len(sys.argv) < 3:
        print("Penggunaan:")
        print("  betawi jalan <file.betawi>   # Eksekusi langsung")
        print("  betawi rilis <file.betawi>   # Compile menjadi file .py")
        sys.exit(1)

    perintah = sys.argv[1]
    filepath = sys.argv[2]

    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' tidak ditemukan.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()

    try:
        python_code = compile_betawi(source_code)
        
        if perintah == 'jalan':
            # Execute directly in memory
            exec(python_code, {})
        elif perintah == 'rilis':
            # Save to .py file
            out_file = filepath.replace('.betawi', '.py')
            with open(out_file, 'w', encoding='utf-8') as out:
                out.write(python_code)
            print(f"Berhasil kompilasi! Tersimpan di: {out_file}")
        else:
            print(f"Perintah tidak dikenal: {perintah}")
            
    except Exception as e:
        print(f"Kompilasi Gagal: {e}")

if __name__ == '__main__':
    main()
