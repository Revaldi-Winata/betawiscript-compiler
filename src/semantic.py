from typing import List, Dict, Optional, Set
from src.ast_nodes import *

class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        # List of scopes. Index 0 is global scope.
        self.scopes: List[Dict[str, str]] = [{}]
        
        # Initialize global scope with some built-ins for demonstration
        builtins = [
            'cetak', 'panjang', 'himpunan', 'mutlak', 'Error', 
            'baca', 'bukak', 'sleep', 'daftar', 'tipe', 'masuakan',
            'angka', 'kato', 'desimal', 'rentang'
        ]
        for b in builtins:
            self.declare(b, 'builtin')

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Cannot pop global scope")

    def declare(self, name: str, symbol_type: str = 'variable'):
        # Declare in the current scope
        self.scopes[-1][name] = symbol_type

    def lookup(self, name: str) -> bool:
        # Search from innermost scope to global
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.loop_depth = 0

    def analyze(self, node: ASTNode):
        method_name = f"visit_{node.__class__.__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node: ASTNode):
        for key, value in node.__dict__.items():
            if isinstance(value, ASTNode):
                self.analyze(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self.analyze(item)
                    elif isinstance(item, tuple):
                        for sub_item in item:
                            if isinstance(sub_item, ASTNode):
                                self.analyze(sub_item)
                            elif isinstance(sub_item, list):
                                for x in sub_item:
                                    if isinstance(x, ASTNode):
                                        self.analyze(x)

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.analyze(stmt)

    def visit_Assignment(self, node: Assignment):
        # Analyze value first (RHS)
        self.analyze(node.value)
        # Declare target (LHS)
        self.symbol_table.declare(node.target.name)

    def visit_Identifier(self, node: Identifier):
        if node.name in ['gue', 'emak']:
            return # Special keywords for class scope
            
        if not self.symbol_table.lookup(node.name):
            raise SemanticError(f"Variabel atau fungsi '{node.name}' belum dideklarasikan.")

    def visit_FunctionDef(self, node: FunctionDef):
        # Function name is declared in the current scope
        self.symbol_table.declare(node.name.name, 'function')
        
        self.symbol_table.push_scope()
        # Declare parameters in the new scope
        for param in node.params:
            self.symbol_table.declare(param.name, 'parameter')
            
        for stmt in node.body:
            self.analyze(stmt)
            
        self.symbol_table.pop_scope()

    def visit_ClassDef(self, node: ClassDef):
        self.symbol_table.declare(node.name.name, 'class')
        if node.parent:
            self.analyze(node.parent)
            
        self.symbol_table.push_scope()
        for stmt in node.body:
            self.analyze(stmt)
        self.symbol_table.pop_scope()

    def visit_IfStmt(self, node: IfStmt):
        self.analyze(node.condition)
        
        self.symbol_table.push_scope()
        for stmt in node.then_branch:
            self.analyze(stmt)
        self.symbol_table.pop_scope()
        
        for condition, body in node.elif_branches:
            self.analyze(condition)
            self.symbol_table.push_scope()
            for stmt in body:
                self.analyze(stmt)
            self.symbol_table.pop_scope()
            
        if node.else_branch:
            self.symbol_table.push_scope()
            for stmt in node.else_branch:
                self.analyze(stmt)
            self.symbol_table.pop_scope()

    def visit_WhileStmt(self, node: WhileStmt):
        self.analyze(node.condition)
        self.loop_depth += 1
        self.symbol_table.push_scope()
        
        for stmt in node.body:
            self.analyze(stmt)
            
        self.symbol_table.pop_scope()
        self.loop_depth -= 1

    def visit_ForStmt(self, node: ForStmt):
        self.analyze(node.iterable)
        self.loop_depth += 1
        self.symbol_table.push_scope()
        
        self.symbol_table.declare(node.iterator.name, 'iterator')
        
        for stmt in node.body:
            self.analyze(stmt)
            
        self.symbol_table.pop_scope()
        self.loop_depth -= 1

    def visit_BreakStmt(self, node: BreakStmt):
        if self.loop_depth == 0:
            raise SemanticError("Sintaks 'berenti' (break) berada di luar perulangan.")

    def visit_ContinueStmt(self, node: ContinueStmt):
        if self.loop_depth == 0:
            raise SemanticError("Sintaks 'terusin' (continue) berada di luar perulangan.")

    def visit_FunctionCall(self, node: FunctionCall):
        self.analyze(node.name)
        for arg in node.args:
            self.analyze(arg)

    def visit_ImportStmt(self, node: ImportStmt):
        if node.alias:
            self.symbol_table.declare(node.alias.name, 'module')
        else:
            self.symbol_table.declare(node.module.name, 'module')

    def visit_FromImportStmt(self, node: FromImportStmt):
        self.symbol_table.declare(node.name.name, 'module_member')

    def visit_WithStmt(self, node: WithStmt):
        self.analyze(node.expression)
        self.symbol_table.push_scope()
        if node.alias:
            self.symbol_table.declare(node.alias.name, 'context_var')
            
        for stmt in node.body:
            self.analyze(stmt)
        self.symbol_table.pop_scope()

    def visit_TryStmt(self, node: TryStmt):
        self.symbol_table.push_scope()
        for stmt in node.body:
            self.analyze(stmt)
        self.symbol_table.pop_scope()
        
        for exc_type, alias, body in node.except_blocks:
            if exc_type:
                self.analyze(exc_type)
            self.symbol_table.push_scope()
            if alias:
                self.symbol_table.declare(alias.name, 'exception')
            for stmt in body:
                self.analyze(stmt)
            self.symbol_table.pop_scope()
            
        if node.finally_block:
            self.symbol_table.push_scope()
            for stmt in node.finally_block:
                self.analyze(stmt)
            self.symbol_table.pop_scope()

    def visit_MatchStmt(self, node: MatchStmt):
        self.analyze(node.expression)
        for case_expr, body in node.cases:
            self.analyze(case_expr)
            self.symbol_table.push_scope()
            for stmt in body:
                self.analyze(stmt)
            self.symbol_table.pop_scope()

    def visit_LambdaExpr(self, node: LambdaExpr):
        self.symbol_table.push_scope()
        for param in node.params:
            self.symbol_table.declare(param.name, 'parameter')
        self.analyze(node.body)
        self.symbol_table.pop_scope()

    def visit_Literal(self, node: Literal):
        pass # Literals don't need semantic validation
        
    def visit_PassStmt(self, node: PassStmt):
        pass
        
    def visit_ReturnStmt(self, node: ReturnStmt):
        if node.value:
            self.analyze(node.value)
