from typing import List, Optional
from src.ast_nodes import *

class ASTOptimizer:
    def optimize(self, node: ASTNode) -> ASTNode:
        method_name = f"visit_{node.__class__.__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node: ASTNode) -> ASTNode:
        # Default behavior: visit all children and replace them with optimized versions
        for key, value in node.__dict__.items():
            if isinstance(value, ASTNode):
                setattr(node, key, self.optimize(value))
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, ASTNode):
                        optimized_item = self.optimize(item)
                        if optimized_item:
                            new_list.append(optimized_item)
                    elif isinstance(item, tuple):
                        # For cases like elif_branches or match_cases
                        new_tuple = []
                        for sub_item in item:
                            if isinstance(sub_item, ASTNode):
                                new_tuple.append(self.optimize(sub_item))
                            elif isinstance(sub_item, list):
                                new_sub_list = self._optimize_block(sub_item)
                                new_tuple.append(new_sub_list)
                            else:
                                new_tuple.append(sub_item)
                        new_list.append(tuple(new_tuple))
                    else:
                        new_list.append(item)
                setattr(node, key, new_list)
        return node

    def _optimize_block(self, statements: List[ASTNode]) -> List[ASTNode]:
        optimized_stmts = []
        for stmt in statements:
            opt_stmt = self.optimize(stmt)
            if opt_stmt:
                optimized_stmts.append(opt_stmt)
            # Dead code elimination: stop processing block after return, break, or continue
            if isinstance(opt_stmt, (ReturnStmt, BreakStmt, ContinueStmt)):
                break
        return optimized_stmts

    def visit_Program(self, node: Program) -> Program:
        node.statements = self._optimize_block(node.statements)
        return node

    def visit_FunctionDef(self, node: FunctionDef) -> FunctionDef:
        node.body = self._optimize_block(node.body)
        return node

    def visit_ClassDef(self, node: ClassDef) -> ClassDef:
        node.body = self._optimize_block(node.body)
        return node

    def visit_WhileStmt(self, node: WhileStmt) -> Optional[ASTNode]:
        node.condition = self.optimize(node.condition)
        
        # Dead Code: if condition is strictly False
        if isinstance(node.condition, Literal) and not bool(node.condition.value):
            return None # Remove the loop completely
            
        node.body = self._optimize_block(node.body)
        return node

    def visit_ForStmt(self, node: ForStmt) -> ForStmt:
        node.iterable = self.optimize(node.iterable)
        node.body = self._optimize_block(node.body)
        return node

    def visit_WithStmt(self, node: WithStmt) -> WithStmt:
        node.expression = self.optimize(node.expression)
        node.body = self._optimize_block(node.body)
        return node

    def visit_TryStmt(self, node: TryStmt) -> TryStmt:
        node.body = self._optimize_block(node.body)
        
        opt_excepts = []
        for exc_type, alias, body in node.except_blocks:
            opt_exc_type = self.optimize(exc_type) if exc_type else None
            opt_body = self._optimize_block(body)
            opt_excepts.append((opt_exc_type, alias, opt_body))
        node.except_blocks = opt_excepts
        
        if node.finally_block:
            node.finally_block = self._optimize_block(node.finally_block)
            
        return node

    def visit_MatchStmt(self, node: MatchStmt) -> MatchStmt:
        node.expression = self.optimize(node.expression)
        opt_cases = []
        for case_expr, body in node.cases:
            opt_cases.append((self.optimize(case_expr), self._optimize_block(body)))
        node.cases = opt_cases
        return node

    def visit_IfStmt(self, node: IfStmt) -> Optional[ASTNode]:
        node.condition = self.optimize(node.condition)
        node.then_branch = self._optimize_block(node.then_branch)
        
        # Optimize elifs
        opt_elifs = []
        for cond, body in node.elif_branches:
            opt_cond = self.optimize(cond)
            opt_body = self._optimize_block(body)
            opt_elifs.append((opt_cond, opt_body))
        node.elif_branches = opt_elifs
        
        if node.else_branch:
            node.else_branch = self._optimize_block(node.else_branch)

        # Dead code elimination for If branches based on Literal conditions
        if isinstance(node.condition, Literal):
            if bool(node.condition.value):
                # We can just replace this whole if statement with its then_branch
                # However, since returning a list of statements instead of a single node 
                # is tricky in a generic visitor without flattening, we will return an IfStmt 
                # with no elif/else and True condition. Or wrap in a block.
                # For simplicity, keep it but remove elif/else.
                node.elif_branches = []
                node.else_branch = None
            else:
                # The main if is false. Let's see if there's an elif that is true
                found_true_elif = False
                new_elifs = []
                for cond, body in node.elif_branches:
                    if isinstance(cond, Literal):
                        if bool(cond.value):
                            # This elif is true! Make it the main if
                            node.condition = cond
                            node.then_branch = body
                            node.elif_branches = []
                            node.else_branch = None
                            found_true_elif = True
                            break
                        else:
                            pass # False elif, discard
                    else:
                        new_elifs.append((cond, body))
                        
                if not found_true_elif:
                    node.elif_branches = new_elifs
                    if not node.elif_branches:
                        if node.else_branch:
                            # Only else branch remains
                            node.condition = Literal(True)
                            node.then_branch = node.else_branch
                            node.else_branch = None
                        else:
                            # Entire if statement is dead code
                            return None
        return node

    def visit_BinaryOp(self, node: BinaryOp) -> ASTNode:
        node.left = self.optimize(node.left)
        node.right = self.optimize(node.right)
        
        # Constant Folding
        if isinstance(node.left, Literal) and isinstance(node.right, Literal):
            l = node.left.value
            r = node.right.value
            op = node.operator
            
            try:
                # Math
                if op == '+': return Literal(l + r)
                elif op == '-': return Literal(l - r)
                elif op == '*': return Literal(l * r)
                elif op == '/': return Literal(l / r)
                elif op == '//': return Literal(l // r)
                elif op == '%': return Literal(l % r)
                elif op == '**': return Literal(l ** r)
                # Comparison
                elif op == '==': return Literal(l == r)
                elif op == '!=': return Literal(l != r)
                elif op == '>': return Literal(l > r)
                elif op == '<': return Literal(l < r)
                elif op == '>=': return Literal(l >= r)
                elif op == '<=': return Literal(l <= r)
                # Logical
                elif op == 'ama': return Literal(l and r)
                elif op == 'atawa': return Literal(l or r)
            except Exception:
                # Division by zero or type mismatch during folding
                pass
                
        return node

    def visit_UnaryOp(self, node: UnaryOp) -> ASTNode:
        node.operand = self.optimize(node.operand)
        
        # Constant Folding
        if isinstance(node.operand, Literal):
            val = node.operand.value
            op = node.operator
            
            try:
                if op == '-': return Literal(-val)
                elif op == '+': return Literal(+val)
                elif op == 'bukan': return Literal(not bool(val))
            except Exception:
                pass
                
        return node
