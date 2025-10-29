
"""
Code Generator for Arabic Programming Language
مولد الكود الوسيط - يحول شجرة AST إلى كود بايثون قابل للتنفيذ
"""

from ast_nodes import *
from symbol_table import TypeInfo
import re


class CodeGenerator:
    """مولد الكود - Code Generator"""
    
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "  # 4 spaces
        self.generated_code = []
        self.temp_var_counter = 0
        self.in_procedure = False
        self.procedure_code = {}  # Store procedure code separately
        
    def generate(self, ast_node):
        """توليد الكود من شجرة AST - Generate code from AST"""
        if not ast_node:
            return ""
        
        self.generated_code = []
        self.visit(ast_node)
        
        # Combine all code
        code = "\n".join(self.generated_code)
        return code
    
    def emit(self, code_line):
        """إصدار سطر كود - Emit a line of code"""
        indent = self.indent_str * self.indent_level
        self.generated_code.append(indent + code_line)
    
    def emit_blank(self):
        """إصدار سطر فارغ - Emit blank line"""
        self.generated_code.append("")
    
    def increase_indent(self):
        """زيادة المسافة البادئة - Increase indentation"""
        self.indent_level += 1
    
    def decrease_indent(self):
        """إنقاص المسافة البادئة - Decrease indentation"""
        self.indent_level = max(0, self.indent_level - 1)
    
    def get_temp_var(self):
        """الحصول على متغير مؤقت - Get temporary variable"""
        self.temp_var_counter += 1
        return f"_temp_{self.temp_var_counter}"
    
    def sanitize_name(self, name):
        """تنظيف الأسماء العربية - Sanitize Arabic names for Python"""
        # Keep Arabic names as is, but ensure they're valid Python identifiers
        # Python 3 supports Unicode identifiers
        return name
    
    # ==================== Visit Methods ====================
    
    def visit(self, node):
        """زيارة عقدة - Visit a node"""
        if node is None:
            return ""
        
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """زيارة عامة - Generic visit"""
        return f"# Unhandled node: {node.__class__.__name__}"
    
    # ==================== Program & Block ====================
    
    def visit_ProgramNode(self, node):
        """توليد كود البرنامج - Generate program code"""
        # self.emit("#!/usr/bin/env python3")
        # self.emit("# -*- coding: utf-8 -*-")
        # self.emit(f'"""')
        # self.emit(f"برنامج: {node.name}")
        # self.emit(f"Program: {node.name}")
        # self.emit(f"مولّد تلقائياً من مترجم اللغة العربية البرمجية")
        # self.emit(f"Auto-generated from Arabic Programming Language Compiler")
        # self.emit(f'"""')
        # self.emit_blank()
        
        # Add imports
        self.emit("import sys")
        self.emit("import math")
        self.emit_blank()
        
        # Generate block code
        self.visit(node.block)
        
        # Add main execution
        self.emit_blank()
        self.emit("if __name__ == '__main__':")
        self.increase_indent()
        self.emit("main()")
        self.emit("print('exit')")
        self.decrease_indent()
    
    def visit_BlockNode(self, node):
        """توليد كود الكتلة - Generate block code"""
        # Constants
        if node.constants:
            self.emit("# ===== الثوابت - Constants =====")
            for const in node.constants:
                self.visit(const)
            self.emit_blank()
        
        # Types (as comments or class definitions)
        if node.types:
            self.emit("# ===== الأنواع - Types =====")
            for type_def in node.types:
                self.visit(type_def)
            self.emit_blank()
        
        # Variables (global variables)
        if node.variables and not self.in_procedure:
            self.emit("# ===== المتغيرات - Variables =====")
            for var in node.variables:
                self.visit(var)
            self.emit_blank()
        
        # Procedures
        if node.procedures:
            self.emit("# ===== الإجراءات - Procedures =====")
            for proc in node.procedures:
                self.visit(proc)
            self.emit_blank()
        
        # Main instructions
        if node.instructions:
            if not self.in_procedure:
                self.emit("# ===== البرنامج الرئيسي - Main Program =====")
                self.emit("def main():")
                self.increase_indent()
                
                # Declare variables if any
                if node.variables:
                    for var in node.variables:
                        self.visit_VarDeclNode_init(var)
                
            self.visit(node.instructions)
            
            if not self.in_procedure:
                self.decrease_indent()
    
    # ==================== Constants ====================
    
    def visit_ConstantDefNode(self, node):
        """توليد كود تعريف الثابت - Generate constant definition"""
        name = self.sanitize_name(node.name)
        value = self.format_value(node.value)
        self.emit(f"{name} = {value}  # ثابت - Constant")
    
    def format_value(self, value):
        """تنسيق القيمة - Format value"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return "True" if value else "False"
        elif value is None:
            return "None"
        else:
            return str(value)
    
    # ==================== Types ====================
    
    def visit_TypeDefNode(self, node):
        """توليد كود تعريف النوع - Generate type definition"""
        name = self.sanitize_name(node.name)
        
        if isinstance(node.type_spec, TypeInfo):
            if node.type_spec.is_record:
                # Generate class for record type
                self.emit(f"class {name}:")
                self.increase_indent()
                self.emit(f'"""سجل - Record type"""')
                self.emit("def __init__(self):")
                self.increase_indent()
                
                # Initialize fields
                for field_name, field_type in node.type_spec.fields.items():
                    default_value = self.get_default_value(field_type)
                    self.emit(f"self.{self.sanitize_name(field_name)} = {default_value}")
                
                self.decrease_indent()
                self.decrease_indent()
                self.emit_blank()
            
            elif node.type_spec.is_list:
                # Generate comment for list type
                self.emit(f"# {name}: قائمة من {node.type_spec.list_size} عنصر من نوع {node.type_spec.base_type}")
                self.emit(f"# {name}: List of {node.type_spec.list_size} elements of type {node.type_spec.base_type}")
    
    def get_default_value(self, type_info):
        """الحصول على القيمة الافتراضية للنوع - Get default value for type"""
        if isinstance(type_info, TypeInfo):
            base = type_info.base_type
        else:
            base = str(type_info)
        
        if base in ['صحيح', 'حقيقي']:
            return "0"
        elif base == 'منطقي':
            return "False"
        elif base == 'حرفي':
            return "''"
        elif base == 'خيط_رمزي':
            return '""'
        elif isinstance(type_info, TypeInfo) and type_info.is_list:
            size = type_info.list_size
            elem_default = self.get_default_value(type_info.base_type)
            return f"[{elem_default}] * {size}"
        elif isinstance(type_info, TypeInfo) and type_info.is_record:
            # Return None, will be initialized later
            return "None"
        else:
            return "None"
    
    # ==================== Variables ====================
    
    def visit_VarDeclNode(self, node):
        """توليد كود تعريف المتغير - Generate variable declaration"""
        # Just emit comment, actual initialization in visit_VarDeclNode_init
        names = ", ".join([self.sanitize_name(n) for n in node.names])
        self.emit(f"# {names}: {node.data_type}")
    
    def visit_VarDeclNode_init(self, node):
        """تهيئة المتغير - Initialize variable"""
        for name in node.names:
            sanitized = self.sanitize_name(name)
            # Try to get type info from symbol table or use basic default
            default_val = "None"
            
            # Map Arabic type names to defaults
            if node.data_type == 'صحيح':
                default_val = "0"
            elif node.data_type == 'حقيقي':
                default_val = "0.0"
            elif node.data_type == 'منطقي':
                default_val = "False"
            elif node.data_type == 'حرفي':
                default_val = "''"
            elif node.data_type == 'خيط_رمزي':
                default_val = '""'
            
            self.emit(f"{sanitized} = {default_val}")
    
    # ==================== Procedures ====================
    
    def visit_ProcedureDefNode(self, node):
        """توليد كود الإجراء - Generate procedure code"""
        proc_name = self.sanitize_name(node.name)
        
        # Generate parameter list
        params = []
        for param in node.params:
            param_names = [self.sanitize_name(n) for n in param.names]
            params.extend(param_names)
        
        param_str = ", ".join(params) if params else ""
        
        self.emit(f"def {proc_name}({param_str}):")
        self.increase_indent()
        self.emit(f'"""اجراء - Procedure: {node.name}"""')
        
        # Set flag
        old_in_proc = self.in_procedure
        self.in_procedure = True
        
        # Generate procedure body
        if node.block:
            # Handle variable declarations in procedure
            if node.block.variables:
                for var in node.block.variables:
                    self.visit_VarDeclNode_init(var)
            
            # Generate instructions
            if node.block.instructions:
                self.visit(node.block.instructions)
        else:
            self.emit("pass")
        
        self.in_procedure = old_in_proc
        self.decrease_indent()
        self.emit_blank()
    
    # ==================== Statements ====================
    
    def visit_CompoundStmtNode(self, node):
        """توليد كود العبارة المركبة - Generate compound statement"""
        for stmt in node.statements:
            if stmt:
                self.visit(stmt)
    
    def visit_AssignmentNode(self, node):
        """توليد كود الإسناد - Generate assignment"""
        var_code = self.visit(node.variable)
        expr_code = self.visit(node.expression)
        self.emit(f"{var_code} = {expr_code}")
    
    def visit_InputNode(self, node):
        """توليد كود القراءة - Generate input statement"""
        var_code = self.visit(node.variable)
        
        # Determine type for conversion
        type_str = "input"
        if hasattr(node.variable, 'expr_type') and node.variable.expr_type:
            base_type = node.variable.expr_type.base_type if isinstance(node.variable.expr_type, TypeInfo) else str(node.variable.expr_type)
            
            if base_type == 'صحيح':
                type_str = "int(input())"
            elif base_type == 'حقيقي':
                type_str = "float(input())"
            elif base_type == 'منطقي':
                type_str = "input().lower() in ['صح', 'true', '1', 'yes']"
            else:
                type_str = "input()"
        
        self.emit(f"{var_code} = {type_str}")
    
    def visit_OutputNode(self, node):
        """توليد كود الطباعة - Generate output statement"""
        items = []
        for item in node.items:
            item_code = self.visit(item)
            items.append(item_code)
        
        items_str = ", ".join(items)
        self.emit(f"print({items_str})")
    
    def visit_CallNode(self, node):
        """توليد كود استدعاء الإجراء - Generate procedure call"""
        proc_name = self.sanitize_name(node.procedure_name)
        
        args = []
        for arg in node.arguments:
            arg_code = self.visit(arg)
            args.append(arg_code)
        
        args_str = ", ".join(args)
        self.emit(f"{proc_name}({args_str})")
    
    # ==================== Control Flow ====================
    
    def visit_IfNode(self, node):
        """توليد كود الشرط - Generate if statement"""
        # Main if
        condition_code = self.visit(node.condition)
        self.emit(f"if {condition_code}:")
        self.increase_indent()
        
        if node.then_stmt:
            self.visit(node.then_stmt)
        else:
            self.emit("pass")
        
        self.decrease_indent()
        
        # Elif parts
        for elif_cond, elif_stmt in node.elif_parts:
            elif_cond_code = self.visit(elif_cond)
            self.emit(f"elif {elif_cond_code}:")
            self.increase_indent()
            
            if elif_stmt:
                self.visit(elif_stmt)
            else:
                self.emit("pass")
            
            self.decrease_indent()
        
        # Else part
        if node.else_stmt:
            self.emit("else:")
            self.increase_indent()
            self.visit(node.else_stmt)
            self.decrease_indent()
    
    def visit_ForLoopNode(self, node):
        """توليد كود حلقة for - Generate for loop"""
        loop_var = self.sanitize_name(node.loop_var)
        start_code = self.visit(node.start_expr)
        end_code = self.visit(node.end_expr)
        
        if node.step_expr:
            step_code = self.visit(node.step_expr)
            self.emit(f"for {loop_var} in range({start_code}, {end_code} + 1, {step_code}):")
        else:
            self.emit(f"for {loop_var} in range({start_code}, {end_code} + 1):")
        
        self.increase_indent()
        
        if node.body:
            self.visit(node.body)
        else:
            self.emit("pass")
        
        self.decrease_indent()
    
    def visit_WhileLoopNode(self, node):
        """توليد كود حلقة while - Generate while loop"""
        condition_code = self.visit(node.condition)
        self.emit(f"while {condition_code}:")
        self.increase_indent()
        
        if node.body:
            self.visit(node.body)
        else:
            self.emit("pass")
        
        self.decrease_indent()
    
    def visit_RepeatUntilNode(self, node):
        """توليد كود حلقة repeat-until - Generate repeat-until loop"""
        # Repeat-until is do-while equivalent
        # Generate as while True with break condition
        self.emit("while True:")
        self.increase_indent()
        
        if node.body:
            self.visit(node.body)
        
        # Add break condition
        condition_code = self.visit(node.condition)
        self.emit(f"if {condition_code}:")
        self.increase_indent()
        self.emit("break")
        self.decrease_indent()
        
        self.decrease_indent()
    
    # ==================== Expressions ====================
    
    def visit_BinOpNode(self, node):
        """توليد كود العملية الثنائية - Generate binary operation"""
        left_code = self.visit(node.left)
        right_code = self.visit(node.right)
        op = self.convert_operator(node.operator)
        
        return f"({left_code} {op} {right_code})"
    
    def visit_UnaryOpNode(self, node):
        """توليد كود العملية الأحادية - Generate unary operation"""
        operand_code = self.visit(node.operand)
        op = self.convert_operator(node.operator)
        
        return f"({op}{operand_code})"
    
    def convert_operator(self, op):
        """تحويل العامل - Convert operator"""
        op_map = {
            '==': '==',
            '=!': '!=',
            '>=': '>=',
            '<=': '<=',
            '>': '>',
            '<': '<',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '\\': '//',
            '%': '%',
            '^': '**',
            '&&': 'and',
            '||': 'or',
            '!': 'not '
        }
        return op_map.get(op, op)
    
    def visit_VarAccessNode(self, node):
        """توليد كود الوصول للمتغير - Generate variable access"""
        var_name = self.sanitize_name(node.name)
        
        if node.selector:
            selector_code = self.visit(node.selector)
            return f"{var_name}{selector_code}"
        
        return var_name
    
    def visit_IndexedSelectorNode(self, node):
        """توليد كود الوصول المفهرس - Generate indexed access"""
        index_code = self.visit(node.index_expr)
        return f"[{index_code}]"
    
    def visit_FieldSelectorNode(self, node):
        """توليد كود الوصول للحقل - Generate field access"""
        field_name = self.sanitize_name(node.field_name)
        return f".{field_name}"
    
    # ==================== Literals ====================
    
    def visit_LiteralNode(self, node):
        """توليد كود القيمة الحرفية - Generate literal"""
        if node.literal_type in ['صحيح', 'حقيقي']:
            return str(node.value)
        elif node.literal_type == 'منطقي':
            return "True" if node.value else "False"
        elif node.literal_type == 'خيط_رمزي':
            # Escape quotes
            escaped = node.value.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        elif node.literal_type == 'حرفي':
            escaped = node.value.replace('\\', '\\\\').replace("'", "\\'")
            return f"'{escaped}'"
        else:
            return str(node.value)
    
    def visit_ConstantRefNode(self, node):
        """توليد كود مرجع الثابت - Generate constant reference"""
        return self.sanitize_name(node.name)


def generate_code(ast, output_file=None):
    """
    توليد الكود من شجرة AST - Generate code from AST
    
    Args:
        ast: شجرة AST - AST tree
        output_file: ملف الإخراج (اختياري) - Output file (optional)
    
    Returns:
        str: الكود المولّد - Generated code
    """
    generator = CodeGenerator()
    code = generator.generate(ast)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"✓ تم توليد الكود في: {output_file}")
        print(f"✓ Code generated in: {output_file}")
    
    return code


if __name__ == "__main__":
    print("مولد الكود الوسيط للغة العربية البرمجية")
    print("Arabic Programming Language Code Generator")
    print("=" * 50)
