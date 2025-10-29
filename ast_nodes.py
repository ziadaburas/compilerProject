"""
AST Node Classes for Arabic Programming Language
تعريف عقد شجرة النحو المجرد (Abstract Syntax Tree)
"""

class ASTNode:
    """Base class for all AST nodes"""
    def __init__(self, line=None, column=None):
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"


class ProgramNode(ASTNode):
    """برنامج - Program node"""
    def __init__(self, name, block, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.block = block
    
    def __repr__(self):
        return f"ProgramNode(name='{self.name}')"


class BlockNode(ASTNode):
    """كتلة برمجية - Block node"""
    def __init__(self, constants=None, types=None, variables=None, 
                 procedures=None, instructions=None, line=None, column=None):
        super().__init__(line, column)
        self.constants = constants or []
        self.types = types or []
        self.variables = variables or []
        self.procedures = procedures or []
        self.instructions = instructions or []


class ConstantDefNode(ASTNode):
    """تعريف ثابت - Constant definition"""
    def __init__(self, name, value, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"ConstantDefNode(name='{self.name}', value={self.value})"


class TypeDefNode(ASTNode):
    """تعريف نوع - Type definition"""
    def __init__(self, name, type_spec, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.type_spec = type_spec
    
    def __repr__(self):
        return f"TypeDefNode(name='{self.name}')"


class ListTypeNode(ASTNode):
    """نوع قائمة - List type"""
    def __init__(self, size, element_type, line=None, column=None):
        super().__init__(line, column)
        self.size = size
        self.element_type = element_type
    
    def __repr__(self):
        return f"ListTypeNode(size={self.size}, type={self.element_type})"


class RecordTypeNode(ASTNode):
    """نوع سجل - Record type"""
    def __init__(self, fields, line=None, column=None):
        super().__init__(line, column)
        self.fields = fields  # List of FieldDefNode
    
    def __repr__(self):
        return f"RecordTypeNode(fields={len(self.fields)})"


class FieldDefNode(ASTNode):
    """تعريف حقل - Field definition"""
    def __init__(self, names, data_type, line=None, column=None):
        super().__init__(line, column)
        self.names = names  # List of field names
        self.data_type = data_type
    
    def __repr__(self):
        return f"FieldDefNode(names={self.names}, type={self.data_type})"


class VarDeclNode(ASTNode):
    """تعريف متغير - Variable declaration"""
    def __init__(self, names, data_type, line=None, column=None):
        super().__init__(line, column)
        self.names = names  # List of variable names
        self.data_type = data_type
    
    def __repr__(self):
        return f"VarDeclNode(names={self.names}, type={self.data_type})"


class ProcedureDefNode(ASTNode):
    """تعريف إجراء - Procedure definition"""
    def __init__(self, name, params, block, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.params = params or []
        self.block = block
    
    def __repr__(self):
        return f"ProcedureDefNode(name='{self.name}', params={len(self.params)})"


class ParamDefNode(ASTNode):
    """تعريف معامل - Parameter definition"""
    def __init__(self, names, data_type, pass_mode='BY_VALUE', line=None, column=None):
        super().__init__(line, column)
        self.names = names
        self.data_type = data_type
        self.pass_mode = pass_mode  # 'BY_VALUE' or 'BY_REFERENCE'
    
    def __repr__(self):
        return f"ParamDefNode(names={self.names}, type={self.data_type}, mode={self.pass_mode})"


# ===== Statement Nodes =====

class AssignmentNode(ASTNode):
    """عبارة إسناد - Assignment statement"""
    def __init__(self, variable, expression, line=None, column=None):
        super().__init__(line, column)
        self.variable = variable
        self.expression = expression
    
    def __repr__(self):
        return f"AssignmentNode(var={self.variable})"


class InputNode(ASTNode):
    """عبارة قراءة - Input statement (اقرأ)"""
    def __init__(self, variable, line=None, column=None):
        super().__init__(line, column)
        self.variable = variable
    
    def __repr__(self):
        return f"InputNode(var={self.variable})"


class OutputNode(ASTNode):
    """عبارة طباعة - Output statement (اطبع)"""
    def __init__(self, items, line=None, column=None):
        super().__init__(line, column)
        self.items = items
    
    def __repr__(self):
        return f"OutputNode(items={len(self.items)})"


class CallNode(ASTNode):
    """استدعاء إجراء - Procedure call"""
    def __init__(self, procedure_name, arguments, line=None, column=None):
        super().__init__(line, column)
        self.procedure_name = procedure_name
        self.arguments = arguments or []
    
    def __repr__(self):
        return f"CallNode(proc='{self.procedure_name}', args={len(self.arguments)})"


class IfNode(ASTNode):
    """عبارة شرطية - Conditional statement (اذا)"""
    def __init__(self, condition, then_stmt, elif_parts=None, else_stmt=None, 
                 line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.then_stmt = then_stmt
        self.elif_parts = elif_parts or []  # List of (condition, stmt) tuples
        self.else_stmt = else_stmt
    
    def __repr__(self):
        return f"IfNode(elif_count={len(self.elif_parts)}, has_else={self.else_stmt is not None})"


class ForLoopNode(ASTNode):
    """حلقة تكرار for - For loop (كرر)"""
    def __init__(self, loop_var, start_expr, end_expr, step_expr, body, 
                 line=None, column=None):
        super().__init__(line, column)
        self.loop_var = loop_var
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.step_expr = step_expr
        self.body = body
    
    def __repr__(self):
        return f"ForLoopNode(var='{self.loop_var}')"


class WhileLoopNode(ASTNode):
    """حلقة طالما - While loop (طالما)"""
    def __init__(self, condition, body, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileLoopNode()"


class RepeatUntilNode(ASTNode):
    """حلقة اعد حتى - Repeat-until loop (اعد حتى)"""
    def __init__(self, body, condition, line=None, column=None):
        super().__init__(line, column)
        self.body = body
        self.condition = condition
    
    def __repr__(self):
        return f"RepeatUntilNode()"


class CompoundStmtNode(ASTNode):
    """عبارة مركبة - Compound statement { }"""
    def __init__(self, statements, line=None, column=None):
        super().__init__(line, column)
        self.statements = statements
    
    def __repr__(self):
        return f"CompoundStmtNode(stmts={len(self.statements)})"


# ===== Expression Nodes =====

class BinOpNode(ASTNode):
    """عملية ثنائية - Binary operation"""
    def __init__(self, left, operator, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right
        self.expr_type = None  # Will be filled by semantic analyzer
    
    def __repr__(self):
        return f"BinOpNode(op='{self.operator}')"


class UnaryOpNode(ASTNode):
    """عملية أحادية - Unary operation"""
    def __init__(self, operator, operand, line=None, column=None):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand
        self.expr_type = None
    
    def __repr__(self):
        return f"UnaryOpNode(op='{self.operator}')"


class VarAccessNode(ASTNode):
    """الوصول لمتغير - Variable access"""
    def __init__(self, name, selector=None, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.selector = selector  # IndexedSelectorNode or FieldSelectorNode
        self.expr_type = None
    
    def __repr__(self):
        return f"VarAccessNode(name='{self.name}', has_selector={self.selector is not None})"


class IndexedSelectorNode(ASTNode):
    """وصول مفهرس - Indexed access [index]"""
    def __init__(self, index_expr, line=None, column=None):
        super().__init__(line, column)
        self.index_expr = index_expr
    
    def __repr__(self):
        return f"IndexedSelectorNode()"


class FieldSelectorNode(ASTNode):
    """وصول حقل - Field access .field"""
    def __init__(self, field_name, line=None, column=None):
        super().__init__(line, column)
        self.field_name = field_name
    
    def __repr__(self):
        return f"FieldSelectorNode(field='{self.field_name}')"


class LiteralNode(ASTNode):
    """قيمة حرفية - Literal value"""
    def __init__(self, value, literal_type, line=None, column=None):
        super().__init__(line, column)
        self.value = value
        self.literal_type = literal_type  # 'INTEGER', 'REAL', 'STRING', 'CHAR', 'BOOLEAN'
        self.expr_type = literal_type
    
    def __repr__(self):
        return f"LiteralNode(value={self.value}, type={self.literal_type})"


class ConstantRefNode(ASTNode):
    """مرجع ثابت - Constant reference"""
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.expr_type = None
    
    def __repr__(self):
        return f"ConstantRefNode(name='{self.name}')"
