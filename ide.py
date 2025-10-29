#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
المترجم العربي (Arabic Compiler IDE)
مشروع محاكي لبيئة تطوير متكاملة باللغة العربية
"""

import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ArabicCompilerIDE(QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #     self.current_file = None
    #     self.dark_mode = True
    #     self.init_ui()
    #     self.setup_connections()

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.dark_mode = True
        self.waiting_for_input = False  # ← أضف هذا السطر
        self.input_buffer = ""  # ← أضف هذا السطر
        self.input_callback = None  # ← أضف هذا السطر
        self.console_output=None
        self.editor_widget= None
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("المترجم العربي - Arabic Compiler IDE")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
        # تطبيق الأيقونة
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # إنشاء القوائم
        self.create_menu_bar()
        
        # إنشاء الواجهة الرئيسية
        self.create_main_layout()
        
        # إنشاء شريط الحالة
        self.create_status_bar()
        
        # تطبيق النمط الداكن
        self.apply_dark_theme()
        
    def create_menu_bar(self):
        """إنشاء شريط القوائم"""
        menubar = self.menuBar()
        menubar.setLayoutDirection(Qt.RightToLeft)
        
        # قائمة ملف
        file_menu = menubar.addMenu("ملف")
        
        new_action = QAction("📄 ملف جديد", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("📂 فتح ملف", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("💾 حفظ", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("💾 حفظ باسم...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        print_action = QAction("🖨️ طباعة", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_file)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("❌ خروج", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # قائمة تعديل
        edit_menu = menubar.addMenu("تعديل")
        
        cut_action = QAction("✂️ قص", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut_text)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("📋 نسخ", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_text)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("📎 لصق", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_text)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        undo_action = QAction("🔙 تراجع", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo_text)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("🔜 إعادة", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo_text)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        clear_action = QAction("🧹 حذف الكل", self)
        clear_action.triggered.connect(self.clear_all)
        edit_menu.addAction(clear_action)
        
        # قائمة تشغيل
        run_menu = menubar.addMenu("تشغيل")
        
        run_action = QAction("▶️ تشغيل الكود", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)
        
        stop_action = QAction("🧩 إيقاف التنفيذ", self)
        stop_action.setShortcut("Shift+F5")
        stop_action.triggered.connect(self.stop_execution)
        run_menu.addAction(stop_action)
        
        run_menu.addSeparator()
        
        settings_action = QAction("⚙️ إعدادات التشغيل", self)
        settings_action.triggered.connect(self.run_settings)
        run_menu.addAction(settings_action)
        
        # قائمة عرض
        view_menu = menubar.addMenu("عرض")
        
        lexical_action = QAction("📜 إظهار التحليل المعجمي", self)
        lexical_action.triggered.connect(self.show_lexical_analysis)
        view_menu.addAction(lexical_action)
        
        syntax_action = QAction("🧠 إظهار التحليل النحوي", self)
        syntax_action.triggered.connect(self.show_syntax_analysis)
        view_menu.addAction(syntax_action)
        
        semantic_action = QAction("🧩 إظهار التحليل الدلالي", self)
        semantic_action.triggered.connect(self.show_semantic_analysis)
        view_menu.addAction(semantic_action)
        
        view_menu.addSeparator()
        
        symbol_action = QAction("📊 عرض جدول الرموز", self)
        symbol_action.triggered.connect(self.show_symbol_table)
        view_menu.addAction(symbol_action)
        
        console_action = QAction("🧾 عرض مخرجات التنفيذ", self)
        console_action.triggered.connect(self.show_console)
        view_menu.addAction(console_action)
        
        view_menu.addSeparator()
        
        theme_action = QAction("🎨 تغيير النمط (فاتح / داكن)", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        # قائمة مساعدة
        help_menu = menubar.addMenu("مساعدة")
        
        about_action = QAction("ℹ️ حول البرنامج", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        guide_action = QAction("💡 دليل الاستخدام", self)
        guide_action.triggered.connect(self.show_guide)
        help_menu.addAction(guide_action)
        
        developer_action = QAction("🧑‍💻 عن المطور", self)
        developer_action.triggered.connect(self.show_developer)
        help_menu.addAction(developer_action)
        
        contact_action = QAction("🌐 تواصل معنا", self)
        contact_action.triggered.connect(self.show_contact)
        help_menu.addAction(contact_action)
        
    def create_main_layout(self):
        """إنشاء التخطيط الرئيسي"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # إنشاء Splitter للتحكم في الأحجام
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # الشريط الجانبي (يسار)
        self.create_sidebar()
        
        # المنطقة الوسطى (محرر + وحدة التحكم)
        self.create_center_area()
        
        # تعيين الأحجام الأولية
        self.main_splitter.setSizes([200, 800])
        self.main_splitter.setCollapsible(0, True)
        
    def create_sidebar(self):
        """إنشاء الشريط الجانبي"""
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(5, 5, 5, 5)
        
        # تبويبات الشريط الجانبي
        sidebar_tabs = QTabWidget()
        sidebar_tabs.setTabPosition(QTabWidget.North)
        
        # تبويب الملفات
        files_widget = QWidget()
        files_layout = QVBoxLayout(files_widget)
        
        files_label = QLabel("📂 الملفات")
        files_label.setAlignment(Qt.AlignCenter)
        files_layout.addWidget(files_label)
        
        self.files_list = QListWidget()
        self.files_list.addItem("ملف جديد.txt")
        files_layout.addWidget(self.files_list)
        
        sidebar_tabs.addTab(files_widget, "الملفات")
        
        # تبويب التحليلات
        analysis_widget = QWidget()
        analysis_layout = QVBoxLayout(analysis_widget)
        
        analysis_label = QLabel("🧠 التحليلات")
        analysis_label.setAlignment(Qt.AlignCenter)
        analysis_layout.addWidget(analysis_label)
        
        self.analysis_list = QListWidget()
        self.analysis_list.addItems([
            "📜 التحليل المعجمي",
            "🧠 التحليل النحوي", 
            "🧩 التحليل الدلالي",
            "📊 جدول الرموز"
        ])
        analysis_layout.addWidget(self.analysis_list)
        
        sidebar_tabs.addTab(analysis_widget, "التحليلات")
        
        # تبويب الإعدادات
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        settings_label = QLabel("⚙️ الإعدادات")
        settings_label.setAlignment(Qt.AlignCenter)
        settings_layout.addWidget(settings_label)
        
        theme_btn = QPushButton("🎨 تبديل النمط")
        theme_btn.clicked.connect(self.toggle_theme)
        settings_layout.addWidget(theme_btn)
        
        font_btn = QPushButton("🔤 تغيير الخط")
        font_btn.clicked.connect(self.change_font)
        settings_layout.addWidget(font_btn)
        
        settings_layout.addStretch()
        
        sidebar_tabs.addTab(settings_widget, "الإعدادات")
        
        sidebar_layout.addWidget(sidebar_tabs)
        
        self.main_splitter.addWidget(sidebar_widget)
        
    def create_center_area(self):
        """إنشاء المنطقة الوسطى"""
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(5, 5, 5, 5)
        
        # إنشاء Splitter عمودي للمحرر ووحدة التحكم
        self.vertical_splitter = QSplitter(Qt.Vertical)
        center_layout.addWidget(self.vertical_splitter)
        
        # منطقة المحرر
        self.create_editor_area()
        
        # منطقة وحدة التحكم
        self.create_console_area()
        
        # تعيين الأحجام الأولية
        self.vertical_splitter.setSizes([500, 150])
        self.vertical_splitter.setCollapsible(1, True)
        
        self.main_splitter.addWidget(center_widget)
        
    def create_editor_area(self):
        """إنشاء منطقة المحرر"""
        self.editor_widget = QWidget()
        editor_layout = QVBoxLayout(self.editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        
        # شريط الأدوات للمحرر
        editor_toolbar = QHBoxLayout()
        editor_toolbar.setContentsMargins(5, 5, 5, 5)
        
        # أزرار التحكم
        run_btn = QPushButton("▶️ تشغيل")
        run_btn.clicked.connect(self.run_code)
        run_btn.setMinimumHeight(30)
        editor_toolbar.addWidget(run_btn)
        
        save_btn = QPushButton("💾 حفظ")
        save_btn.clicked.connect(self.save_file)
        save_btn.setMinimumHeight(30)
        editor_toolbar.addWidget(save_btn)
        
        clear_btn = QPushButton("🧹 مسح")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setMinimumHeight(30)
        editor_toolbar.addWidget(clear_btn)
        
        editor_toolbar.addStretch()
        
        # معلومات الملف
        self.file_info_label = QLabel("ملف جديد")
        self.file_info_label.setAlignment(Qt.AlignLeft)
        editor_toolbar.addWidget(self.file_info_label)
        
        editor_layout.addLayout(editor_toolbar)
        
        # محرر النصوص
        self.text_editor = QTextEdit()
        self.text_editor.setLayoutDirection(Qt.RightToLeft)
        self.text_editor.setPlaceholderText("اكتب الكود العربي هنا...\n\nمثال:\nإعلان متغير عدد = ١٠\nطباعة عدد")
        
        # تعيين خط الكود
        font = QFont("Consolas", 12)
        if not font.exactMatch():
            font = QFont("Courier New", 12)
        self.text_editor.setFont(font)
        
        editor_layout.addWidget(self.text_editor)
        
        self.vertical_splitter.addWidget(self.editor_widget)
        
    def create_console_area(self):
        """إنشاء منطقة وحدة التحكم"""
        console_widget = QWidget()
        console_layout = QVBoxLayout(console_widget)
        console_layout.setContentsMargins(0, 0, 0, 0)
        # في الدالة create_main_layout
        
        # شريط وحدة التحكم
        console_toolbar = QHBoxLayout()
        console_toolbar.setContentsMargins(5, 5, 5, 5)
        
        console_label = QLabel("🧾 وحدة التحكم والمخرجات")
        console_label.setAlignment(Qt.AlignRight)
        console_toolbar.addWidget(console_label)
        
        console_toolbar.addStretch()
        
        clear_console_btn = QPushButton("🧹 مسح المخرجات")
        clear_console_btn.clicked.connect(self.clear_console)
        clear_console_btn.setMaximumHeight(25)
        console_toolbar.addWidget(clear_console_btn)
        
        console_layout.addLayout(console_toolbar)
        
        # منطقة المخرجات
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setLayoutDirection(Qt.RightToLeft)
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(False)  # ← غيّر من True إلى False
        self.console_output.setPlaceholderText("المخرجات والمدخلات ستظهر هنا...")
        self.console_output.installEventFilter(self)  # ← أضف هذا السطر

        # خط وحدة التحكم
        console_font = QFont("Consolas", 10)
        if not console_font.exactMatch():
            console_font = QFont("Courier New", 10)
        self.console_output.setFont(console_font)
        
        # رسالة ترحيب
        welcome_msg = """
🌟 مرحباً بك في المترجم العربي
📝 اكتب الكود في المحرر أعلاه واضغط تشغيل
⚡ سيتم عرض النتائج والتحليلات هنا
        """
        self.console_output.setPlainText(welcome_msg.strip())
        
        console_layout.addWidget(self.console_output)
        
        self.vertical_splitter.addWidget(console_widget)
        
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_bar = self.statusBar()
        self.status_bar.setLayoutDirection(Qt.RightToLeft)
        
        # حالة النظام
        self.status_label = QLabel("🟢 جاهز")
        self.status_bar.addPermanentWidget(self.status_label)
        
        # فاصل
        separator1 = QLabel(" | ")
        self.status_bar.addPermanentWidget(separator1)
        
        # اسم الملف
        self.file_name_label = QLabel("📁 ملف جديد")
        self.status_bar.addPermanentWidget(self.file_name_label)
        
        # فاصل
        separator2 = QLabel(" | ")
        self.status_bar.addPermanentWidget(separator2)
        
        # الوقت
        self.time_label = QLabel()
        self.update_time()
        self.status_bar.addPermanentWidget(self.time_label)
        
        # فاصل
        separator3 = QLabel(" | ")
        self.status_bar.addPermanentWidget(separator3)
        
        # زر تبديل النمط
        self.theme_toggle_btn = QPushButton("🌗")
        self.theme_toggle_btn.setMaximumSize(30, 25)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.theme_toggle_btn.setToolTip("تبديل النمط (فاتح/داكن)")
        self.status_bar.addPermanentWidget(self.theme_toggle_btn)
        
        # تحديث الوقت كل ثانية
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
    def setup_connections(self):
        """إعداد الاتصالات والإشارات"""
        # ربط قائمة الملفات
        self.files_list.itemClicked.connect(self.on_file_selected)
        
        # ربط قائمة التحليلات
        self.analysis_list.itemClicked.connect(self.on_analysis_selected)
        
        # ربط تغيير النص
        self.text_editor.textChanged.connect(self.on_text_changed)
        
    # وظائف القوائم
    def new_file(self):
        """إنشاء ملف جديد"""
        if self.text_editor.toPlainText().strip():
            reply = QMessageBox.question(self, "ملف جديد", 
                                       "هل تريد حفظ التغييرات الحالية؟",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return
                
        self.text_editor.clear()
        self.current_file = None
        self.file_info_label.setText("ملف جديد")
        self.file_name_label.setText("📁 ملف جديد")
        self.log_to_console("📄 تم إنشاء ملف جديد")
        
    def open_file(self):
        """فتح ملف"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "فتح ملف", "", 
            "ملفات نصية (*.txt);;ملفات الكود (*.code);;جميع الملفات (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_editor.setPlainText(content)
                    self.current_file = file_path
                    file_name = os.path.basename(file_path)
                    self.file_info_label.setText(file_name)
                    self.file_name_label.setText(f"📁 {file_name}")
                    self.log_to_console(f"📂 تم فتح الملف: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"لا يمكن فتح الملف:\n{str(e)}")
                
    def save_file(self):
        """حفظ الملف"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.toPlainText())
                self.log_to_console(f"💾 تم حفظ الملف: {os.path.basename(self.current_file)}")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"لا يمكن حفظ الملف:\n{str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        """حفظ الملف باسم جديد"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "حفظ باسم", "", 
            "ملفات نصية (*.txt);;ملفات الكود (*.code);;جميع الملفات (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.toPlainText())
                    self.current_file = file_path
                    file_name = os.path.basename(file_path)
                    self.file_info_label.setText(file_name)
                    self.file_name_label.setText(f"📁 {file_name}")
                    self.log_to_console(f"💾 تم حفظ الملف باسم: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"لا يمكن حفظ الملف:\n{str(e)}")
                
    def print_file(self):
        """طباعة الملف"""
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.text_editor.print_(printer)
            self.log_to_console("🖨️ تم إرسال الملف للطباعة")
            
    # وظائف التعديل
    def cut_text(self):
        self.text_editor.cut()
        self.log_to_console("✂️ تم قص النص")
        
    def copy_text(self):
        self.text_editor.copy()
        self.log_to_console("📋 تم نسخ النص")
        
    def paste_text(self):
        self.text_editor.paste()
        self.log_to_console("📎 تم لصق النص")
        
    def undo_text(self):
        self.text_editor.undo()
        self.log_to_console("🔙 تم التراجع")
        
    def redo_text(self):
        self.text_editor.redo()
        self.log_to_console("🔜 تم الإعادة")
        
    def clear_all(self):
        """مسح كل النص"""
        reply = QMessageBox.question(self, "مسح الكل", 
                                   "هل أنت متأكد من مسح كل النص؟",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.text_editor.clear()
            self.log_to_console("🧹 تم مسح كل النص")
            
    # وظائف التشغيل
    def run_code(self):
        """تشغيل الكود مباشرة من الواجهة"""
        try:
            # مسح الكونسول
            self.console_output.clear()
            
            # الحصول على الكود المصدري 
            source_code = self.text_editor.toPlainText()
            if not source_code.strip():
                self.console_output.setPlainText("❌ لا يوجد كود للتشغيل!")
                return
            
            # استيراد المكتبات الضرورية
            from antlr4 import InputStream, CommonTokenStream
            from ArabicGrammarLexer import ArabicGrammarLexer
            from ArabicGrammarParser import ArabicGrammarParser
            from semantic_analyzer import SemanticAnalyzer
            from code_generator import CodeGenerator
            
            # التحليل اللغوي
            input_stream = InputStream(source_code)
            lexer = ArabicGrammarLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = ArabicGrammarParser(token_stream)
            
            # بناء شجرة AST
            tree = parser.program()
            
            # التحليل الدلالي
            analyzer = SemanticAnalyzer()
            ast = analyzer.visit(tree)
            
            if analyzer.errors:
                error_msg = "\n".join([f"❌ {err}" for err in analyzer.errors])
                self.console_output.setPlainText(error_msg)
                return
            
            # توليد الكود
            generator = CodeGenerator()
            python_code = generator.generate(ast)
            
            # تنفيذ الكود المولد
            self.execute_generated_code(python_code)
            
        except Exception as e:
            self.console_output.setPlainText(f"❌ خطأ في التنفيذ:\n{str(e)}")
    def execute_generated_code(self, python_code):
        """تنفيذ الكود البايثون المولد داخل الواجهة"""
        import io
        import sys
        from contextlib import redirect_stdout, redirect_stderr
        
        # إنشاء بيئة تنفيذ معزولة
        namespace = {
            '__name__': '__main__',
            '__builtins__': __builtins__,
            'print': self.console_print,  # استبدال print
            'input': self.console_input,  # استبدال input
            'math': __import__('math'),
            'sys': __import__('sys')
        }
        
        try:
            # تنفيذ الكود
            exec(python_code, namespace)
            
            # تشغيل main إذا كانت موجودة
            if 'main' in namespace:
                namespace['main']()
                
        except Exception as e:
            self.console_output.insertPlainText(f"\n❌ خطأ في التنفيذ: {str(e)}\n")
    def console_print(self, *args, **kwargs):
        """دالة طباعة مخصصة للكونسول"""
        # تحويل كل المدخلات إلى نص
        text = " ".join(str(arg) for arg in args)
        
        # إضافة النص للكونسول
        self.console_output.insertPlainText(text)
        
        # إضافة سطر جديد إذا لم يكن end محددًا
        if kwargs.get('end', '\n') == '\n':
            self.console_output.insertPlainText('\n')
        
        # التمرير للأسفل
        scrollbar = self.console_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # تحديث الواجهة
        QApplication.processEvents()

    def run_code1(self):
        """تشغيل الكود"""
        code = self.text_editor.toPlainText().strip()
        if not code:
            self.log_to_console("⚠️ لا يوجد كود للتشغيل", "warning")
            return
            
        self.status_label.setText("🔄 جارٍ التحليل...")
        self.log_to_console("▶️ بدء تحليل الكود...")
        # حاول استدعاء المترجم الحقيقي من ملف main1.py
        try:
            success, generated_code, ast, errors, captured = self.run_compiler_and_capture(code)

            # أظهر ناتج المترجم (التحليلات والمخرجات)
            if captured:
                for line in captured.splitlines():
                    self.log_to_console(line, "output")

            if errors:
                for err in errors:
                    # قد يكون err عبارة عن كائن أو نص
                    try:
                        msg = err.format_error()
                    except Exception:
                        msg = str(err)
                    self.log_to_console(msg, "error")

            if not success:
                self.log_to_console("✗ فشل التجميع أو التنفيذ", "error")
        except Exception as e:
            # إن لم يتوفر المترجم، استمر مع المحاكاة القديمة
            self.log_to_console(f"⚠️ تعذر تشغيل المترجم الحقيقي: {e}")
            # محاكاة التحليل المعجمي
            self.simulate_lexical_analysis(code)
            
            # محاكاة التحليل النحوي
            self.simulate_syntax_analysis(code)
            
            # محاكاة التحليل الدلالي
            self.simulate_semantic_analysis(code)
            
            # محاكاة التنفيذ
            self.simulate_execution(code)
        
        self.status_label.setText("🟢 جاهز")
        
    def stop_execution(self):
        """إيقاف التنفيذ"""
        self.log_to_console("🛑 تم إيقاف التنفيذ", "error")
        self.status_label.setText("🟢 جاهز")
        
    def run_settings(self):
        """إعدادات التشغيل"""
        QMessageBox.information(self, "إعدادات التشغيل", 
                              "إعدادات التشغيل ستكون متاحة في الإصدار القادم")
        
    # وظائف العرض
    def show_lexical_analysis(self):
        """عرض التحليل المعجمي"""
        code = self.text_editor.toPlainText().strip()
        if code:
            self.simulate_lexical_analysis(code)
        else:
            self.log_to_console("⚠️ لا يوجد كود للتحليل", "warning")
            
    def show_syntax_analysis(self):
        """عرض التحليل النحوي"""
        code = self.text_editor.toPlainText().strip()
        if code:
            self.simulate_syntax_analysis(code)
        else:
            self.log_to_console("⚠️ لا يوجد كود للتحليل", "warning")
            
    def show_semantic_analysis(self):
        """عرض التحليل الدلالي"""
        code = self.text_editor.toPlainText().strip()
        if code:
            self.simulate_semantic_analysis(code)
        else:
            self.log_to_console("⚠️ لا يوجد كود للتحليل", "warning")
            
    def show_symbol_table(self):
        """عرض جدول الرموز"""
        self.log_to_console("📊 جدول الرموز:")
        self.log_to_console("┌─────────────┬──────────┬─────────┐")
        self.log_to_console("│    الرمز    │  النوع   │ القيمة  │")
        self.log_to_console("├─────────────┼──────────┼─────────┤")
        self.log_to_console("│    عدد      │  متغير   │   ١٠    │")
        self.log_to_console("│   نص       │  متغير   │ 'مرحبا'  │")
        self.log_to_console("│  طباعة     │  دالة    │   -     │")
        self.log_to_console("└─────────────┴──────────┴─────────┘")
        
    def show_console(self):
        """إظهار وحدة التحكم"""
        if self.vertical_splitter.sizes()[1] == 0:
            self.vertical_splitter.setSizes([500, 150])
        self.log_to_console("🧾 تم إظهار وحدة التحكم")
        
    def toggle_theme(self):
        """تبديل النمط"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_theme()
            self.log_to_console("🌙 تم تطبيق النمط الداكن")
        else:
            self.apply_light_theme()
            self.log_to_console("☀️ تم تطبيق النمط الفاتح")
            
    # وظائف المساعدة
    def show_about(self):
        """حول البرنامج"""
        about_text = """
        <div style='text-align: center; direction: rtl;'>
        <h2>🌟 المترجم العربي</h2>
        <h3>Arabic Compiler IDE</h3>
        <p><b>الإصدار:</b> 1.0</p>
        <p><b>التاريخ:</b> أكتوبر 2024</p>
        <br>
        <p>محاكي لبيئة تطوير متكاملة باللغة العربية</p>
        <p>يدعم الكتابة من اليمين لليسار والواجهة العربية الكاملة</p>
        <br>
        <p><b>المطور:</b> فريق المترجم العربي</p>
        <p><b>حقوق النشر:</b> © 2024 جميع الحقوق محفوظة</p>
        </div>
        """
        QMessageBox.about(self, "حول البرنامج", about_text)
        
    def show_guide(self):
        """دليل الاستخدام"""
        guide_text = """
        دليل الاستخدام السريع:
        
        🔸 كتابة الكود: استخدم منطقة المحرر لكتابة الكود العربي
        🔸 التشغيل: اضغط F5 أو زر "تشغيل" لتحليل الكود
        🔸 الحفظ: استخدم Ctrl+S لحفظ الملف
        🔸 التحليلات: استخدم قائمة "عرض" لإظهار التحليلات المختلفة
        🔸 النمط: يمكنك تبديل النمط الفاتح/الداكن من قائمة "عرض"
        
        للمزيد من المساعدة، راجع قائمة "مساعدة"
        """
        QMessageBox.information(self, "دليل الاستخدام", guide_text)
        
    def show_developer(self):
        """عن المطور"""
        dev_text = """
        🧑‍💻 فريق تطوير المترجم العربي
        
        تم تطوير هذا البرنامج كمشروع تعليمي لمحاكاة 
        بيئة التطوير المتكاملة باللغة العربية
        
        الهدف: تسهيل تعلم البرمجة باللغة العربية
        التقنيات: Python + PyQt5
        
        نسعى لتطوير البرمجة العربية! 🚀
        """
        QMessageBox.information(self, "عن المطور", dev_text)
        
    def show_contact(self):
        """تواصل معنا"""
        contact_text = """
        🌐 للتواصل معنا:
        
        📧 البريد الإلكتروني: info@arabic-compiler.com
        🐙 GitHub: github.com/arabic-compiler
        🌐 الموقع: www.arabic-compiler.com
        📱 تويتر: @ArabicCompiler
        
        نرحب بملاحظاتكم واقتراحاتكم! 💙
        """
        QMessageBox.information(self, "تواصل معنا", contact_text)
        
    # وظائف المحاكاة
    def simulate_lexical_analysis(self, code):
        """محاكاة التحليل المعجمي"""
        self.log_to_console("📜 بدء التحليل المعجمي...")
        
        # كلمات مفتاحية عربية
        arabic_keywords = ['إعلان', 'متغير', 'طباعة', 'إذا', 'وإلا', 'كرر', 'دالة', 'إرجاع']
        
        tokens = []
        words = code.split()
        
        for word in words:
            if word in arabic_keywords:
                tokens.append(f"KEYWORD: {word}")
            elif word.isdigit() or any(c in '١٢٣٤٥٦٧٨٩٠' for c in word):
                tokens.append(f"NUMBER: {word}")
            elif word.startswith('"') and word.endswith('"'):
                tokens.append(f"STRING: {word}")
            elif word in ['=', '+', '-', '*', '/']:
                tokens.append(f"OPERATOR: {word}")
            else:
                tokens.append(f"IDENTIFIER: {word}")
                
        self.log_to_console("الرموز المستخرجة:")
        for token in tokens[:10]:  # عرض أول 10 رموز
            self.log_to_console(f"  • {token}")
            
        if len(tokens) > 10:
            self.log_to_console(f"  ... و {len(tokens) - 10} رموز أخرى")
            
        self.log_to_console("✅ اكتمل التحليل المعجمي بنجاح")
        
    def simulate_syntax_analysis(self, code):
        """محاكاة التحليل النحوي"""
        self.log_to_console("🧠 بدء التحليل النحوي...")
        
        lines = code.split('\n')
        errors = []
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # فحص بسيط للبناء النحوي
            if line.startswith('إعلان'):
                if '=' not in line:
                    errors.append(f"السطر {i}: مطلوب تعيين قيمة للمتغير")
            elif line.startswith('طباعة'):
                if '(' not in line or ')' not in line:
                    errors.append(f"السطر {i}: مطلوب أقواس للدالة طباعة")
                    
        if errors:
            self.log_to_console("❌ أخطاء نحوية:", "error")
            for error in errors:
                self.log_to_console(f"  • {error}", "error")
        else:
            self.log_to_console("✅ لا توجد أخطاء نحوية")
            self.log_to_console("الشجرة النحوية:")
            self.log_to_console("  Program")
            self.log_to_console("  ├── Declarations")
            self.log_to_console("  └── Statements")
            
        self.log_to_console("✅ اكتمل التحليل النحوي")
        
    def simulate_semantic_analysis(self, code):
        """محاكاة التحليل الدلالي"""
        self.log_to_console("🧩 بدء التحليل الدلالي...")
        
        # فحص دلالي بسيط
        declared_vars = []
        used_vars = []
        
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('إعلان متغير'):
                parts = line.split()
                if len(parts) >= 3:
                    var_name = parts[2]
                    declared_vars.append(var_name)
            elif 'طباعة' in line:
                # استخراج المتغيرات المستخدمة
                import re
                vars_in_line = re.findall(r'\b[أ-ي]+\b', line)
                for var in vars_in_line:
                    if var not in ['طباعة']:
                        used_vars.append(var)
                        
        # فحص المتغيرات غير المعرفة
        undefined_vars = [var for var in used_vars if var not in declared_vars]
        
        if undefined_vars:
            self.log_to_console("⚠️ تحذيرات دلالية:", "warning")
            for var in undefined_vars:
                self.log_to_console(f"  • المتغير '{var}' مستخدم بدون تعريف", "warning")
        else:
            self.log_to_console("✅ لا توجد أخطاء دلالية")
            
        self.log_to_console("المتغيرات المعرفة:", "success")
        for var in declared_vars:
            self.log_to_console(f"  • {var}", "success")
            
        self.log_to_console("✅ اكتمل التحليل الدلالي")
        
    def simulate_execution(self, code):
        """محاكاة التنفيذ"""
        self.log_to_console("⚡ بدء التنفيذ...")
        
        lines = code.split('\n')
        variables = {}
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                if line.startswith('إعلان متغير'):
                    # تحليل تعريف المتغير
                    parts = line.split(' = ')
                    if len(parts) == 2:
                        var_info = parts[0].split()
                        if len(var_info) >= 3:
                            var_name = var_info[2]
                            value = parts[1]
                            
                            # تحويل الأرقام العربية
                            arabic_to_english = str.maketrans('١٢٣٤٥٦٧٨٩٠', '1234567890')
                            value = value.translate(arabic_to_english)
                            
                            if value.isdigit():
                                variables[var_name] = int(value)
                            else:
                                variables[var_name] = value.strip('"\'')
                                
                            self.log_to_console(f"تم تعيين {var_name} = {variables[var_name]}", "success")
                            
                elif line.startswith('طباعة'):
                    # تحليل أمر الطباعة
                    content = line[line.find('(')+1:line.rfind(')')]
                    if content in variables:
                        output = variables[content]
                    else:
                        output = content.strip('"\'')
                        
                    self.log_to_console(f"📤 المخرجات: {output}", "output")
                    
            except Exception as e:
                self.log_to_console(f"❌ خطأ في السطر {i}: {str(e)}", "error")
                
        self.log_to_console("✅ اكتمل التنفيذ بنجاح")

    def run_compiler_and_capture(self, code):
        """استدعي الدالة compile_and_run من main1 واحتجز مخرجات stdout/stderr (بما في ذلك مخرجات العمليات الفرعية).

        Returns: (success, generated_code, ast, errors, captured_output_str)
        """
        try:
            import main1
        except Exception as e:
            raise ImportError(f"تعذر استيراد main1: {e}")

        import sys, os

        # افتح قناة لقراءة ما سيكتب على مستوى النظام (file descriptor)
        r_fd, w_fd = os.pipe()

        # تأكد من تفريغ stdout/stderr الحالية
        sys.stdout.flush()
        sys.stderr.flush()

        saved_stdout = os.dup(1)
        saved_stderr = os.dup(2)

        # أعد توجيه stdout و stderr إلى نهاية الكتابة للبايب
        os.dup2(w_fd, 1)
        os.dup2(w_fd, 2)

        # أغلق descriptor للكتابة في العملية الحالية (بعد النسخ)
        os.close(w_fd)

        try:
            # استدعاء المترجم - هذا قد يطلق subprocesss التي ترث الـ fds المعاد توجيهها
            success, generated_code, ast, errors = main1.compile_and_run(code, verbose=True, execute=True, output_file=None)
        finally:
            # استعادة stdout/stderr الأصلية
            os.dup2(saved_stdout, 1)
            os.dup2(saved_stderr, 2)
            os.close(saved_stdout)
            os.close(saved_stderr)

        # قراءة كل ما تم كتابته إلى البايب
        captured_bytes = []
        try:
            while True:
                chunk = os.read(r_fd, 4096)
                if not chunk:
                    break
                captured_bytes.append(chunk)
        finally:
            os.close(r_fd)

        captured = b"".join(captured_bytes).decode('utf-8', errors='replace')
        return success, generated_code, ast, errors, captured
        
    # وظائف مساعدة
    def log_to_console(self, message, msg_type="info"):
        """إضافة رسالة لوحدة التحكم"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if msg_type == "error":
            formatted_msg = f"[{timestamp}] ❌ {message}"
        elif msg_type == "warning":
            formatted_msg = f"[{timestamp}] ⚠️ {message}"
        elif msg_type == "success":
            formatted_msg = f"[{timestamp}] ✅ {message}"
        elif msg_type == "output":
            formatted_msg = f"[{timestamp}] 📤 {message}"
        else:
            formatted_msg = f"[{timestamp}] ℹ️ {message}"
            
        self.console_output.append(formatted_msg)
        
        # التمرير للأسفل
        scrollbar = self.console_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def clear_console(self):
        """مسح وحدة التحكم"""
        self.console_output.clear()
        welcome_msg = "🧾 تم مسح وحدة التحكم - جاهز لاستقبال مخرجات جديدة"
        self.console_output.setPlainText(welcome_msg)
        
    def update_time(self):
        """تحديث الوقت في شريط الحالة"""
        current_time = datetime.now().strftime(" %H:%M:%S")
        self.time_label.setText(current_time)
        
    def change_font(self):
        """تغيير خط المحرر"""
        font, ok = QFontDialog.getFont(self.text_editor.font(), self)
        if ok:
            self.text_editor.setFont(font)
            self.console_output.setFont(font)
            self.log_to_console(f"🔤 تم تغيير الخط إلى: {font.family()}")
            
    def on_file_selected(self, item):
        """عند اختيار ملف من القائمة"""
        self.log_to_console(f"📂 تم اختيار الملف: {item.text()}")
        
    def on_analysis_selected(self, item):
        """عند اختيار تحليل من القائمة"""
        analysis_name = item.text()
        self.log_to_console(f"🔍 تم اختيار: {analysis_name}")
        
        if "المعجمي" in analysis_name:
            self.show_lexical_analysis()
        elif "النحوي" in analysis_name:
            self.show_syntax_analysis()
        elif "الدلالي" in analysis_name:
            self.show_semantic_analysis()
        elif "الرموز" in analysis_name:
            self.show_symbol_table()
            
    def on_text_changed(self):
        """عند تغيير النص في المحرر"""
        # تحديث حالة الحفظ
        if self.current_file:
            self.file_info_label.setText(f"{os.path.basename(self.current_file)} *")
            
    def apply_dark_theme(self):
        """تطبيق النمط الداكن"""
        dark_style = """
        QMainWindow {
            background-color: #1E1E1E;
            color: #F5F5F5;
        }
        
        QMenuBar {
            background-color: #2D2D30;
            color: #F5F5F5;
            border-bottom: 1px solid #3E3E42;
            padding: 4px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        QMenuBar::item:selected {
            background-color: #3B3B98;
        }
        
        QMenu {
            background-color: #2D2D30;
            color: #F5F5F5;
            border: 1px solid #3E3E42;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 24px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #3B3B98;
        }
        
        QTextEdit {
            background-color: #0D1117;
            color: #F5F5F5;
            border: 1px solid #3E3E42;
            border-radius: 8px;
            padding: 8px;
            selection-background-color: #3B3B98;
        }
        
        QPushButton {
            background-color: #3B3B98;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #4A4AAA;
        }
        
        QPushButton:pressed {
            background-color: #2A2A88;
        }
        
        QTabWidget::pane {
            border: 1px solid #3E3E42;
            border-radius: 8px;
            background-color: #252526;
        }
        
        QTabBar::tab {
            background-color: #2D2D30;
            color: #F5F5F5;
            padding: 8px 16px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #3B3B98;
        }
        
        QListWidget {
            background-color: #252526;
            color: #F5F5F5;
            border: 1px solid #3E3E42;
            border-radius: 8px;
            padding: 4px;
        }
        
        QListWidget::item {
            padding: 8px;
            border-radius: 4px;
        }
        
        QListWidget::item:selected {
            background-color: #3B3B98;
        }
        
        QLabel {
            color: #F5F5F5;
        }
        
        QStatusBar {
            background-color: #2D2D30;
            color: #F5F5F5;
            border-top: 1px solid #3E3E42;
        }
        
        QSplitter::handle {
            background-color: #3E3E42;
        }
        
        QSplitter::handle:horizontal {
            width: 3px;
        }
        
        QSplitter::handle:vertical {
            height: 3px;
        }
        """
        
        self.setStyleSheet(dark_style)
        self.theme_toggle_btn.setText("☀️")
        
    def apply_light_theme(self):
        """تطبيق النمط الفاتح"""
        light_style = """
        QMainWindow {
            background-color: #FFFFFF;
            color: #000000;
        }
        
        QMenuBar {
            background-color: #F0F0F0;
            color: #000000;
            border-bottom: 1px solid #CCCCCC;
            padding: 4px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        QMenuBar::item:selected {
            background-color: #3B3B98;
            color: white;
        }
        
        QMenu {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 24px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #3B3B98;
            color: white;
        }
        
        QTextEdit {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            padding: 8px;
            selection-background-color: #3B3B98;
        }
        
        QPushButton {
            background-color: #3B3B98;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #4A4AAA;
        }
        
        QPushButton:pressed {
            background-color: #2A2A88;
        }
        
        QTabWidget::pane {
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            background-color: #F8F8F8;
        }
        
        QTabBar::tab {
            background-color: #E0E0E0;
            color: #000000;
            padding: 8px 16px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #3B3B98;
            color: white;
        }
        
        QListWidget {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            padding: 4px;
        }
        
        QListWidget::item {
            padding: 8px;
            border-radius: 4px;
        }
        
        QListWidget::item:selected {
            background-color: #3B3B98;
            color: white;
        }
        
        QLabel {
            color: #000000;
        }
        
        QStatusBar {
            background-color: #F0F0F0;
            color: #000000;
            border-top: 1px solid #CCCCCC;
        }
        
        QSplitter::handle {
            background-color: #CCCCCC;
        }
        
        QSplitter::handle:horizontal {
            width: 3px;
        }
        
        QSplitter::handle:vertical {
            height: 3px;
        }
        """
        
        self.setStyleSheet(light_style)
        self.theme_toggle_btn.setText("🌙")
    def eventFilter(self, obj, event):
        """معالج الأحداث للكونسول - للإدخال التفاعلي"""
        if obj == self.console_output and self.waiting_for_input:
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    # عند الضغط على Enter
                    self.waiting_for_input = False
                    if self.input_callback:
                        self.input_callback(self.input_buffer)
                    self.input_buffer = ""
                    return True
                elif event.key() == Qt.Key_Backspace:
                    # معالجة الحذف
                    if self.input_buffer:
                        self.input_buffer = self.input_buffer[:-1]
                    return False
                elif len(event.text()) > 0 and event.text().isprintable():
                    # إضافة الحرف المكتوب
                    self.input_buffer += event.text()
            return False
        return super().eventFilter(obj, event)
    def console_input(self, prompt=""):
        """دالة الإدخال من الكونسول - تحاكي input()"""
        from PyQt5.QtCore import QEventLoop
        
        # طباعة رسالة الطلب
        if prompt:
            self.console_output.insertPlainText(prompt)
        
        # تفعيل وضع الإدخال
        self.waiting_for_input = True
        self.input_buffer = ""
        result = None
        
        # حلقة انتظار
        loop = QEventLoop()
        
        def callback(value):
            nonlocal result
            result = value
            loop.quit()
        
        self.input_callback = callback
        self.console_output.setFocus()
        loop.exec_()
        
        # طباعة السطر الجديد
        self.console_output.insertPlainText("\n")
        return result



def main():
    """الدالة الرئيسية"""
    app = QApplication(sys.argv)
    
    # تعيين معلومات التطبيق
    app.setApplicationName("المترجم العربي")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Arabic Compiler Team")
    
    # تعيين اتجاه النص الافتراضي
    app.setLayoutDirection(Qt.RightToLeft)
    
    # إنشاء النافذة الرئيسية
    window = ArabicCompilerIDE()
    window.show()
    
    # تشغيل التطبيق
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()