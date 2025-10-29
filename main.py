
"""
Main Program for Arabic Semantic Analyzer
البرنامج الرئيسي للمحلل الدلالي
"""

import sys
from antlr4 import *

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


def analyze_program(source_code, verbose=False):
    """
    تحليل كود مصدري - Analyze source code
    
    Args:
        source_code: نص الكود المصدري - Source code text
        verbose: طباعة معلومات تفصيلية - Print detailed information
    
    Returns:
        tuple: (ast_root, analyzer, success)
    """
    try:
        # Create input stream
        input_stream = InputStream(source_code)
        
        # Create lexer
        lexer = ArabicGrammarLexer(input_stream)
        
        # Create token stream
        token_stream = CommonTokenStream(lexer)
        
        # Create parser
        parser = ArabicGrammarParser(token_stream)
        
        # Parse the program
        if verbose:
            print("=" * 70)
            print("بدء التحليل النحوي...")
            print("Starting syntactic analysis...")
            print("=" * 70)
        
        parse_tree = parser.program()
        
        if verbose:
            print("✓ التحليل النحوي نجح")
            print("✓ Syntactic analysis succeeded\n")
        
        # Create semantic analyzer
        analyzer = SemanticAnalyzer()
        
        if verbose:
            print("=" * 70)
            print("بدء التحليل الدلالي...")
            print("Starting semantic analysis...")
            print("=" * 70)
        
        # Visit parse tree to build AST and perform semantic checks
        ast_root = analyzer.visit(parse_tree)
        
        # Check for semantic errors
        if analyzer.errors:
            if verbose:
                print("\n✗ فشل التحليل الدلالي - تم اكتشاف أخطاء:")
                print("✗ Semantic analysis failed - errors detected:\n")
            
            for error in analyzer.errors:
                print(f"  • {error}")
            
            return ast_root, analyzer, False
        
        if verbose:
            print("✓ التحليل الدلالي نجح - لا توجد أخطاء!")
            print("✓ Semantic analysis succeeded - no errors!\n")
        
        return ast_root, analyzer, True
    
    except SemanticError as e:
        print(f"\n✗ خطأ دلالي: {e}")
        print(f"✗ Semantic error: {e}")
        return None, None, False
    
    except Exception as e:
        print(f"\n✗ خطأ غير متوقع: {e}")
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None, None, False


def print_symbol_table(analyzer):
    """طباعة جدول الرموز - Print symbol table"""
    print("\n" + "=" * 70)
    print("جدول الرموز - Symbol Table")
    print("=" * 70)
    print(analyzer.symbol_table)


def print_ast_summary(ast_root):
    """طباعة ملخص شجرة AST - Print AST summary"""
    if not ast_root:
        return
    
    print("\n" + "=" * 70)
    print("ملخص شجرة البرنامج - Program AST Summary")
    print("=" * 70)
    print(f"البرنامج: {ast_root.name}")
    print(f"Program: {ast_root.name}\n")
    
    block = ast_root.block
    print(f"  • الثوابت: {len(block.constants)} ثابت")
    print(f"    Constants: {len(block.constants)}")
    
    print(f"  • الأنواع: {len(block.types)} نوع")
    print(f"    Types: {len(block.types)}")
    
    print(f"  • المتغيرات: {len(block.variables)} مجموعة")
    print(f"    Variables: {len(block.variables)} group(s)")
    
    print(f"  • الإجراءات: {len(block.procedures)} إجراء")
    print(f"    Procedures: {len(block.procedures)}")
    
    if block.instructions:
        stmt_count = len(block.instructions.statements) if hasattr(block.instructions, 'statements') else 0
        print(f"  • التعليمات: {stmt_count} تعليمة")
        print(f"    Instructions: {stmt_count}")


# ==================== Example Programs ====================

# مثال 1: برنامج بسيط - Simple program
EXAMPLE_PROGRAM_1 = """
برنامج حساب_المساحة؛
    متغير
        طول، عرض، مساحة: صحيح؛
{
    اقرا(طول)؛
    اقرا(عرض)؛
    مساحة = طول * عرض؛
    اطبع(مساحة)
}.
"""

