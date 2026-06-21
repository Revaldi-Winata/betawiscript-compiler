from typing import List
from src.cst_nodes import ParseNode
from src.token import Token
from src.ast_nodes import *

class ASTBuilder:
    def build(self, node: ParseNode) -> ASTNode:
        method_name = f"build_{node.name}"
        method = getattr(self, method_name, self.generic_build)
        return method(node)

    def generic_build(self, node: ParseNode) -> ASTNode:
        raise NotImplementedError(f"No build method for ParseNode '{node.name}'")

    def build_program(self, node: ParseNode) -> Program:
        program = Program()
        for child in node.children:
            if isinstance(child, ParseNode):
                program.statements.append(self.build(child))
        return program

    def build_assignment_stmt(self, node: ParseNode) -> Assignment:
        target = Identifier(node.children[0].value)
        value = self.build(node.children[2])
        return Assignment(target, value)

    def build_if_stmt(self, node: ParseNode) -> IfStmt:
        condition = self.build(node.children[2])
        then_branch = []
        idx = 5
        while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
            then_branch.append(self.build(node.children[idx]))
            idx += 1
            
        idx += 1 # skip RBRACE
        elif_branches = []
        else_branch = None
        
        while idx < len(node.children):
            token = node.children[idx]
            if isinstance(token, Token):
                if token.value == 'kalo_kaga':
                    elif_cond = self.build(node.children[idx+2])
                    elif_body = []
                    idx += 5
                    while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
                        elif_body.append(self.build(node.children[idx]))
                        idx += 1
                    elif_branches.append((elif_cond, elif_body))
                    idx += 1
                elif token.value == 'laennya':
                    else_branch = []
                    idx += 2
                    while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
                        else_branch.append(self.build(node.children[idx]))
                        idx += 1
                    idx += 1
                else:
                    idx += 1
            else:
                idx += 1

        return IfStmt(condition, then_branch, elif_branches, else_branch)

    def build_while_stmt(self, node: ParseNode) -> WhileStmt:
        condition = self.build(node.children[2])
        body = []
        idx = 5
        while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
            body.append(self.build(node.children[idx]))
            idx += 1
        return WhileStmt(condition, body)
        
    def build_for_stmt(self, node: ParseNode) -> ForStmt:
        iterator = Identifier(node.children[2].value)
        iterable = self.build(node.children[4])
        body = []
        idx = 7
        while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
            body.append(self.build(node.children[idx]))
            idx += 1
        return ForStmt(iterator, iterable, body)

    def build_function_def_stmt(self, node: ParseNode) -> FunctionDef:
        name = Identifier(node.children[1].value)
        params_node = node.children[3]
        params = []
        for param_token in params_node.children:
            if isinstance(param_token, Token) and (param_token.type.name == 'IDENTIFIER' or param_token.value == 'gue'):
                params.append(Identifier(param_token.value))
                
        body = []
        idx = 6
        while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
            body.append(self.build(node.children[idx]))
            idx += 1
        return FunctionDef(name, params, body)

    def build_class_def_stmt(self, node: ParseNode) -> ClassDef:
        name = Identifier(node.children[1].value)
        parent = None
        idx = 2
        if isinstance(node.children[idx], Token) and node.children[idx].value == '(':
            parent = Identifier(node.children[idx+1].value)
            idx += 3 # skip ( IDENTIFIER )
        
        idx += 1 # skip {
        body = []
        while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
            body.append(self.build(node.children[idx]))
            idx += 1
        return ClassDef(name, parent, body)

    def build_try_stmt(self, node: ParseNode) -> TryStmt:
        body = []
        idx = 2 # skip cubo {
        while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
            body.append(self.build(node.children[idx]))
            idx += 1
        idx += 1 # skip }
        
        except_blocks = []
        finally_block = None
        
        while idx < len(node.children) and isinstance(node.children[idx], Token) and node.children[idx].value == 'kecuali':
            idx += 1
            exc_type = None
            alias = None
            if isinstance(node.children[idx], Token) and node.children[idx].type.name == 'IDENTIFIER':
                exc_type = Identifier(node.children[idx].value)
                idx += 1
                if isinstance(node.children[idx], Token) and node.children[idx].value == 'sebagai':
                    alias = Identifier(node.children[idx+1].value)
                    idx += 2
            
            idx += 1 # skip {
            ex_body = []
            while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
                ex_body.append(self.build(node.children[idx]))
                idx += 1
            idx += 1 # skip }
            except_blocks.append((exc_type, alias, ex_body))

        if idx < len(node.children) and isinstance(node.children[idx], Token) and node.children[idx].value == 'akhirnya':
            idx += 2 # skip akhirnya {
            finally_block = []
            while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
                finally_block.append(self.build(node.children[idx]))
                idx += 1
                
        return TryStmt(body, except_blocks, finally_block)

    def build_import_stmt(self, node: ParseNode) -> ImportStmt:
        module = Identifier(node.children[1].value)
        alias = None
        if len(node.children) > 2:
            alias = Identifier(node.children[3].value)
        return ImportStmt(module, alias)
        
    def build_from_import_stmt(self, node: ParseNode) -> FromImportStmt:
        module = Identifier(node.children[1].value)
        name = Identifier(node.children[3].value)
        return FromImportStmt(module, name)

    def build_with_stmt(self, node: ParseNode) -> WithStmt:
        expression = self.build(node.children[1])
        alias = None
        idx = 2
        if isinstance(node.children[idx], Token) and node.children[idx].value == 'sebagai':
            alias = Identifier(node.children[idx+1].value)
            idx += 2
        idx += 1 # skip {
        body = []
        while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
            body.append(self.build(node.children[idx]))
            idx += 1
        return WithStmt(expression, alias, body)

    def build_async_stmt(self, node: ParseNode) -> AsyncStmt:
        return AsyncStmt(self.build(node.children[1]))

    def build_match_stmt(self, node: ParseNode) -> MatchStmt:
        expression = self.build(node.children[1])
        cases = []
        idx = 3 # skip cocok expr {
        while idx < len(node.children) and isinstance(node.children[idx], Token) and node.children[idx].value == 'kasus':
            idx += 1
            case_expr = self.build(node.children[idx])
            idx += 2 # skip expr {
            case_body = []
            while idx < len(node.children) and isinstance(node.children[idx], ParseNode):
                case_body.append(self.build(node.children[idx]))
                idx += 1
            idx += 1 # skip }
            cases.append((case_expr, case_body))
        return MatchStmt(expression, cases)

    def build_berenti_stmt(self, node: ParseNode) -> BreakStmt: return BreakStmt()
    def build_terusin_stmt(self, node: ParseNode) -> ContinueStmt: return ContinueStmt()
    def build_lewat_stmt(self, node: ParseNode) -> PassStmt: return PassStmt()

    def _build_unary_ctrl(self, node: ParseNode) -> UnaryCtrlStmt:
        kw = node.children[0].value
        expr = self.build(node.children[1])
        return UnaryCtrlStmt(kw, expr)
        
    build_angkat_stmt = _build_unary_ctrl
    build_pastiin_stmt = _build_unary_ctrl
    build_apus_stmt = _build_unary_ctrl
    build_seluruhnya_stmt = _build_unary_ctrl
    build_bukan_lokal_stmt = _build_unary_ctrl
    build_hasilin_stmt = _build_unary_ctrl

    def build_function_call_stmt(self, node: ParseNode) -> FunctionCall:
        name = Identifier(node.children[0].value)
        args_node = node.children[2]
        args = []
        for child in args_node.children:
            if isinstance(child, ParseNode):
                args.append(self.build(child))
        return FunctionCall(name, args)

    def build_return_stmt(self, node: ParseNode) -> ReturnStmt:
        val = None
        if len(node.children) > 1:
            val = self.build(node.children[1])
        return ReturnStmt(val)

    def build_expression_stmt(self, node: ParseNode) -> ExprStmt:
        return ExprStmt(self.build(node.children[0]))

    def _build_binary_op(self, node: ParseNode) -> ASTNode:
        if len(node.children) == 1:
            return self.build(node.children[0])
            
        left = self.build(node.children[0])
        idx = 1
        if isinstance(node.children[idx], Token) and node.children[idx].type.name == 'KEYWORD':
            operator = node.children[idx].value
        else:
            operator = node.children[idx].value
            
        right = self.build(node.children[2])
        return BinaryOp(left, operator, right)

    build_logical_expression = _build_binary_op
    build_equality_expression = _build_binary_op
    build_comparison_expression = _build_binary_op
    build_term_expression = _build_binary_op
    build_factor_expression = _build_binary_op
    
    def build_unary_expression(self, node: ParseNode) -> UnaryOp:
        op = node.children[0].value
        expr = self.build(node.children[1])
        return UnaryOp(op, expr)
        
    def build_await_expression(self, node: ParseNode) -> AwaitExpr:
        return AwaitExpr(self.build(node.children[1]))
        
    def build_lambda_expression(self, node: ParseNode) -> LambdaExpr:
        params_node = node.children[1]
        params = []
        for param_token in params_node.children:
            if isinstance(param_token, Token) and (param_token.type.name == 'IDENTIFIER' or param_token.value == 'gue'):
                params.append(Identifier(param_token.value))
        body = self.build(node.children[3])
        return LambdaExpr(params, body)

    def build_primary(self, node: ParseNode) -> ASTNode:
        token = node.children[0]
        if token.type.name == 'NUMBER':
            val = token.value
            num_val = float(val) if '.' in val else int(val)
            return Literal(num_val)
        elif token.type.name == 'STRING':
            val = token.value[1:-1]
            return Literal(val)
        elif token.type.name == 'IDENTIFIER':
            return Identifier(token.value)
        elif token.type.name == 'BUILTIN':
            return Identifier(token.value)
        elif token.type.name == 'KEYWORD':
            val = token.value
            if val == 'Bener': return Literal(True)
            elif val == 'Kaga': return Literal(False)
            elif val == 'Kosong': return Literal(None)
            elif val == 'gue': return Identifier('gue')
            elif val == 'emak': return Identifier('emak')
        
        raise Exception(f"Unknown primary token: {token}")

    def build_grouping(self, node: ParseNode) -> ASTNode:
        return self.build(node.children[1])
