from src.ast.nodos import AstNode, AstLabel, AstLeaf

# Constantes utilizadas para estructuras de listas y variables
LIST_APPENDER = 'Cons'
LIST_EMPTY = 'Nil'
BLANK_VAR = '_'

# Diccionario para crear expresiones atómicas
atomic_expr = {
    "LOWERID": lambda v: VarExpr(v),
    "UPPERID": lambda v: ConstructorExpr(v),
    "NUMBER": lambda v: NumberExpr(v),
    "CHAR": lambda v: CharExpr(v),
    "STRING": lambda v: build_string(v),
}

# Operadores definidos
OP_UNARY = 'unary'
OP_BINARY = 'binary'

# Mapeo de operadores
operators = {
    OP_BINARY: {
        '||': 'OR',
        '&&': 'AND',
        '==': 'EQ',
        '!=': 'NE',
        '>=': 'GE',
        '<=': 'LE',
        '>': 'GT',
        '<': 'LT',
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV',
        '%': 'MOD',
    },
    OP_UNARY: {
        '-': 'UMINUS',
        '!': 'NOT'
    }
}

class LetExpr(AstNode):
    """Clase para expresiones 'let'."""

    def __init__(self, var_id: str, value_expr: AstNode, body_expr: AstNode):
        super().__init__(AstLabel.ExprLet, [build_id(var_id), value_expr, body_expr])

    def param(self):
        """Retorna el identificador de la variable."""
        return self.children[0].value

    def arg(self):
        """Retorna la expresión de asignación."""
        return self.children[1]

    def expr_in(self):
        """Retorna la expresión que utiliza la variable."""
        return self.children[2]

class ApplyExpr(AstNode):
    """Clase para aplicaciones de función."""

    def __init__(self, func: AstNode, arg: AstNode):
        super().__init__(AstLabel.ExprApply, [func, arg])

    def func(self):
        """Retorna la función aplicada."""
        return self.children[0]

    def arg(self):
        """Retorna el argumento de la función."""
        return self.children[1]

class LambdaExpr(AstNode):
    """Clase para expresiones lambda."""

    def __init__(self, param: str, body: AstNode):
        super().__init__(AstLabel.ExprLambda, [build_id(param), body])

    def param(self):
        """Retorna el parámetro de la lambda."""
        return self.children[0].value

    def expr(self):
        """Retorna la expresión del cuerpo de la lambda."""
        return self.children[1]

class LiteralExpr(AstLeaf):
    """Clase base para literales."""

    def __init__(self, label: AstLabel, value):
        super().__init__(label, value)

    def _out(self):
        """Devuelve la representación del literal."""
        return [self.label, self.value]

class NumberExpr(LiteralExpr):
    """Clase que representa un literal numérico."""

    def __init__(self, value: int):
        super().__init__(AstLabel.ExprNumber, value)

class VarExpr(LiteralExpr):
    """Clase que representa una expresión de variable."""

    def __init__(self, value: str):
        super().__init__(AstLabel.ExprVar, build_id(value))

    def id(self):
        """Retorna el identificador de la variable."""
        return self.value.value

class ConstructorExpr(LiteralExpr):
    """Clase para expresiones de constructor."""

    def __init__(self, value: str):
        super().__init__(AstLabel.ExprConstructor, build_id(value))

    def id(self):
        """Retorna el identificador del constructor."""
        return self.value.value

class CharExpr(LiteralExpr):
    """Clase que representa un carácter literal."""

    def __init__(self, value: str):
        super().__init__(AstLabel.ExprChar, ord(value))

# Funciones auxiliares para construir expresiones
def build_string(string_param: str):
    """Construye una expresión de cadena utilizando recursion."""
    if not string_param:
        return ConstructorExpr(LIST_EMPTY)
    return ApplyExpr(ApplyExpr(ConstructorExpr(LIST_APPENDER), CharExpr(string_param[0])), build_string(string_param[1:]))

def build_expression(params: list, expression: AstNode):
    """Construye una expresión lambda o devuelve la expresión directamente."""
    if not params:
        return expression
    return LambdaExpr(params[0], build_expression(params[1:], expression))

def build_id(value: str):
    """Construye un nodo del AST para un identificador."""
    return AstLeaf(AstLabel.Id, value)
def build_atomic(_type, value):
    """Construye un nodo atómico del AST según el tipo."""
    return atomic_expr[_type](value)
def build_binary_expression(left: AstNode, operator: str, right: AstNode) -> ApplyExpr:
    """Construye una expresión binaria en el AST.

    :param left: El operando izquierdo de la expresión.
    :param operator: El operador binario (por ejemplo, '+', '-', etc.).
    :param right: El operando derecho de la expresión.
    :return: Un nodo ApplyExpr que representa la expresión binaria.
    """
    # Obtiene el nombre del operador en el AST
    op = operators[OP_BINARY].get(operator)
    
    # Crea una aplicación de la función del operador
    left_apply = ApplyExpr(VarExpr(op), left)
    
    # Devuelve la aplicación de la función del operador a la parte izquierda y la parte derecha
    return ApplyExpr(left_apply, right)
def build_unary_expression(operator: str, right: AstNode) -> ApplyExpr:
    """Construye una expresión unaria en el AST.

    :param operator: El operador unario (por ejemplo, '-', 'NOT', etc.).
    :param right: El operando de la expresión unaria.
    :return: Un nodo ApplyExpr que representa la expresión unaria.
    """
    # Obtiene el nombre del operador en el AST
    op = operators[OP_UNARY].get(operator)
    
    # Crea un nodo ApplyExpr que aplica el operador unario a su operando
    return ApplyExpr(VarExpr(op), right)
def build_seq_let(expr1: AstNode, expr2: AstNode) -> LetExpr:
    """Construye una expresión de secuencia 'let' en el AST.

    :param expr1: La expresión que se asigna a la variable.
    :param expr2: La expresión que utiliza la variable ya asignada.
    :return: Un nodo LetExpr que representa la secuencia 'let'.
    """
    return LetExpr(BLANK_VAR, expr1, expr2)

