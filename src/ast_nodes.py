from dataclasses import dataclass, field
from typing import List, Optional, Union, Tuple

@dataclass
class ASTNode:
    def print_ast(self, level: int = 0) -> str:
        indent = "  " * level
        result = f"{indent}{self.__class__.__name__}\n"
        for key, value in self.__dict__.items():
            if isinstance(value, ASTNode):
                result += f"{indent}  {key}:\n"
                result += value.print_ast(level + 2)
            elif isinstance(value, list):
                if value:
                    result += f"{indent}  {key}:\n"
                    for item in value:
                        if isinstance(item, ASTNode):
                            result += item.print_ast(level + 2)
                        elif isinstance(item, tuple):
                            # Special case for if-elif pairs
                            if len(item) == 2 and isinstance(item[0], ASTNode) and isinstance(item[1], list):
                                result += f"{indent}    - ElifBranch:\n"
                                result += f"{indent}        Condition:\n"
                                result += item[0].print_ast(level + 5)
                                result += f"{indent}        Body:\n"
                                for b_stmt in item[1]:
                                    result += b_stmt.print_ast(level + 5)
                        else:
                            result += f"{indent}    - {item}\n"
            else:
                result += f"{indent}  {key}: {value}\n"
        return result

@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class Literal(ASTNode):
    value: Union[str, int, float, bool, None]

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class Assignment(ASTNode):
    target: Identifier
    value: ASTNode

@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    elif_branches: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)
    else_branch: Optional[List[ASTNode]] = None

@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: List[ASTNode]
    
@dataclass
class ForStmt(ASTNode):
    iterator: Identifier
    iterable: ASTNode
    body: List[ASTNode]

@dataclass
class FunctionDef(ASTNode):
    name: Identifier
    params: List[Identifier]
    body: List[ASTNode]

@dataclass
class FunctionCall(ASTNode):
    name: Identifier
    args: List[ASTNode]

@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode]
    
@dataclass
class ExprStmt(ASTNode):
    expression: ASTNode

@dataclass
class ClassDef(ASTNode):
    name: Identifier
    parent: Optional[Identifier]
    body: List[ASTNode]

@dataclass
class TryStmt(ASTNode):
    body: List[ASTNode]
    except_blocks: List[Tuple[Optional[Identifier], Optional[Identifier], List[ASTNode]]] = field(default_factory=list)
    finally_block: Optional[List[ASTNode]] = None

@dataclass
class ImportStmt(ASTNode):
    module: Identifier
    alias: Optional[Identifier]

@dataclass
class FromImportStmt(ASTNode):
    module: Identifier
    name: Identifier

@dataclass
class WithStmt(ASTNode):
    expression: ASTNode
    alias: Optional[Identifier]
    body: List[ASTNode]

@dataclass
class AsyncStmt(ASTNode):
    stmt: ASTNode

@dataclass
class AwaitExpr(ASTNode):
    expression: ASTNode

@dataclass
class MatchStmt(ASTNode):
    expression: ASTNode
    cases: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)

@dataclass
class BreakStmt(ASTNode):
    pass

@dataclass
class ContinueStmt(ASTNode):
    pass

@dataclass
class PassStmt(ASTNode):
    pass

@dataclass
class UnaryCtrlStmt(ASTNode):
    keyword: str
    expression: ASTNode

@dataclass
class LambdaExpr(ASTNode):
    params: List[Identifier]
    body: ASTNode
