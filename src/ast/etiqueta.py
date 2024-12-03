from enum import Enum


class AstLabel(Enum):
    Program = ""
    Id = "Id"
    Def = "Def"
    ExprVar = "ExprVar"
    ExprConstructor = "ExprConstructor"
    ExprNumber = "ExprNumber"
    ExprChar = "ExprChar"
    ExprCase = "ExprCase"
    ExprLet = "ExprLet"
    ExprLambda = "ExprLambda"
    ExprApply = "ExprApply"
    CaseBranch = "CaseBranch"
    CaseBranches = ""
    Params = ""