"""
محلل مراحل الترجمة - Compiler Stages Analyzer
يحسب مخرجات كل مرحلة من مراحل المترجم بشكل فعلي
"""

from antlr4 import InputStream, CommonTokenStream
from ArabicGrammarLexer import ArabicGrammarLexer
from ArabicGrammarParser import ArabicGrammarParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
import ast_nodes


class CompilerAnalyzer:
    """محلل مراحل الترجمة"""
    
    def __init__(self):
        self.lexer = None
        self.tokens = None
        self.parser = None
        self.tree = None
        self.analyzer = None
        self.ast = None
        self.generator = None
        self.python_code = None
        self.errors = []
    
    def analyze_lexical(self, source_code):
        """التحليل المعجمي - Lexical Analysis"""
        try:
            input_stream = InputStream(source_code)
            self.lexer = ArabicGrammarLexer(input_stream)
            token_stream = CommonTokenStream(self.lexer)
            token_stream.fill()
            self.tokens = token_stream.tokens
            
            # استخراج الرموز
            result = {
                'success': True,
                'tokens': [],
                'token_count': len(self.tokens)
            }
            
            for token in self.tokens:
                if token.type != -1:  # تجاهل EOF
                    token_info = {
                        'type': self.lexer.symbolicNames[token.type] if token.type < len(self.lexer.symbolicNames) else 'UNKNOWN',
                        'text': token.text,
                        'line': token.line,
                        'column': token.column
                    }
                    result['tokens'].append(token_info)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'tokens': []
            }
    
    def analyze_syntax(self, source_code):
        """التحليل النحوي - Syntax Analysis"""
        try:
            input_stream = InputStream(source_code)
            lexer = ArabicGrammarLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            self.parser = ArabicGrammarParser(token_stream)
            
            # بناء الشجرة
            self.tree = self.parser.program()
            
            # فحص الأخطاء النحوية
            syntax_errors = self.parser.getNumberOfSyntaxErrors()
            
            # تحويل الشجرة إلى شكل قابل للقراءة
            tree_structure = self.format_parse_tree(self.tree, self.parser)
            
            result = {
                'success': syntax_errors == 0,
                'tree_raw': self.tree.toStringTree(recog=self.parser) if self.tree else None,
                'tree_formatted': tree_structure,
                'error_count': syntax_errors,
                'errors': []
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'tree_raw': None,
                'tree_formatted': []
            }
    
    def format_parse_tree(self, tree, parser, indent=0):
        """تنسيق شجرة التحليل النحوي بشكل قابل للقراءة"""
        formatted_lines = []
        indent_str = "  " * indent
        
        if tree is None:
            return formatted_lines
        
        # الحصول على اسم القاعدة
        rule_name = parser.ruleNames[tree.getRuleIndex()] if hasattr(tree, 'getRuleIndex') else 'Terminal'
        
        # إذا كانت العقدة نهائية (Terminal)
        if hasattr(tree, 'symbol'):
            token_text = tree.getText()
            formatted_lines.append(f"{indent_str}└─ 📝 {token_text}")
        else:
            # عقدة غير نهائية (Non-terminal)
            formatted_lines.append(f"{indent_str}├─ 🔷 {rule_name}")
            
            # معالجة الأبناء
            if hasattr(tree, 'children') and tree.children:
                for i, child in enumerate(tree.children):
                    is_last = (i == len(tree.children) - 1)
                    child_lines = self.format_parse_tree(child, parser, indent + 1)
                    formatted_lines.extend(child_lines)
        
        return formatted_lines
    
    def analyze_semantic(self, source_code):
        """التحليل الدلالي - Semantic Analysis مع تفاصيل شاملة"""
        try:
            # أولاً التحليل النحوي
            input_stream = InputStream(source_code)
            lexer = ArabicGrammarLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = ArabicGrammarParser(token_stream)
            tree = parser.program()
            
            # التحليل الدلالي
            self.analyzer = SemanticAnalyzer()
            self.ast = self.analyzer.visit(tree)
            
            # استخراج جدول الرموز الكامل
            symbol_table_data = self.get_symbol_table_data()
            
            # استخراج شجرة AST المنسقة
            ast_formatted = self.format_ast_tree(self.ast)
            
            # استخراج تقرير الأخطاء الدلالية
            semantic_errors = self.format_semantic_errors(self.analyzer.errors)
            
            # إحصائيات التحليل الدلالي
            statistics = self.get_semantic_statistics(symbol_table_data, self.analyzer.errors)
            
            result = {
                'success': len(self.analyzer.errors) == 0,
                'ast': self.ast,
                'ast_formatted': ast_formatted,
                'errors': [str(err) for err in self.analyzer.errors],
                'errors_formatted': semantic_errors,
                'symbol_table': symbol_table_data,
                'statistics': statistics
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'ast': None,
                'ast_formatted': [],
                'errors': [str(e)],
                'errors_formatted': [],
                'symbol_table': [],
                'statistics': {}
            }
    
    def format_ast_tree(self, node, indent=0, prefix=""):
        """تنسيق شجرة AST بشكل هرمي قابل للقراءة"""
        lines = []
        indent_str = "  " * indent
        
        if node is None:
            return lines
        
        # اسم نوع العقدة
        node_type = node.__class__.__name__
        
        # رمز العقدة حسب النوع
        icon = self.get_node_icon(node_type)
        
        # معلومات إضافية عن العقدة
        node_info = self.get_node_info(node)
        
        # السطر الرئيسي للعقدة
        if node_info:
            lines.append(f"{indent_str}{prefix}{icon} {node_type}: {node_info}")
        else:
            lines.append(f"{indent_str}{prefix}{icon} {node_type}")
        
        # معالجة الأطفال
        children = self.get_node_children(node)
        for i, (child_name, child_node) in enumerate(children):
            is_last = (i == len(children) - 1)
            child_prefix = "└─ " if is_last else "├─ "
            
            if isinstance(child_node, list):
                # إذا كان الطفل قائمة
                lines.append(f"{indent_str}  {child_prefix}📋 {child_name} [{len(child_node)} عنصر]")
                for j, item in enumerate(child_node):
                    item_is_last = (j == len(child_node) - 1)
                    item_prefix = "   └─ " if item_is_last else "   ├─ "
                    item_lines = self.format_ast_tree(item, indent + 2, item_prefix)
                    lines.extend(item_lines)
            elif child_node is not None:
                # طفل واحد
                child_lines = self.format_ast_tree(child_node, indent + 1, child_prefix)
                lines.extend(child_lines)
        
        return lines
    
    def get_node_icon(self, node_type):
        """الحصول على أيقونة مناسبة حسب نوع العقدة"""
        icon_map = {
            'ProgramNode': '🎯',
            'BlockNode': '📦',
            'ConstantDefNode': '🔒',
            'VarDeclNode': '📊',
            'ProcedureDefNode': '⚙️',
            'AssignmentNode': '➡️',
            'InputNode': '⌨️',
            'OutputNode': '🖨️',
            'IfNode': '❓',
            'ForLoopNode': '🔄',
            'WhileLoopNode': '🔁',
            'CallNode': '📞',
            'BinOpNode': '➕',
            'UnaryOpNode': '➖',
            'VarAccessNode': '📌',
            'LiteralNode': '💎',
            'CompoundStmtNode': '📝',
        }
        return icon_map.get(node_type, '🔸')
    
    def get_node_info(self, node):
        """استخراج معلومات إضافية عن العقدة"""
        info_parts = []
        
        # معلومات حسب نوع العقدة
        if hasattr(node, 'name'):
            info_parts.append(f"'{node.name}'")
        
        if hasattr(node, 'value') and node.value is not None:
            if isinstance(node.value, str):
                info_parts.append(f"القيمة: '{node.value}'")
            else:
                info_parts.append(f"القيمة: {node.value}")
        
        if hasattr(node, 'operator'):
            info_parts.append(f"العامل: {node.operator}")
        
        if hasattr(node, 'data_type') and node.data_type:
            info_parts.append(f"النوع: {node.data_type}")
        
        if hasattr(node, 'literal_type') and node.literal_type:
            info_parts.append(f"النوع: {node.literal_type}")
        
        return " | ".join(info_parts) if info_parts else ""
    
    def get_node_children(self, node):
        """الحصول على أطفال العقدة"""
        children = []
        
        # قائمة الحقول المهمة حسب نوع العقدة
        if hasattr(node, 'block') and node.block:
            children.append(('block', node.block))
        
        if hasattr(node, 'constants') and node.constants:
            children.append(('constants', node.constants))
        
        if hasattr(node, 'variables') and node.variables:
            children.append(('variables', node.variables))
        
        if hasattr(node, 'procedures') and node.procedures:
            children.append(('procedures', node.procedures))
        
        if hasattr(node, 'instructions') and node.instructions:
            children.append(('instructions', node.instructions))
        
        if hasattr(node, 'statements') and node.statements:
            children.append(('statements', node.statements))
        
        if hasattr(node, 'variable') and node.variable:
            children.append(('variable', node.variable))
        
        if hasattr(node, 'expression') and node.expression:
            children.append(('expression', node.expression))
        
        if hasattr(node, 'condition') and node.condition:
            children.append(('condition', node.condition))
        
        if hasattr(node, 'then_stmt') and node.then_stmt:
            children.append(('then_stmt', node.then_stmt))
        
        if hasattr(node, 'else_stmt') and node.else_stmt:
            children.append(('else_stmt', node.else_stmt))
        
        if hasattr(node, 'body') and node.body:
            children.append(('body', node.body))
        
        if hasattr(node, 'left') and node.left:
            children.append(('left', node.left))
        
        if hasattr(node, 'right') and node.right:
            children.append(('right', node.right))
        
        if hasattr(node, 'operand') and node.operand:
            children.append(('operand', node.operand))
        
        if hasattr(node, 'items') and node.items:
            children.append(('items', node.items))
        
        if hasattr(node, 'arguments') and node.arguments:
            children.append(('arguments', node.arguments))
        
        return children
    
    def format_semantic_errors(self, errors):
        """تنسيق الأخطاء الدلالية مع تفاصيل"""
        formatted_errors = []
        
        for i, error in enumerate(errors, 1):
            error_info = {
                'number': i,
                'message': str(error),
                'line': None,
                'column': None,
                'severity': 'خطأ'
            }
            
            # استخراج رقم السطر والعمود إن وجد
            if hasattr(error, 'line'):
                error_info['line'] = error.line
            if hasattr(error, 'column'):
                error_info['column'] = error.column
            
            # تصنيف نوع الخطأ
            error_msg = str(error).lower()
            if 'type' in error_msg or 'نوع' in error_msg:
                error_info['type'] = 'خطأ في الأنواع'
            elif 'undefined' in error_msg or 'غير معرّف' in error_msg:
                error_info['type'] = 'رمز غير معرّف'
            elif 'scope' in error_msg or 'نطاق' in error_msg:
                error_info['type'] = 'خطأ في النطاق'
            else:
                error_info['type'] = 'خطأ دلالي عام'
            
            formatted_errors.append(error_info)
        
        return formatted_errors
    
    def get_semantic_statistics(self, symbol_table, errors):
        """إحصائيات التحليل الدلالي"""
        stats = {
            'total_symbols': len(symbol_table),
            'total_errors': len(errors),
            'variables': 0,
            'constants': 0,
            'procedures': 0,
            'parameters': 0,
            'types': 0
        }
        
        for symbol in symbol_table:
            sym_type = symbol.get('type', '').upper()
            if 'VARIABLE' in sym_type:
                stats['variables'] += 1
            elif 'CONSTANT' in sym_type:
                stats['constants'] += 1
            elif 'PROCEDURE' in sym_type:
                stats['procedures'] += 1
            elif 'PARAMETER' in sym_type:
                stats['parameters'] += 1
            elif 'TYPE' in sym_type:
                stats['types'] += 1
        
        return stats
    
    def get_symbol_table_data(self):
        """الحصول على بيانات جدول الرموز - معالجة جميع النطاقات"""
        if not self.analyzer:
            return []
        
        symbols = []
        
        try:
            # جدول الرموز قد يكون له هيكل مختلف
            symbol_table = self.analyzer.symbol_table
            
            # طريقة 1: إذا كان هناك attribute اسمه scopes (قائمة من النطاقات)
            if hasattr(symbol_table, 'scopes'):
                for scope_level, scope in enumerate(symbol_table.scopes):
                    if isinstance(scope, dict):
                        for name, symbol in scope.items():
                            symbols.append(self.extract_symbol_info(symbol, scope_level))
            
            # طريقة 2: إذا كان هناك attribute اسمه current_scope
            elif hasattr(symbol_table, 'current_scope') and symbol_table.current_scope:
                if isinstance(symbol_table.current_scope, dict):
                    for name, symbol in symbol_table.current_scope.items():
                        symbols.append(self.extract_symbol_info(symbol, 0))
            
            # طريقة 3: البحث في جميع الـ attributes الممكنة
            else:
                # محاولة إيجاد أي dictionary يحتوي على رموز
                for attr_name in dir(symbol_table):
                    if not attr_name.startswith('_'):
                        attr = getattr(symbol_table, attr_name, None)
                        if isinstance(attr, dict) and attr:
                            # التحقق إذا كان هذا dictionary يحتوي على رموز
                            for key, value in attr.items():
                                if hasattr(value, 'name') or hasattr(value, 'symbol_type'):
                                    symbols.append(self.extract_symbol_info(value, 0))
                        elif isinstance(attr, list) and attr:
                            # قد تكون scopes في list
                            for scope in attr:
                                if isinstance(scope, dict):
                                    for name, symbol in scope.items():
                                        symbols.append(self.extract_symbol_info(symbol, 0))
            
            # إذا لم نجد أي رموز، نحاول طريقة مباشرة
            if not symbols:
                # محاولة الوصول المباشر لأي متغيرات معرفة
                if hasattr(symbol_table, '__dict__'):
                    for key, value in symbol_table.__dict__.items():
                        if isinstance(value, dict):
                            for name, sym in value.items():
                                if hasattr(sym, 'name'):
                                    symbols.append(self.extract_symbol_info(sym, 0))
        
        except Exception as e:
            # في حالة حدوث خطأ، نرجع قائمة فارغة مع رسالة
            print(f"تحذير: لم يتم استخراج جدول الرموز بشكل كامل - {str(e)}")
        
        return symbols
    
    def extract_symbol_info(self, symbol, scope_level=0):
        """استخراج معلومات الرمز بشكل مفصل"""
        try:
            symbol_info = {
                'name': getattr(symbol, 'name', 'غير معروف'),
                'type': getattr(symbol, 'symbol_type', 'غير محدد'),
                'data_type': 'غير محدد',
                'value': '-',
                'scope': f"النطاق {scope_level}",
                'is_constant': getattr(symbol, 'is_constant', False),
                'line': getattr(symbol, 'line', '-'),
                'details': ''
            }
            
            # استخراج نوع البيانات
            if hasattr(symbol, 'data_type'):
                dt = symbol.data_type
                if dt is not None:
                    if hasattr(dt, 'base_type'):
                        symbol_info['data_type'] = str(dt.base_type)
                        # معلومات إضافية عن النوع المركب
                        if hasattr(dt, 'is_list') and dt.is_list:
                            symbol_info['details'] = f"قائمة[{dt.list_size}]"
                        elif hasattr(dt, 'is_record') and dt.is_record:
                            symbol_info['details'] = f"سجل ({len(dt.fields)} حقول)"
                    else:
                        symbol_info['data_type'] = str(dt)
            
            # استخراج القيمة
            if hasattr(symbol, 'value') and symbol.value is not None:
                val = symbol.value
                if isinstance(val, str):
                    symbol_info['value'] = f"'{val}'"
                else:
                    symbol_info['value'] = str(val)
            
            # معلومات إضافية للإجراءات
            if hasattr(symbol, 'params') and symbol.params:
                param_count = len(symbol.params)
                symbol_info['value'] = f"({param_count} معامل)"
                # تفاصيل المعاملات
                param_details = []
                for param in symbol.params:
                    if hasattr(param, 'name') and hasattr(param, 'data_type'):
                        param_details.append(f"{param.name}: {param.data_type}")
                if param_details:
                    symbol_info['details'] = ", ".join(param_details)
            
            return symbol_info
            
        except Exception as e:
            return {
                'name': 'خطأ',
                'type': 'خطأ',
                'data_type': str(e),
                'value': '-',
                'scope': f"النطاق {scope_level}",
                'is_constant': False,
                'line': '-',
                'details': ''
            }
    
    def generate_code(self, source_code):
        """توليد الكود - Code Generation"""
        try:
            # التحليل الدلالي أولاً
            semantic_result = self.analyze_semantic(source_code)
            
            if not semantic_result['success']:
                return {
                    'success': False,
                    'code': None,
                    'errors': semantic_result['errors']
                }
            
            # توليد الكود
            self.generator = CodeGenerator()
            self.python_code = self.generator.generate(self.ast)
            
            return {
                'success': True,
                'code': self.python_code,
                'errors': []
            }
            
        except Exception as e:
            return {
                'success': False,
                'code': None,
                'error': str(e)
            }
    
    def full_analysis(self, source_code):
        """تحليل كامل لجميع المراحل"""
        results = {
            'lexical': self.analyze_lexical(source_code),
            'syntax': self.analyze_syntax(source_code),
            'semantic': self.analyze_semantic(source_code),
            'code_gen': self.generate_code(source_code)
        }
        return results


# دوال مساعدة للاستدعاء المباشر
def get_lexical_analysis(source_code):
    """الحصول على التحليل المعجمي"""
    analyzer = CompilerAnalyzer()
    return analyzer.analyze_lexical(source_code)


def get_syntax_analysis(source_code):
    """الحصول على التحليل النحوي"""
    analyzer = CompilerAnalyzer()
    return analyzer.analyze_syntax(source_code)


def get_semantic_analysis(source_code):
    """الحصول على التحليل الدلالي"""
    analyzer = CompilerAnalyzer()
    return analyzer.analyze_semantic(source_code)


def get_symbol_table(source_code):
    """الحصول على جدول الرموز"""
    analyzer = CompilerAnalyzer()
    semantic_result = analyzer.analyze_semantic(source_code)
    return semantic_result.get('symbol_table', [])


def generate_intermediate_code(source_code):
    """توليد الكود الوسيط"""
    analyzer = CompilerAnalyzer()
    return analyzer.generate_code(source_code)
