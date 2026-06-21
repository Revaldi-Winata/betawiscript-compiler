from dataclasses import dataclass, field
from typing import List, Union
from src.token import Token

@dataclass
class ParseNode:
    name: str
    children: List[Union['ParseNode', Token]] = field(default_factory=list)

    def print_tree(self, level: int = 0) -> str:
        indent = "  " * level
        result = f"{indent}{self.name}\n"
        for child in self.children:
            if isinstance(child, ParseNode):
                result += child.print_tree(level + 1)
            elif isinstance(child, Token):
                result += f"{indent}  '{child.value}' ({child.type.name})\n"
        return result
