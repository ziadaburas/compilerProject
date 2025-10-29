
"""
Symbol Table Implementation for Arabic Programming Language
جدول الرموز لإدارة النطاقات والتحقق من الأنواع
"""

class SemanticError(Exception):
    """استثناء خاص بالأخطاء الدلالية - Semantic error exception"""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format_error())
    
    def format_error(self):
        if self.line is not None and self.column is not None:
            return f"خطأ دلالي في السطر {self.line}, العمود {self.column}: {self.message}"
        elif self.line is not None:
            return f"خطأ دلالي في السطر {self.line}: {self.message}"
        else:
            return f"خطأ دلالي: {self.message}"


class Symbol:
    """رمز في جدول الرموز - Symbol in symbol table"""
    def __init__(self, name, symbol_type, data_type=None, value=None, 
                 params=None, scope_level=0, is_constant=False):
        self.name = name
        self.symbol_type = symbol_type  # 'CONSTANT', 'TYPE', 'VARIABLE', 'PARAMETER', 'PROCEDURE'
        self.data_type = data_type      # Type of the symbol
        self.value = value              # For constants
        self.params = params or []      # For procedures: list of ParamSymbol
        self.scope_level = scope_level
        self.is_constant = is_constant
    
    def __repr__(self):
        return f"Symbol(name='{self.name}', type={self.symbol_type}, data_type={self.data_type})"


class ParamSymbol:
    """رمز معامل - Parameter symbol"""
    def __init__(self, name, data_type, pass_mode='BY_VALUE'):
        self.name = name
        self.data_type = data_type
        self.pass_mode = pass_mode  # 'BY_VALUE' or 'BY_REFERENCE'
    
    def __repr__(self):
        return f"ParamSymbol(name='{self.name}', type={self.data_type}, mode={self.pass_mode})"


class TypeInfo:
    """معلومات النوع - Type information"""
    def __init__(self, base_type, is_list=False, list_size=None, 
                 is_record=False, fields=None, is_user_defined=False):
        self.base_type = base_type      # 'صحيح', 'حقيقي', 'منطقي', 'حرفي', 'خيط_رمزي'
        self.is_list = is_list
        self.list_size = list_size
        self.is_record = is_record
        self.fields = fields or {}      # For records: {field_name: TypeInfo}
        self.is_user_defined = is_user_defined
    
    def __repr__(self):
        if self.is_list:
            return f"TypeInfo(list[{self.list_size}] of {self.base_type})"
        elif self.is_record:
            return f"TypeInfo(record with {len(self.fields)} fields)"
        else:
            return f"TypeInfo({self.base_type})"
    
    def __eq__(self, other):
        if not isinstance(other, TypeInfo):
            return False
        if self.is_list != other.is_list or self.is_record != other.is_record:
            return False
        if self.is_list:
            return self.base_type == other.base_type
        if self.is_record:
            return self.fields == other.fields
        return self.base_type == other.base_type