# مثال 2: برنامج مع ثوابت وإجراءات - Program with constants and procedures
EXAMPLE_PROGRAM_2 = """
برنامج حساب_الدائرة؛
    ثابت
        باي = 3.14؛
    
    متغير
        نصف_القطر: حقيقي؛
        المساحة: حقيقي؛
    
    اجراء احسب_مساحة(بالمرجع س: حقيقي؛ بالقيمة ر: حقيقي)؛
        متغير
            نتيجة: حقيقي؛
    {
        نتيجة = باي * ر * ر؛
        س = نتيجة
    }؛
{
    اقرا(نصف_القطر)؛
    احسب_مساحة(المساحة، نصف_القطر)؛
    اطبع("المساحة: "، المساحة)
}.
"""

# مثال 3: برنامج مع حلقات وشروط - Program with loops and conditions
EXAMPLE_PROGRAM_3 = """
برنامج حساب_المجموع؛
    متغير
        عداد، مجموع، عدد: صحيح؛
{
    مجموع = 0؛
    كرر(عداد = 1 الى 10)
    {
        اقرا(عدد)؛
        اذا(عدد > 0) فان
            مجموع = مجموع + عدد
    }؛
    اطبع("المجموع: "، مجموع)
}.
"""

# مثال 4: برنامج مع قوائم وسجلات - Program with lists and records
EXAMPLE_PROGRAM_4 = """
برنامج ادارة_طلاب؛
    نوع
        طالب = سجل {
            الاسم: خيط_رمزي؛
            العمر: صحيح؛
            المعدل: حقيقي
        }؛
        قائمة_طلاب = قائمة[50] من طالب؛
    
    متغير
        طلاب: قائمة_طلاب؛
        فهرس: صحيح؛
{
    فهرس = 0؛
    اقرا(طلاب[فهرس].الاسم)؛
    اقرا(طلاب[فهرس].العمر)؛
    اقرا(طلاب[فهرس].المعدل)؛
    اطبع("الطالب: "، طلاب[فهرس].الاسم)
}.
"""

# مثال 5: برنامج مع أخطاء دلالية - Program with semantic errors
EXAMPLE_PROGRAM_WITH_ERRORS = """
برنامج برنامج_خاطئ؛
    متغير
        س: صحيح؛
        ص: حقيقي؛
{
    س = ص؛
    ع = 10؛
    اطبع(غير_معرف)؛
    غير_موجود(س، ص)
}.
"""


def main():
    """البرنامج الرئيسي - Main program"""
    print("\n" + "=" * 70)
    print("محلل دلالي للغة البرمجة العربية")
    print("Arabic Programming Language Semantic Analyzer")
    print("=" * 70)
    
    # Choose which example to run
    print("\nاختر مثال لتحليله:")
    print("Choose an example to analyze:")
    print("  1. برنامج بسيط (حساب المساحة)")
    print("  2. برنامج مع ثوابت وإجراءات (حساب مساحة الدائرة)")
    print("  3. برنامج مع حلقات وشروط (حساب المجموع)")
    print("  4. برنامج مع قوائم وسجلات (إدارة الطلاب)")
    print("  5. برنامج مع أخطاء دلالية")
    
    choice = input("\nأدخل رقم المثال (1-5): ").strip()
    
    programs = {
        '1': ('حساب_المساحة', EXAMPLE_PROGRAM_1),
        '2': ('حساب_الدائرة', EXAMPLE_PROGRAM_2),
        '3': ('حساب_المجموع', EXAMPLE_PROGRAM_3),
        '4': ('ادارة_طلاب', EXAMPLE_PROGRAM_4),
        '5': ('برنامج_خاطئ', EXAMPLE_PROGRAM_WITH_ERRORS)
    }
    
    if choice not in programs:
        print("خيار غير صحيح!")
        return
    
    program_name, source_code = programs[choice]
    
    print(f"\n{'=' * 70}")
    print(f"تحليل البرنامج: {program_name}")
    print(f"Analyzing program: {program_name}")
    print('=' * 70)
    print("\nالكود المصدري:")
    print("Source code:")
    print(source_code)
    
    # Analyze the program
    ast_root, analyzer, success = analyze_program(source_code, verbose=True)
    
    if success:
        # Print symbol table
        print_symbol_table(analyzer)
        
        # Print AST summary
        print_ast_summary(ast_root)
        
        print("\n" + "=" * 70)
        print("✓✓✓ نجح التحليل الدلالي بدون أخطاء!")
        print("✓✓✓ Semantic analysis completed successfully!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✗✗✗ فشل التحليل الدلالي")
        print("✗✗✗ Semantic analysis failed")
        print("=" * 70)


if __name__ == "__main__":
    main()
