
"""
Main Program for Arabic Programming Language Compiler
البرنامج الرئيسي للمترجم - يشمل التحليل التوليد والتنفيذ
"""

import sys
import os
import subprocess
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

# Import generated ANTLR files
try:
    from ArabicGrammarLexer import ArabicGrammarLexer
    from ArabicGrammarParser import ArabicGrammarParser
except ImportError:
    print("=" * 70)
    print("خطأ: ملفات ANTLR غير موجودة!")
    print("Error: ANTLR files not found!")
    print("=" * 70)
    print("\nيرجى توليد ملفات البايثون من ملف القواعد باستخدام الأمر التالي:")
    print("Please generate Python files from grammar using:")
    print("\n  antlr4 -Dlanguage=Python3 -visitor ArabicGrammar.g4\n")
    print("تأكد من تثبيت ANTLR4:")
    print("Make sure ANTLR4 is installed:")
    print("  pip install antlr4-python3-runtime")
    print("=" * 70)
    sys.exit(1)

from semantic_analyzer import SemanticAnalyzer
from symbol_table import SemanticError
from code_generator import generate_code


def compile_and_run(source_code, verbose=False, execute=True, output_file=None):
    """
    تحليل وتوليد وتنفيذ كود مصدري - Compile and execute source code
    
    Args:
        source_code: الكود المصدري - Source code
        verbose: عرض تفاصيل إضافية - Show verbose output
        execute: تنفيذ الكود المولّد - Execute generated code
        output_file: ملف الإخراج - Output file
    
    Returns:
        tuple: (success, generated_code, ast, errors)
    """
    
    print("=" * 70)
    print("مترجم اللغة العربية البرمجية")
    print("Arabic Programming Language Compiler")
    print("=" * 70)
    print()
    
    # ===== المرحلة 1: التحليل اللغوي (Lexical Analysis) =====
    if verbose:
        print("▶ المرحلة 1: التحليل اللغوي")
        print("▶ Phase 1: Lexical Analysis")
        print("-" * 70)
    
    try:
        input_stream = InputStream(source_code)
        lexer = ArabicGrammarLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        
        if verbose:
            token_stream.fill()
            print(f"✓ تم التعرف على {len(token_stream.tokens)} رمز")
            print(f"✓ Recognized {len(token_stream.tokens)} tokens")
            print()
            
            # Reset stream for parser
            input_stream = InputStream(source_code)
            lexer = ArabicGrammarLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
        
    except Exception as e:
        print(f"✗ خطأ في التحليل اللغوي: {e}")
        print(f"✗ Lexical analysis error: {e}")
        return False, None, None, [str(e)]
    
    # ===== المرحلة 2: التحليل النحوي (Syntax Analysis) =====
    if verbose:
        print("▶ المرحلة 2: التحليل النحوي")
        print("▶ Phase 2: Syntax Analysis")
        print("-" * 70)
    
    try:
        parser = ArabicGrammarParser(token_stream)
        
        # Custom error listener
        parser.removeErrorListeners()
        error_listener = CustomErrorListener()
        parser.addErrorListener(error_listener)
        
        # Parse
        parse_tree = parser.program()
        
        if error_listener.errors:
            print("✗ أخطاء نحوية:")
            print("✗ Syntax errors:")
            for error in error_listener.errors:
                print(f"  {error}")
            return False, None, None, error_listener.errors
        
        if verbose:
            print("✓ التحليل النحوي ناجح")
            print("✓ Syntax analysis successful")
            print()
        
    except Exception as e:
        print(f"✗ خطأ في التحليل النحوي: {e}")
        print(f"✗ Syntax analysis error: {e}")
        return False, None, None, [str(e)]
    
    # ===== المرحلة 3: التحليل الدلالي (Semantic Analysis) =====
    if verbose:
        print("▶ المرحلة 3: التحليل الدلالي")
        print("▶ Phase 3: Semantic Analysis")
        print("-" * 70)
    
    try:
        analyzer = SemanticAnalyzer()
        ast = analyzer.visit(parse_tree)
        
        if analyzer.errors:
            print("✗ أخطاء دلالية:")
            print("✗ Semantic errors:")
            for error in analyzer.errors:
                print(f"  {error.format_error()}")
            return False, None, ast, analyzer.errors
        
        if verbose:
            print("✓ التحليل الدلالي ناجح")
            print("✓ Semantic analysis successful")
            print(f"  - البرنامج: {ast.name}")
            print(f"  - Program: {ast.name}")
            
            if ast.block.constants:
                print(f"  - ثوابت: {len(ast.block.constants)}")
                print(f"  - Constants: {len(ast.block.constants)}")
            
            if ast.block.variables:
                print(f"  - متغيرات: {len(ast.block.variables)}")
                print(f"  - Variables: {len(ast.block.variables)}")
            
            if ast.block.procedures:
                print(f"  - إجراءات: {len(ast.block.procedures)}")
                print(f"  - Procedures: {len(ast.block.procedures)}")
            
            print()
        
    except Exception as e:
        print(f"✗ خطأ في التحليل الدلالي: {e}")
        print(f"✗ Semantic analysis error: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None, [str(e)]
    
    # ===== المرحلة 4: توليد الكود (Code Generation) =====
    if verbose:
        print("▶ المرحلة 4: توليد الكود")
        print("▶ Phase 4: Code Generation")
        print("-" * 70)
    
    try:
        # Determine output file
        if not output_file:
            output_file = f"{ast.name}_generated.py"
        
        generated_code = generate_code(ast, output_file)
        
        if verbose:
            print(f"✓ تم توليد الكود بنجاح: {output_file}")
            print(f"✓ Code generated successfully: {output_file}")
            print(f"  - عدد الأسطر: {len(generated_code.splitlines())}")
            print(f"  - Lines: {len(generated_code.splitlines())}")
            print()
        
    except Exception as e:
        print(f"✗ خطأ في توليد الكود: {e}")
        print(f"✗ Code generation error: {e}")
        import traceback
        traceback.print_exc()
        return False, None, ast, [str(e)]
    
    # ===== المرحلة 5: التنفيذ (Execution) =====
    if execute:
        if verbose:
            print("▶ المرحلة 5: التنفيذ")
            print("▶ Phase 5: Execution")
            print("-" * 70)
        
        print()
        print("=" * 70)
        print("مخرجات البرنامج / Program Output:")
        print("=" * 70)
        print()
        
        try:
            # Execute the generated code
            result = subprocess.run(
                [sys.executable, output_file],
                capture_output=False,
                text=True,
                timeout=30
            )
            
            print()
            print("=" * 70)
            
            if result.returncode == 0:
                print("✓ تم تنفيذ البرنامج بنجاح")
                print("✓ Program executed successfully")
            else:
                print(f"✗ فشل التنفيذ - رمز الخروج: {result.returncode}")
                print(f"✗ Execution failed - Exit code: {result.returncode}")
            
        except subprocess.TimeoutExpired:
            print()
            print("=" * 70)
            print("✗ انتهت مهلة التنفيذ (30 ثانية)")
            print("✗ Execution timeout (30 seconds)")
        
        except Exception as e:
            print()
            print("=" * 70)
            print(f"✗ خطأ في التنفيذ: {e}")
            print(f"✗ Execution error: {e}")
    
    print("=" * 70)
    return True, generated_code, ast, []


class CustomErrorListener(ErrorListener):
    """مستمع الأخطاء المخصص - Custom error listener"""
    
    def __init__(self):
        super().__init__()
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_msg = f"السطر {line}:{column} - {msg}"
        self.errors.append(error_msg)


def main():
    """البرنامج الرئيسي - Main program"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='مترجم اللغة العربية البرمجية - Arabic Programming Language Compiler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة / Examples:
  python main_complete.py program.txt              # تجميع وتنفيذ ملف
  python main_complete.py program.txt -v           # وضع مفصل
  python main_complete.py program.txt -o output.py # تحديد ملف الإخراج
  python main_complete.py program.txt --no-exec    # عدم التنفيذ
        """
    )
    
    parser.add_argument('source_file', help='ملف المصدر العربي - Arabic source file')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='عرض تفاصيل إضافية - Show verbose output')
    parser.add_argument('-o', '--output', help='ملف الإخراج - Output file')
    parser.add_argument('--no-exec', action='store_true',
                       help='عدم تنفيذ الكود المولّد - Don\'t execute generated code')
    
    args = parser.parse_args()
    
    # Read source file
    try:
        with open(args.source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"✗ الملف غير موجود: {args.source_file}")
        print(f"✗ File not found: {args.source_file}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ خطأ في قراءة الملف: {e}")
        print(f"✗ Error reading file: {e}")
        sys.exit(1)
    
    # Compile and run
    success, code, ast, errors = compile_and_run(
        source_code,
        verbose=args.verbose,
        execute=not args.no_exec,
        output_file=args.output
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
