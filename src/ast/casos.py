from typing import Sequence
from src.ast.nodos import AstNodeList, AstNode
from src.ast.expresion import build_id
from src.ast.etiqueta import AstLabel

# Identificadores para los valores booleanos
TRUE_ID = 'True'
FALSE_ID = 'False'

class CaseBranch(AstNode):
    """Clase que representa una rama de un caso en el árbol de sintaxis abstracta (AST)."""

    def __init__(self, _id: str, _params: Sequence[str], expr):
        """
        Inicializa una rama de caso.

        :param _id: Identificador de la rama.
        :param _params: Parámetros de la rama.
        :param expr: Expresión asociada a la rama.
        """
        # Crea un nodo de tipo CaseBranch con el identificador, parámetros y expresión
        children = [build_id(_id), Params([build_id(param) for param in _params]), expr]
        super().__init__(AstLabel.CaseBranch, children)

    def id(self) -> str:
        """Devuelve el identificador de la rama."""
        return self.children[0].value

    def params(self) -> list:
        """Devuelve los parámetros de la rama."""
        return [param.value for param in self.children[1].children]

    def expr(self):
        """Devuelve la expresión de la rama."""
        return self.children[2]

class Params(AstNodeList):
    """Clase que representa una lista de parámetros en una rama de caso."""
    
    def __init__(self, params: Sequence[AstNode]):
        """Inicializa una lista de parámetros."""
        super().__init__(AstLabel.Params, params)

class CaseBranches(AstNodeList):
    """Clase que representa una lista de ramas de caso."""

    def __init__(self, branches: Sequence[CaseBranch]):
        """Inicializa una lista de ramas de caso."""
        super().__init__(AstLabel.CaseBranches, branches)

    def append_case(self, branch: CaseBranch):
        """Agrega una rama de caso a la lista."""
        return self.append(branch)

class CaseExpr(AstNode):
    """Clase que representa una expresión de tipo case en el árbol de sintaxis abstracta (AST)."""

    def __init__(self, expr: AstNode, branches: CaseBranches):
        """
        Inicializa una expresión de tipo case.

        :param expr: Expresión que se está evaluando.
        :param branches: Ramas de caso que se evalúan.
        """
        super().__init__(AstLabel.ExprCase, [expr] + branches.children)

    def expr(self) -> AstNode:
        """Devuelve la expresión que se evalúa en el case."""
        return self.children[0]

    def branches(self) -> list:
        """Devuelve las ramas de caso para la expresión."""
        return self.children[1:]

    def _out_branches(self):
        """Devuelve la representación de las ramas de caso."""
        return [branch._out() for branch in self.branches()]

    def _out(self):
        """Devuelve la representación de la expresión case en formato JSON."""
        return [self.label, self.expr()._out(), self._out_branches()]

# Constructores

def build_if(expr: AstNode, then_expr: AstNode, else_expr: AstNode) -> CaseExpr:
    """Construye una expresión if a partir de una expresión y sus rama 'then' y 'else'."""
    return CaseExpr(expr, CaseBranches([CaseBranch(TRUE_ID, [], then_expr), else_expr]))

def build_else(else_expr: AstNode) -> CaseBranch:
    """Construye una rama de caso para la expresión else."""
    return CaseBranch(FALSE_ID, [], else_expr)