class SymbolTable:
    """جدول الرموز مع دعم النطاقات المتداخلة - Symbol table with nested scopes"""
    
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes (dictionaries)
        self.current_scope_level = 0
        self._initialize_builtin_types()
    
    def _initialize_builtin_types(self):
        """تهيئة الأنواع المدمجة - Initialize built-in types"""
        builtin_types = {
            'صحيح': TypeInfo('صحيح'),
            'حقيقي': TypeInfo('حقيقي'),
            'منطقي': TypeInfo('منطقي'),
            'حرفي': TypeInfo('حرفي'),
            'خيط_رمزي': TypeInfo('خيط_رمزي')
        }
        for name, type_info in builtin_types.items():
            self.scopes[0][name] = Symbol(
                name=name, 
                symbol_type='TYPE', 
                data_type=type_info,
                scope_level=0
            )
    
    def enter_scope(self):
        """الدخول إلى نطاق جديد - Enter a new scope"""
        self.scopes.append({})
        self.current_scope_level += 1
    
    def exit_scope(self):
        """الخروج من النطاق الحالي - Exit current scope"""
        if self.current_scope_level > 0:
            self.scopes.pop()
            self.current_scope_level -= 1
        else:
            raise RuntimeError("لا يمكن الخروج من النطاق العام")
    
    def insert(self, symbol):
        """إضافة رمز إلى النطاق الحالي - Insert symbol into current scope"""
        current_scope = self.scopes[self.current_scope_level]
        
        if symbol.name in current_scope:
            raise SemanticError(
                f"الرمز '{symbol.name}' معرّف مسبقاً في هذا النطاق",
                line=None
            )
        
        symbol.scope_level = self.current_scope_level
        current_scope[symbol.name] = symbol
    
    def lookup(self, name, current_scope_only=False):
        """البحث عن رمز - Look up a symbol"""
        if current_scope_only:
            return self.scopes[self.current_scope_level].get(name)
        
        # Search from current scope up to global scope
        for level in range(self.current_scope_level, -1, -1):
            if name in self.scopes[level]:
                return self.scopes[level][name]
        
        return None
    
    def lookup_type(self, type_name):
        """البحث عن نوع - Look up a type"""
        symbol = self.lookup(type_name)
        if symbol and symbol.symbol_type == 'TYPE':
            return symbol.data_type
        return None
    
    def is_defined(self, name):
        """التحقق من تعريف الرمز - Check if symbol is defined"""
        return self.lookup(name) is not None
    
    def is_variable(self, name):
        """التحقق من كون الرمز متغير - Check if symbol is a variable"""
        symbol = self.lookup(name)
        return symbol and symbol.symbol_type in ['VARIABLE', 'PARAMETER']
    
    def is_constant(self, name):
        """التحقق من كون الرمز ثابت - Check if symbol is a constant"""
        symbol = self.lookup(name)
        return symbol and symbol.symbol_type == 'CONSTANT'
    
    def is_procedure(self, name):
        """التحقق من كون الرمز إجراء - Check if symbol is a procedure"""
        symbol = self.lookup(name)
        return symbol and symbol.symbol_type == 'PROCEDURE'
    
    def get_type(self, name):
        """الحصول على نوع الرمز - Get symbol's type"""
        symbol = self.lookup(name)
        if symbol:
            return symbol.data_type
        return None
    
    def get_constant_value(self, name):
        """الحصول على قيمة الثابت - Get constant value"""
        symbol = self.lookup(name)
        if symbol and symbol.symbol_type == 'CONSTANT':
            return symbol.value
        return None
    
    def get_procedure_params(self, name):
        """الحصول على معاملات الإجراء - Get procedure parameters"""
        symbol = self.lookup(name)
        if symbol and symbol.symbol_type == 'PROCEDURE':
            return symbol.params
        return None
    
    def __repr__(self):
        result = "Symbol Table:\n"
        for level, scope in enumerate(self.scopes):
            result += f"  Level {level}:\n"
            for name, symbol in scope.items():
                result += f"    {symbol}\n"
        return result


class TypeChecker:
    """فاحص الأنواع - Type checker utilities"""
    
    @staticmethod
    def are_compatible(type1, type2):
        """التحقق من توافق الأنواع - Check type compatibility"""
        if type1 is None or type2 is None:
            return False
        
        if isinstance(type1, TypeInfo) and isinstance(type2, TypeInfo):
            # Exact match
            if type1 == type2:
                return True
            
            # Numeric compatibility: صحيح can be assigned to حقيقي
            if type1.base_type == 'صحيح' and type2.base_type == 'حقيقي':
                return True
            
            return False
        
        return type1 == type2
    
    @staticmethod
    def is_numeric(type_info):
        """التحقق من كون النوع رقمي - Check if type is numeric"""
        if isinstance(type_info, TypeInfo):
            return type_info.base_type in ['صحيح', 'حقيقي']
        return False
    
    @staticmethod
    def is_boolean(type_info):
        """التحقق من كون النوع منطقي - Check if type is boolean"""
        if isinstance(type_info, TypeInfo):
            return type_info.base_type == 'منطقي'
        return False
    
    @staticmethod
    def is_string(type_info):
        """التحقق من كون النوع نصي - Check if type is string"""
        if isinstance(type_info, TypeInfo):
            return type_info.base_type in ['خيط_رمزي', 'حرفي']
        return False
    
    @staticmethod
    def get_result_type(operator, left_type, right_type=None):
        """تحديد نوع نتيجة العملية - Determine result type of operation"""
        if right_type is None:  # Unary operation
            if operator == '!':
                if TypeChecker.is_boolean(left_type):
                    return left_type
            elif operator in ['+', '-']:
                if TypeChecker.is_numeric(left_type):
                    return left_type
            return None
        
        # Binary operation
        if operator in ['+', '-', '*', '/', '\\', '%']:
            if TypeChecker.is_numeric(left_type) and TypeChecker.is_numeric(right_type):
                # If either is حقيقي, result is حقيقي
                if left_type.base_type == 'حقيقي' or right_type.base_type == 'حقيقي':
                    return TypeInfo('حقيقي')
                return TypeInfo('صحيح')
        
        elif operator in ['==', '=!', '>', '<', '>=', '<=']:
            if TypeChecker.are_compatible(left_type, right_type):
                return TypeInfo('منطقي')
        
        elif operator in ['&&', '||']:
            if TypeChecker.is_boolean(left_type) and TypeChecker.is_boolean(right_type):
                return TypeInfo('منطقي')
        
        return None
