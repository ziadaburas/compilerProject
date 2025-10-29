
"""
Semantic Analyzer for Arabic Programming Language
المحلل الدلالي - يبني شجرة AST ويفحص الأخطاء الدلالية
"""

# NOTE: This assumes you have generated the parser files using ANTLR4
# Generate them using: antlr4 -Dlanguage=Python3 -visitor ArabicGrammar.g4
try:
    from ArabicGrammarParser import ArabicGrammarParser
    from ArabicGrammarVisitor import ArabicGrammarVisitor
except ImportError:
    # If ANTLR files are not generated yet, create placeholder classes
    print("تحذير: ملفات ANTLR غير موجودة. يرجى توليدها أولاً باستخدام:")
    print("antlr4 -Dlanguage=Python3 -visitor ArabicGrammar.g4")
    
    class ArabicGrammarParser:
        pass
    
    class ArabicGrammarVisitor:
        def visitChildren(self, ctx):
            return None

from ast_nodes import *
from symbol_table import SymbolTable, Symbol, ParamSymbol, TypeInfo, SemanticError, TypeChecker


class SemanticAnalyzer(ArabicGrammarVisitor):
    """المحلل الدلالي - Semantic Analyzer Visitor"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_procedure = None
        self.errors = []
    
    def add_error(self, message, ctx=None):
        """إضافة خطأ دلالي - Add semantic error"""
        line = ctx.start.line if ctx else None
        column = ctx.start.column if ctx else None
        error = SemanticError(message, line, column)
        self.errors.append(error)
        return error
    
    # ==================== Program & Block ====================
    
    def visitProgram(self, ctx):
        """زيارة برنامج - Visit program node"""
        program_name = ctx.ID().getText()
        block = self.visit(ctx.block())
        
        return ProgramNode(
            name=program_name,
            block=block,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitBlock(self, ctx):
        """زيارة كتلة - Visit block node"""
        constants = []
        types = []
        variables = []
        procedures = []
        
        # Visit definitions
        if ctx.definitions_part():
            defs = self.visit(ctx.definitions_part())
            constants = defs.get('constants', [])
            types = defs.get('types', [])
            variables = defs.get('variables', [])
            procedures = defs.get('procedures', [])
        
        # Visit instructions
        instructions = self.visit(ctx.instructions_list()) if ctx.instructions_list() else []
        
        return BlockNode(
            constants=constants,
            types=types,
            variables=variables,
            procedures=procedures,
            instructions=instructions,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitDefinitions_part(self, ctx):
        """زيارة جزء التعريفات - Visit definitions part"""
        result = {
            'constants': [],
            'types': [],
            'variables': [],
            'procedures': []
        }
        
        # Constants
        if ctx.constants_definition():
            result['constants'] = self.visit(ctx.constants_definition())
        
        # Types
        if ctx.types_definition():
            result['types'] = self.visit(ctx.types_definition())
        
        # Variables
        if ctx.variables_definition():
            result['variables'] = self.visit(ctx.variables_definition())
        
        # Procedures
        if ctx.procedures_definition():
            result['procedures'] = self.visit(ctx.procedures_definition())
        
        return result
    
    # ==================== Constants ====================
    
    def visitConstants_definition(self, ctx):
        """زيارة تعريفات الثوابت - Visit constants definition"""
        constants = []
        for const_def_ctx in ctx.constant_def():
            const_node = self.visit(const_def_ctx)
            if const_node:
                constants.append(const_node)
        return constants
    
    def visitConstant_def(self, ctx):
        """زيارة تعريف ثابت - Visit constant definition"""
        const_name = ctx.ID().getText()
        const_node = self.visit(ctx.constant_value())
        
        # Check if already defined
        if self.symbol_table.is_defined(const_name):
            self.add_error(f"الثابت '{const_name}' معرّف مسبقاً", ctx)
            return None
        
        # Determine data_type and value from node
        data_type = None
        value = None
        if hasattr(const_node, 'expr_type') and const_node.expr_type is not None:
            data_type = const_node.expr_type
        if hasattr(const_node, 'value'):
            value = const_node.value

        # Add to symbol table
        symbol = Symbol(
            name=const_name,
            symbol_type='CONSTANT',
            data_type=data_type,
            value=value,
            is_constant=True
        )
        self.symbol_table.insert(symbol)
        
        return ConstantDefNode(
            name=const_name,
            value=value,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitConstant_value(self, ctx):
        """زيارة قيمة ثابتة - Visit constant value"""
        if ctx.numeric_value():
            return self.visit(ctx.numeric_value())
        elif ctx.literal_value():
            return self.visit(ctx.literal_value())
        elif ctx.logical_value():
            return self.visit(ctx.logical_value())
        elif ctx.ID():
            # Reference to another constant
            const_name = ctx.ID().getText()
            if not self.symbol_table.is_constant(const_name):
                self.add_error(f"'{const_name}' ليس ثابتاً معرّفاً", ctx)
                return None
            # return a constant reference node with its type
            sym = self.symbol_table.lookup(const_name)
            node = ConstantRefNode(name=const_name, line=ctx.start.line, column=ctx.start.column)
            node.expr_type = sym.data_type if sym else None
            # if constant has a stored primitive value, attach it
            if sym and sym.value is not None:
                node.value = sym.value
            return node
        return None
    
    # ==================== Types ====================
    
    def visitTypes_definition(self, ctx):
        """زيارة تعريفات الأنواع - Visit types definition"""
        types = []
        for type_def_ctx in ctx.type_def():
            type_node = self.visit(type_def_ctx)
            if type_node:
                types.append(type_node)
        return types
    
    def visitType_def(self, ctx):
        """زيارة تعريف نوع - Visit type definition"""
        type_name = ctx.ID().getText()
        
        # Check if already defined
        if self.symbol_table.is_defined(type_name):
            self.add_error(f"النوع '{type_name}' معرّف مسبقاً", ctx)
            return None
        
        type_spec = self.visit(ctx.composite_type())
        
        # Add to symbol table
        symbol = Symbol(
            name=type_name,
            symbol_type='TYPE',
            data_type=type_spec
        )
        self.symbol_table.insert(symbol)
        
        return TypeDefNode(
            name=type_name,
            type_spec=type_spec,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitComposite_type(self, ctx):
        """زيارة نوع مركب - Visit composite type"""
        if ctx.list_type():
            return self.visit(ctx.list_type())
        elif ctx.record_type():
            return self.visit(ctx.record_type())
        return None
    
    def visitList_type(self, ctx):
        """زيارة نوع قائمة - Visit list type"""
        size = int(ctx.INTEGER().getText())
        element_type_name = self.visit(ctx.data_type())
        
        # Resolve element type
        element_type = self.symbol_table.lookup_type(element_type_name)
        if not element_type:
            self.add_error(f"النوع '{element_type_name}' غير معرّف", ctx)
            element_type = TypeInfo('صحيح')  # Default fallback
        
        type_info = TypeInfo(
            base_type=element_type_name,
            is_list=True,
            list_size=size
        )
        
        return type_info
    
    def visitRecord_type(self, ctx):
        """زيارة نوع سجل - Visit record type"""
        fields_dict = {}
        
        if ctx.fields_list():
            fields = self.visit(ctx.fields_list())
            for field_node in fields:
                for name in field_node.names:
                    if name in fields_dict:
                        self.add_error(f"الحقل '{name}' معرّف مسبقاً في السجل", ctx)
                    else:
                        # Resolve field type
                        field_type = self.symbol_table.lookup_type(field_node.data_type)
                        if not field_type:
                            field_type = TypeInfo(field_node.data_type)
                        fields_dict[name] = field_type
        
        type_info = TypeInfo(
            base_type='سجل',
            is_record=True,
            fields=fields_dict
        )
        
        return type_info
    
    def visitFields_list(self, ctx):
        """زيارة قائمة الحقول - Visit fields list"""
        fields = []
        for field_ctx in ctx.field_def():
            field_node = self.visit(field_ctx)
            if field_node:
                fields.append(field_node)
        return fields
    
    def visitField_def(self, ctx):
        """زيارة تعريف حقل - Visit field definition"""
        names = [id_node.getText() for id_node in ctx.ID()]
        data_type = self.visit(ctx.data_type())
        
        return FieldDefNode(
            names=names,
            data_type=data_type,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    # ==================== Variables ====================
    
    def visitVariables_definition(self, ctx):
        """زيارة تعريفات المتغيرات - Visit variables definition"""
        variables = []
        for var_def_ctx in ctx.variable_def():
            var_node = self.visit(var_def_ctx)
            if var_node:
                variables.append(var_node)
        return variables
    
    def visitVariable_def(self, ctx):
        """زيارة تعريف متغير - Visit variable definition"""
        return self.visit(ctx.variables_group())
    
    def visitVariables_group(self, ctx):
        """زيارة مجموعة متغيرات - Visit variables group"""
        names = [id_node.getText() for id_node in ctx.ID()]
        data_type_name = self.visit(ctx.data_type())
        
        # Resolve type
        data_type = self.symbol_table.lookup_type(data_type_name)
        if not data_type:
            self.add_error(f"النوع '{data_type_name}' غير معرّف", ctx)
            data_type = TypeInfo('صحيح')  # Default fallback
        
        # Add each variable to symbol table
        for name in names:
            if self.symbol_table.lookup(name, current_scope_only=True):
                self.add_error(f"المتغير '{name}' معرّف مسبقاً في هذا النطاق", ctx)
                continue
            
            symbol = Symbol(
                name=name,
                symbol_type='VARIABLE',
                data_type=data_type
            )
            self.symbol_table.insert(symbol)
        
        return VarDeclNode(
            names=names,
            data_type=data_type_name,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitData_type(self, ctx):
        """زيارة نوع بيانات - Visit data type"""
        if ctx.DT_INTEGER():
            return 'صحيح'
        elif ctx.DT_REAL():
            return 'حقيقي'
        elif ctx.DT_LOGICAL():
            return 'منطقي'
        elif ctx.DT_CHAR():
            return 'حرفي'
        elif ctx.DT_STRING():
            return 'خيط_رمزي'
        elif ctx.ID():
            return ctx.ID().getText()
        return 'صحيح'  # Default
    
    # ==================== Procedures ====================
    
    def visitProcedures_definition(self, ctx):
        """زيارة تعريفات الإجراءات - Visit procedures definition"""
        procedures = []
        for proc_def_ctx in ctx.procedure_def():
            proc_node = self.visit(proc_def_ctx)
            if proc_node:
                procedures.append(proc_node)
        return procedures
    
    def visitProcedure_def(self, ctx):
        """زيارة تعريف إجراء - Visit procedure definition"""
        # First pass: register procedure in symbol table
        proc_header = ctx.procedure_header()
        proc_name = proc_header.ID().getText()
        
        # Check if already defined
        if self.symbol_table.lookup(proc_name, current_scope_only=True):
            self.add_error(f"الإجراء '{proc_name}' معرّف مسبقاً", ctx)
            return None
        
        # Get parameters
        params = []
        if proc_header.formal_params_list():
            params = self.visit(proc_header.formal_params_list())
        
        # Add procedure to symbol table
        symbol = Symbol(
            name=proc_name,
            symbol_type='PROCEDURE',
            params=params
        )
        self.symbol_table.insert(symbol)
        
        # Enter new scope for procedure body
        self.symbol_table.enter_scope()
        self.current_procedure = proc_name
        
        # Add parameters to new scope
        for param in params:
            self.symbol_table.insert(Symbol(
                name=param.name,
                symbol_type='PARAMETER',
                data_type=param.data_type
            ))
        
        # Visit procedure body
        proc_block = self.visit(ctx.procedure_block())
        
        # Exit procedure scope
        self.symbol_table.exit_scope()
        self.current_procedure = None
        
        return ProcedureDefNode(
            name=proc_name,
            params=params,
            block=proc_block,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitFormal_params_list(self, ctx):
        """زيارة قائمة المعاملات - Visit formal parameters list"""
        params = []
        for param_ctx in ctx.param_def():
            param_nodes = self.visit(param_ctx)
            if param_nodes:
                params.extend(param_nodes)
        return params
    
    def visitParam_def(self, ctx):
        """زيارة تعريف معامل - Visit parameter definition"""
        # Get pass mode
        pass_mode = 'BY_VALUE'
        if ctx.BY_REFERENCE():
            pass_mode = 'BY_REFERENCE'
        elif ctx.BY_VALUE():
            pass_mode = 'BY_VALUE'
        
        # Get variables group
        var_group = self.visit(ctx.variables_group())
        
        # Create parameter symbols
        params = []
        for name in var_group.names:
            data_type = self.symbol_table.lookup_type(var_group.data_type)
            if not data_type:
                data_type = TypeInfo(var_group.data_type)
            
            param = ParamSymbol(
                name=name,
                data_type=data_type,
                pass_mode=pass_mode
            )
            params.append(param)
        
        return params
    
    def visitProcedure_block(self, ctx):
        """زيارة كتلة إجراء - Visit procedure block"""
        return self.visit(ctx.block())
    
    # ==================== Statements ====================
    
    def visitInstructions_list(self, ctx):
        """زيارة قائمة التعليمات - Visit instructions list"""
        instructions = []
        for instr_ctx in ctx.instruction():
            instr = self.visit(instr_ctx)
            if instr:
                instructions.append(instr)
        
        return CompoundStmtNode(
            statements=instructions,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitInstruction(self, ctx):
        """زيارة تعليمة - Visit instruction"""
        if ctx.assignment_statement():
            return self.visit(ctx.assignment_statement())
        elif ctx.input_statement():
            return self.visit(ctx.input_statement())
        elif ctx.output_statement():
            return self.visit(ctx.output_statement())
        elif ctx.call_statement():
            return self.visit(ctx.call_statement())
        elif ctx.conditional_statement():
            return self.visit(ctx.conditional_statement())
        elif ctx.loop_statement():
            return self.visit(ctx.loop_statement())
        elif ctx.instructions_list():
            return self.visit(ctx.instructions_list())
        return None  # Empty statement
    
    def visitAssignment_statement(self, ctx):
        """زيارة عبارة إسناد - Visit assignment statement"""
        variable = self.visit(ctx.variable_access())
        expression = self.visit(ctx.expression())
        
        # Type checking
        if variable and expression:
            var_type = variable.expr_type
            expr_type = expression.expr_type
            
            if var_type and expr_type:
                if not TypeChecker.are_compatible(expr_type, var_type):
                    self.add_error(
                        f"عدم توافق الأنواع في الإسناد: لا يمكن إسناد {expr_type} إلى {var_type}",
                        ctx
                    )
        
        return AssignmentNode(
            variable=variable,
            expression=expression,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitInput_statement(self, ctx):
        """زيارة عبارة قراءة - Visit input statement"""
        variable = self.visit(ctx.variable_access())
        
        return InputNode(
            variable=variable,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitOutput_statement(self, ctx):
        """زيارة عبارة طباعة - Visit output statement"""
        items = self.visit(ctx.print_list())
        
        return OutputNode(
            items=items,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitPrint_list(self, ctx):
        """زيارة قائمة الطباعة - Visit print list"""
        items = []
        for item_ctx in ctx.print_item():
            item = self.visit(item_ctx)
            if item:
                items.append(item)
        return items
    
    def visitPrint_item(self, ctx):
        """زيارة عنصر طباعة - Visit print item"""
        if ctx.variable_access():
            return self.visit(ctx.variable_access())
        elif ctx.literal_value():
            return self.visit(ctx.literal_value())
        return None
    
    def visitCall_statement(self, ctx):
        """زيارة استدعاء إجراء - Visit call statement"""
        proc_name = ctx.ID().getText()
        
        # Check if procedure exists
        if not self.symbol_table.is_procedure(proc_name):
            self.add_error(f"الإجراء '{proc_name}' غير معرّف", ctx)
            return None
        
        # Get actual arguments
        arguments = []
        if ctx.actual_params_list():
            arguments = self.visit(ctx.actual_params_list())
        
        # Get expected parameters
        expected_params = self.symbol_table.get_procedure_params(proc_name)
        
        # Check parameter count
        if len(arguments) != len(expected_params):
            self.add_error(
                f"عدد المعاملات غير صحيح للإجراء '{proc_name}': "
                f"متوقع {len(expected_params)}، موجود {len(arguments)}",
                ctx
            )
        else:
            # Check parameter types
            for i, (arg, param) in enumerate(zip(arguments, expected_params)):
                if hasattr(arg, 'expr_type') and arg.expr_type:
                    if not TypeChecker.are_compatible(arg.expr_type, param.data_type):
                        self.add_error(
                            f"عدم توافق النوع للمعامل {i+1} في استدعاء '{proc_name}'",
                            ctx
                        )
        
        return CallNode(
            procedure_name=proc_name,
            arguments=arguments,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitActual_params_list(self, ctx):
        """زيارة قائمة المعاملات الفعلية - Visit actual parameters list"""
        params = []
        for param_ctx in ctx.actual_param():
            param = self.visit(param_ctx)
            if param:
                params.append(param)
        return params
    
    def visitActual_param(self, ctx):
        """زيارة معامل فعلي - Visit actual parameter"""
        if ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.variable_access():
            return self.visit(ctx.variable_access())
        return None
    
    # ==================== Control Flow ====================
    
    def visitConditional_statement(self, ctx):
        """زيارة عبارة شرطية - Visit conditional statement"""
        condition = self.visit(ctx.condition(0))
        then_stmt = self.visit(ctx.instruction(0))
        
        # Check condition type
        if condition and hasattr(condition, 'expr_type'):
            if not TypeChecker.is_boolean(condition.expr_type):
                self.add_error("الشرط يجب أن يكون من نوع منطقي", ctx)
        
        # Handle elif parts
        elif_parts = []
        elif_conditions = ctx.condition()[1:]
        elif_stmts = ctx.instruction()[1:-1] if ctx.ELSE() else ctx.instruction()[1:]
        
        for elif_cond_ctx, elif_stmt_ctx in zip(elif_conditions, elif_stmts):
            elif_cond = self.visit(elif_cond_ctx)
            elif_stmt = self.visit(elif_stmt_ctx)
            elif_parts.append((elif_cond, elif_stmt))
        
        # Handle else part
        else_stmt = None
        if ctx.ELSE() and len(ctx.instruction()) > len(ctx.condition()):
            else_stmt = self.visit(ctx.instruction()[-1])
        
        return IfNode(
            condition=condition,
            then_stmt=then_stmt,
            elif_parts=elif_parts,
            else_stmt=else_stmt,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitCondition(self, ctx):
        """زيارة شرط - Visit condition"""
        return self.visit(ctx.expression())
    
    def visitLoop_statement(self, ctx):
        """زيارة عبارة حلقة - Visit loop statement"""
        if ctx.for_loop_statement():
            return self.visit(ctx.for_loop_statement())
        elif ctx.while_loop_statement():
            return self.visit(ctx.while_loop_statement())
        elif ctx.repeat_until_statement():
            return self.visit(ctx.repeat_until_statement())
        return None
    
    def visitFor_loop_statement(self, ctx):
        """زيارة حلقة for - Visit for loop"""
        iteration = self.visit(ctx.iteration_range())
        body = self.visit(ctx.instruction())
        
        return ForLoopNode(
            loop_var=iteration['var'],
            start_expr=iteration['start'],
            end_expr=iteration['end'],
            step_expr=iteration['step'],
            body=body,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitIteration_range(self, ctx):
        """زيارة نطاق التكرار - Visit iteration range"""
        loop_var = ctx.ID().getText()
        start_expr = self.visit(ctx.expression(0))
        end_expr = self.visit(ctx.expression(1))
        step_expr = self.visit(ctx.expression(2)) if len(ctx.expression()) > 2 else None
        
        # Check if loop variable is defined
        if not self.symbol_table.is_variable(loop_var):
            self.add_error(f"متغير الحلقة '{loop_var}' غير معرّف", ctx)
        
        # Check types
        if start_expr and hasattr(start_expr, 'expr_type'):
            if not TypeChecker.is_numeric(start_expr.expr_type):
                self.add_error("قيمة البداية يجب أن تكون رقمية", ctx)
        
        if end_expr and hasattr(end_expr, 'expr_type'):
            if not TypeChecker.is_numeric(end_expr.expr_type):
                self.add_error("قيمة النهاية يجب أن تكون رقمية", ctx)
        
        return {
            'var': loop_var,
            'start': start_expr,
            'end': end_expr,
            'step': step_expr
        }
    
    def visitWhile_loop_statement(self, ctx):
        """زيارة حلقة while - Visit while loop"""
        condition = self.visit(ctx.condition())
        body = self.visit(ctx.instruction())
        
        # Check condition type
        if condition and hasattr(condition, 'expr_type'):
            if not TypeChecker.is_boolean(condition.expr_type):
                self.add_error("شرط الحلقة يجب أن يكون من نوع منطقي", ctx)
        
        return WhileLoopNode(
            condition=condition,
            body=body,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitRepeat_until_statement(self, ctx):
        """زيارة حلقة repeat-until - Visit repeat-until loop"""
        body = self.visit(ctx.instruction())
        condition = self.visit(ctx.condition())
        
        # Check condition type
        if condition and hasattr(condition, 'expr_type'):
            if not TypeChecker.is_boolean(condition.expr_type):
                self.add_error("شرط الحلقة يجب أن يكون من نوع منطقي", ctx)
        
        return RepeatUntilNode(
            body=body,
            condition=condition,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    # ==================== Expressions ====================
    
    def visitExpression(self, ctx):
        """زيارة تعبير - Visit expression"""
        left = self.visit(ctx.simple_expression(0))
        
        if ctx.relational_op():
            operator = self.visit(ctx.relational_op())
            right = self.visit(ctx.simple_expression(1))
            
            # Type checking
            result_type = None
            if left and right and hasattr(left, 'expr_type') and hasattr(right, 'expr_type'):
                result_type = TypeChecker.get_result_type(operator, left.expr_type, right.expr_type)
                if not result_type:
                    self.add_error(f"عملية غير صالحة: {operator} بين {left.expr_type} و {right.expr_type}", ctx)
                    result_type = TypeInfo('منطقي')  # Default
            
            node = BinOpNode(
                left=left,
                operator=operator,
                right=right,
                line=ctx.start.line,
                column=ctx.start.column
            )
            node.expr_type = result_type
            return node
        
        return left
    
    def visitSimple_expression(self, ctx):
        """زيارة تعبير بسيط - Visit simple expression"""
        # Handle unary sign
        sign = None
        if ctx.sign():
            sign = self.visit(ctx.sign())
        
        left = self.visit(ctx.term(0))
        
        # Apply sign if present
        if sign and left:
            if hasattr(left, 'expr_type') and not TypeChecker.is_numeric(left.expr_type):
                self.add_error(f"لا يمكن تطبيق علامة {sign} على نوع غير رقمي", ctx)
            
            left = UnaryOpNode(
                operator=sign,
                operand=left,
                line=ctx.start.line,
                column=ctx.start.column
            )
            if hasattr(left.operand, 'expr_type'):
                left.expr_type = left.operand.expr_type
        
        # Handle binary operations
        for i, add_op_ctx in enumerate(ctx.add_op()):
            operator = self.visit(add_op_ctx)
            right = self.visit(ctx.term(i + 1))
            
            # Type checking
            result_type = None
            if left and right and hasattr(left, 'expr_type') and hasattr(right, 'expr_type'):
                result_type = TypeChecker.get_result_type(operator, left.expr_type, right.expr_type)
                if not result_type:
                    self.add_error(f"عملية غير صالحة: {operator} بين {left.expr_type} و {right.expr_type}", ctx)
            
            left = BinOpNode(
                left=left,
                operator=operator,
                right=right,
                line=ctx.start.line,
                column=ctx.start.column
            )
            left.expr_type = result_type
        
        return left
    
    def visitTerm(self, ctx):
        """زيارة حد - Visit term"""
        left = self.visit(ctx.factor(0))
        
        for i, mul_op_ctx in enumerate(ctx.mul_op()):
            operator = self.visit(mul_op_ctx)
            right = self.visit(ctx.factor(i + 1))
            
            # Type checking
            result_type = None
            if left and right and hasattr(left, 'expr_type') and hasattr(right, 'expr_type'):
                result_type = TypeChecker.get_result_type(operator, left.expr_type, right.expr_type)
                if not result_type:
                    self.add_error(f"عملية غير صالحة: {operator} بين {left.expr_type} و {right.expr_type}", ctx)
            
            left = BinOpNode(
                left=left,
                operator=operator,
                right=right,
                line=ctx.start.line,
                column=ctx.start.column
            )
            left.expr_type = result_type
        
        return left
    
    def visitFactor(self, ctx):
        """زيارة عامل - Visit factor"""
        if ctx.variable_access():
            return self.visit(ctx.variable_access())
        elif ctx.constant_value():
            return self.visit(ctx.constant_value())
        elif ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.NOT():
            operand = self.visit(ctx.factor())
            
            # Type checking
            if operand and hasattr(operand, 'expr_type'):
                if not TypeChecker.is_boolean(operand.expr_type):
                    self.add_error("عملية النفي (!) تحتاج نوع منطقي", ctx)
            
            node = UnaryOpNode(
                operator='!',
                operand=operand,
                line=ctx.start.line,
                column=ctx.start.column
            )
            node.expr_type = TypeInfo('منطقي')
            return node
        
        return None
    
    def visitVariable_access(self, ctx):
        """زيارة الوصول لمتغير - Visit variable access"""
        var_name = ctx.ID().getText()
        
        # Check if variable is defined
        if not self.symbol_table.is_defined(var_name):
            self.add_error(f"المتغير '{var_name}' غير معرّف", ctx)
            return None
        
        # Get variable type
        var_type = self.symbol_table.get_type(var_name)
        
        selector = None
        if ctx.selector():
            selector = self.visit(ctx.selector())
            
            # Handle indexed selector
            if isinstance(selector, IndexedSelectorNode):
                if not var_type or not var_type.is_list:
                    self.add_error(f"'{var_name}' ليس قائمة", ctx)
                else:
                    # Type becomes element type
                    var_type = self.symbol_table.lookup_type(var_type.base_type)
            
            # Handle field selector
            elif isinstance(selector, FieldSelectorNode):
                if not var_type or not var_type.is_record:
                    self.add_error(f"'{var_name}' ليس سجلاً", ctx)
                elif selector.field_name not in var_type.fields:
                    self.add_error(f"الحقل '{selector.field_name}' غير موجود في السجل", ctx)
                else:
                    var_type = var_type.fields[selector.field_name]
        
        node = VarAccessNode(
            name=var_name,
            selector=selector,
            line=ctx.start.line,
            column=ctx.start.column
        )
        node.expr_type = var_type
        return node
    
    def visitSelector(self, ctx):
        """زيارة محدد - Visit selector"""
        if ctx.indexed_selector():
            return self.visit(ctx.indexed_selector())
        elif ctx.field_selector():
            return self.visit(ctx.field_selector())
        return None
    
    def visitIndexed_selector(self, ctx):
        """زيارة محدد مفهرس - Visit indexed selector"""
        index_expr = self.visit(ctx.expression())
        
        # Check index type
        if index_expr and hasattr(index_expr, 'expr_type'):
            if not TypeChecker.is_numeric(index_expr.expr_type):
                self.add_error("الفهرس يجب أن يكون رقمياً", ctx)
        
        return IndexedSelectorNode(
            index_expr=index_expr,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    def visitField_selector(self, ctx):
        """زيارة محدد حقل - Visit field selector"""
        field_name = ctx.ID().getText()
        
        return FieldSelectorNode(
            field_name=field_name,
            line=ctx.start.line,
            column=ctx.start.column
        )
    
    # ==================== Literals & Values ====================
    
    def visitConstant_value(self, ctx):
        """زيارة قيمة ثابتة في تعبير - Visit constant value in expression"""
        if ctx.numeric_value():
            return self.visit(ctx.numeric_value())
        elif ctx.literal_value():
            return self.visit(ctx.literal_value())
        elif ctx.logical_value():
            return self.visit(ctx.logical_value())
        elif ctx.ID():
            # Reference to a constant
            const_name = ctx.ID().getText()
            if self.symbol_table.is_constant(const_name):
                const_value = self.symbol_table.get_constant_value(const_name)
                const_type = self.symbol_table.get_type(const_name)
                
                node = ConstantRefNode(
                    name=const_name,
                    line=ctx.start.line,
                    column=ctx.start.column
                )
                node.expr_type = const_type
                return node
            else:
                self.add_error(f"الثابت '{const_name}' غير معرّف", ctx)
        
        return None
    
    def visitNumeric_value(self, ctx):
        """زيارة قيمة رقمية - Visit numeric value"""
        if ctx.REAL_NUMBER():
            value = float(ctx.REAL_NUMBER().getText())
            node = LiteralNode(
                value=value,
                literal_type='حقيقي',
                line=ctx.start.line,
                column=ctx.start.column
            )
            # assign TypeInfo
            node.expr_type = self.symbol_table.lookup_type('حقيقي') or TypeInfo('حقيقي')
            return node
        elif ctx.INTEGER():
            value = int(ctx.INTEGER().getText())
            node = LiteralNode(
                value=value,
                literal_type='صحيح',
                line=ctx.start.line,
                column=ctx.start.column
            )
            node.expr_type = self.symbol_table.lookup_type('صحيح') or TypeInfo('صحيح')
            return node
        return None
    
    def visitLiteral_value(self, ctx):
        """زيارة قيمة حرفية - Visit literal value"""
        if ctx.STRING_LITERAL():
            text = ctx.STRING_LITERAL().getText()
            value = text[1:-1]  # Remove quotes
            node = LiteralNode(
                value=value,
                literal_type='خيط_رمزي',
                line=ctx.start.line,
                column=ctx.start.column
            )
            node.expr_type = self.symbol_table.lookup_type('خيط_رمزي') or TypeInfo('خيط_رمزي')
            return node
        elif ctx.CHAR_LITERAL():
            text = ctx.CHAR_LITERAL().getText()
            value = text[1:-1]  # Remove quotes
            node = LiteralNode(
                value=value,
                literal_type='حرفي',
                line=ctx.start.line,
                column=ctx.start.column
            )
            node.expr_type = self.symbol_table.lookup_type('حرفي') or TypeInfo('حرفي')
            return node
        return None
    
    def visitLogical_value(self, ctx):
        """زيارة قيمة منطقية - Visit logical value"""
        if ctx.TRUE():
            node = LiteralNode(
                value=True,
                literal_type='منطقي',
                line=ctx.start.line,
                column=ctx.start.column
            )
            node.expr_type = self.symbol_table.lookup_type('منطقي') or TypeInfo('منطقي')
            return node
        elif ctx.FALSE():
            node = LiteralNode(
                value=False,
                literal_type='منطقي',
                line=ctx.start.line,
                column=ctx.start.column
            )
            node.expr_type = self.symbol_table.lookup_type('منطقي') or TypeInfo('منطقي')
            return node
        return None
    
    # ==================== Operators ====================
    
    def visitRelational_op(self, ctx):
        """زيارة عامل علاقي - Visit relational operator"""
        if ctx.GT(): return '>'
        elif ctx.LT(): return '<'
        elif ctx.GTE(): return '>='
        elif ctx.LTE(): return '<='
        elif ctx.EQUALS_OP(): return '=='
        elif ctx.NOT_EQUALS_OP(): return '=!'
        return None
    
    def visitSign(self, ctx):
        """زيارة علامة - Visit sign"""
        if ctx.PLUS(): return '+'
        elif ctx.MINUS(): return '-'
        return None
    
    def visitAdd_op(self, ctx):
        """زيارة عامل جمع - Visit addition operator"""
        if ctx.PLUS(): return '+'
        elif ctx.MINUS(): return '-'
        elif ctx.OR(): return '||'
        return None
    
    def visitMul_op(self, ctx):
        """زيارة عامل ضرب - Visit multiplication operator"""
        if ctx.MULT(): return '*'
        elif ctx.DIV(): return '/'
        elif ctx.INT_DIV(): return '\\'
        elif ctx.MOD(): return '%'
        elif ctx.AND(): return '&&'
        return None
