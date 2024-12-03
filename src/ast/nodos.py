import json
from typing import Sequence
from src.ast.etiqueta import AstLabel

# Configuración para la codificación JSON
jsonConfig = {
    'separators': (',', ':'), 
    'default': lambda obj: obj.value
}

def flecha_json_encode(data):
    """Convierte la entrada a una cadena JSON."""
    return json.dumps(data, **jsonConfig)

AstNodeOutput = int | str | Sequence['AstNodeOutput']

class AstNode:
    """Representa un nodo en el árbol de sintaxis abstracta (AST)."""

    def __init__(self, label: AstLabel, children=None):
        """
        Inicializa un nodo del AST.

        :param label: Etiqueta del nodo.
        :param children: Lista de nodos hijos (predeterminado es una lista vacía).
        """
        self.value = None
        self.label = label
        self.children = children if children is not None else []

    def append(self, child: 'AstNode'):
        """Agrega un nodo hijo."""
        self.children.append(child)
        return self

    def _out(self):
        """Genera la representación del nodo como lista."""
        return [self.label] + self._children_out()

    def _children_out(self):
        """Genera la representación de los nodos hijos."""
        return [child._out() for child in self.children]

    def __repr__(self):
        """Devuelve la representación del nodo en formato JSON."""
        return flecha_json_encode(self._out())

    def __eq__(self, other: object) -> bool:
        """Compara si dos nodos son iguales."""
        return self.__repr__() == other.__repr__()

class AstLeaf(AstNode):
    """Representa una hoja en el árbol de sintaxis abstracta (AST)."""

    def __init__(self, label: AstLabel, value):
        """
        Inicializa una hoja del AST.

        :param label: Etiqueta de la hoja.
        :param value: Valor de la hoja.
        """
        super().__init__(label)
        self.value = "OR" if value == '||' else value

    def _out(self):
        """Devuelve el valor de la hoja."""
        return self.value

class AstNodeList(AstNode):
    """Representa una lista de nodos en el árbol de sintaxis abstracta (AST)."""

    def __init__(self, label: AstLabel, nodes: Sequence[AstNode]):
        """
        Inicializa una lista de nodos.

        :param label: Etiqueta de la lista.
        :param nodes: Lista de nodos que la conforman.
        """
        super().__init__(label, nodes)

    def _out(self):
        """Devuelve la representación de los nodos hijos."""
        return self._children_out() if self.children else []