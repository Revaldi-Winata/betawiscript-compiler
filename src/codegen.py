from typing import List
from src.ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        
    def get_indent(self) -> str:
        return "    " * self.indent_level

    def generate(self, node: ASTNode) -> str:
        method_name = f"visit_{node.__class__.__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node: ASTNode) -> str:
        raise NotImplementedError(f"No code generator defined for {node.__class__.__name__}")

    def visit_Program(self, node: Program) -> str:
        code = ""
        for stmt in node.statements:
            code += self.get_indent() + self.generate(stmt) + "\n"
        return code

    def visit_Identifier(self, node: Identifier) -> str:
        # Translate special identifiers back to Python if needed
        if node.name == 'gue': return 'self'
        if node.name == 'emak': return 'super'
        
        # Built-in translations (Minang to Python)
        builtin_map = {
            'cetak': 'print',
            'panjang': 'len',
            'himpunan': 'set',
            'mutlak': 'abs',
            'Error': 'Exception',
            'baca': 'read',
            'bukak': 'open',
            'daftar': 'list',
            'tipe': 'type',
            'masuakan': 'input',
            'angka': 'int',
            'desimal': 'float',
            'kato': 'str',
            'rentang': 'range'
        }
        return builtin_map.get(node.name, node.name)

    def visit_Literal(self, node: Literal) -> str:
        if isinstance(node.value, bool):
            return "True" if node.value else "False"
        elif node.value is None:
            return "None"
        elif isinstance(node.value, str):
            return f'"{node.value}"'
        else:
            return str(node.value)

    def visit_Assignment(self, node: Assignment) -> str:
        target = self.generate(node.target)
        value = self.generate(node.value)
        return f"{target} = {value}"

    def visit_FunctionDef(self, node: FunctionDef) -> str:
        name = self.generate(node.name)
        params = ", ".join([self.generate(p) for p in node.params])
        code = f"def {name}({params}):\n"
        self.indent_level += 1
        if not node.body:
            code += self.get_indent() + "pass\n"
        else:
            for stmt in node.body:
                code += self.get_indent() + self.generate(stmt) + "\n"
        self.indent_level -= 1
        return code.rstrip()

    def visit_ClassDef(self, node: ClassDef) -> str:
        name = self.generate(node.name)
        if node.parent:
            parent = self.generate(node.parent)
            code = f"class {name}({parent}):\n"
        else:
            code = f"class {name}:\n"
            
        self.indent_level += 1
        if not node.body:
            code += self.get_indent() + "pass\n"
        else:
            for stmt in node.body:
                code += self.get_indent() + self.generate(stmt) + "\n"
        self.indent_level -= 1
        return code.rstrip()

    def visit_FunctionCall(self, node: FunctionCall) -> str:
        name = self.generate(node.name)
        args = ", ".join([self.generate(arg) for arg in node.args])
        return f"{name}({args})"

    def visit_ReturnStmt(self, node: ReturnStmt) -> str:
        if node.value:
            return f"return {self.generate(node.value)}"
        return "return"

    def visit_ExprStmt(self, node: ExprStmt) -> str:
        return self.generate(node.expression)

    def visit_BinaryOp(self, node: BinaryOp) -> str:
        left = self.generate(node.left)
        right = self.generate(node.right)
        op = node.operator
        
        # Translate logic operators
        if op == 'ama': op = 'and'
        elif op == 'atawa': op = 'or'
            
        return f"({left} {op} {right})"

    def visit_UnaryOp(self, node: UnaryOp) -> str:
        op = node.operator
        operand = self.generate(node.operand)
        if op == 'bukan': op = 'not '
        return f"({op}{operand})"

    def visit_IfStmt(self, node: IfStmt) -> str:
        cond = self.generate(node.condition)
        code = f"if {cond}:\n"
        
        self.indent_level += 1
        if not node.then_branch:
            code += self.get_indent() + "pass\n"
        else:
            for stmt in node.then_branch:
                code += self.get_indent() + self.generate(stmt) + "\n"
        self.indent_level -= 1
        
        for e_cond, e_body in node.elif_branches:
            code += self.get_indent() + f"elif {self.generate(e_cond)}:\n"
            self.indent_level += 1
            if not e_body:
                code += self.get_indent() + "pass\n"
            else:
                for stmt in e_body:
                    code += self.get_indent() + self.generate(stmt) + "\n"
            self.indent_level -= 1
            
        if node.else_branch is not None:
            code += self.get_indent() + "else:\n"
            self.indent_level += 1
            if not node.else_branch:
                code += self.get_indent() + "pass\n"
            else:
                for stmt in node.else_branch:
                    code += self.get_indent() + self.generate(stmt) + "\n"
            self.indent_level -= 1
            
        return code.rstrip()

    def visit_WhileStmt(self, node: WhileStmt) -> str:
        cond = self.generate(node.condition)
        code = f"while {cond}:\n"
        
        self.indent_level += 1
        if not node.body:
            code += self.get_indent() + "pass\n"
        else:
            for stmt in node.body:
                code += self.get_indent() + self.generate(stmt) + "\n"
        self.indent_level -= 1
        return code.rstrip()

    def visit_ForStmt(self, node: ForStmt) -> str:
        iterator = self.generate(node.iterator)
        iterable = self.generate(node.iterable)
        code = f"for {iterator} in {iterable}:\n"
        
        self.indent_level += 1
        if not node.body:
            code += self.get_indent() + "pass\n"
        else:
            for stmt in node.body:
                code += self.get_indent() + self.generate(stmt) + "\n"
        self.indent_level -= 1
        return code.rstrip()

    def visit_BreakStmt(self, node: BreakStmt) -> str:
        return "break"

    def visit_ContinueStmt(self, node: ContinueStmt) -> str:
        return "continue"

    def visit_PassStmt(self, node: PassStmt) -> str:
        return "pass"

    def visit_TryStmt(self, node: TryStmt) -> str:
        code = "try:\n"
        self.indent_level += 1
        if not node.body:
            code += self.get_indent() + "pass\n"
        else:
            for stmt in node.body:
                code += self.get_indent() + self.generate(stmt) + "\n"
        self.indent_level -= 1
        
        for exc_type, alias, e_body in node.except_blocks:
            exc_str = ""
            if exc_type:
                exc_str = self.generate(exc_type)
                if alias:
                    exc_str += f" as {self.generate(alias)}"
            
            if exc_str:
                code += self.get_indent() + f"except {exc_str}:\n"
            else:
                code += self.get_indent() + "except:\n"
                
            self.indent_level += 1
            if not e_body:
                code += self.get_indent() + "pass\n"
            else:
                for stmt in e_body:
                    code += self.get_indent() + self.generate(stmt) + "\n"
            self.indent_level -= 1
            
        if node.finally_block is not None:
            code += self.get_indent() + "finally:\n"
            self.indent_level += 1
            if not node.finally_block:
                code += self.get_indent() + "pass\n"
            else:
                for stmt in node.finally_block:
                    code += self.get_indent() + self.generate(stmt) + "\n"
            self.indent_level -= 1
            
        return code.rstrip()

    def visit_ImportStmt(self, node: ImportStmt) -> str:
        module = self.generate(node.module)
        if node.alias:
            return f"import {module} as {self.generate(node.alias)}"
        return f"import {module}"

    def visit_FromImportStmt(self, node: FromImportStmt) -> str:
        module = self.generate(node.module)
        name = self.generate(node.name)
        return f"from {module} import {name}"

    def visit_WithStmt(self, node: WithStmt) -> str:
        expr = self.generate(node.expression)
        code = f"with {expr}"
        if node.alias:
            code += f" as {self.generate(node.alias)}"
        code += ":\n"
        
        self.indent_level += 1
        if not node.body:
            code += self.get_indent() + "pass\n"
        else:
            for stmt in node.body:
                code += self.get_indent() + self.generate(stmt) + "\n"
        self.indent_level -= 1
        return code.rstrip()

    def visit_AsyncStmt(self, node: AsyncStmt) -> str:
        stmt = self.generate(node.stmt)
        return f"async {stmt}"

    def visit_AwaitExpr(self, node: AwaitExpr) -> str:
        expr = self.generate(node.expression)
        return f"await {expr}"

    def visit_MatchStmt(self, node: MatchStmt) -> str:
        expr = self.generate(node.expression)
        code = f"match {expr}:\n"
        
        self.indent_level += 1
        for case_expr, case_body in node.cases:
            c_expr = self.generate(case_expr)
            code += self.get_indent() + f"case {c_expr}:\n"
            
            self.indent_level += 1
            if not case_body:
                code += self.get_indent() + "pass\n"
            else:
                for stmt in case_body:
                    code += self.get_indent() + self.generate(stmt) + "\n"
            self.indent_level -= 1
        self.indent_level -= 1
        
        return code.rstrip()

    def visit_UnaryCtrlStmt(self, node: UnaryCtrlStmt) -> str:
        kw_map = {
            'angkat': 'raise',
            'pastiin': 'assert',
            'hapus': 'del',
            'seluruhnya': 'global',
            'bukan_lokal': 'nonlocal',
            'hasilin': 'yield'
        }
        kw = kw_map.get(node.keyword, node.keyword)
        expr = self.generate(node.expression)
        return f"{kw} {expr}"

    def visit_LambdaExpr(self, node: LambdaExpr) -> str:
        params = ", ".join([self.generate(p) for p in node.params])
        body = self.generate(node.body)
        return f"(lambda {params}: {body})"
