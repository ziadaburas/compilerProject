import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from compiler_analyzer import get_lexical_analysis, get_syntax_analysis, get_semantic_analysis
from antlr4 import InputStream, CommonTokenStream
from ArabicGrammarLexer import ArabicGrammarLexer
from ArabicGrammarParser import ArabicGrammarParser
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator

class ArabicCompilerIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.dark_mode = True
        self.waiting_for_input = False  # ← أضف هذا السطر
        self.input_buffer = ""  # ← أضف هذا السطر
        self.input_callback = None  # ← أضف هذا السطر
        self.console_output=None
        self.editor_widget= None
        self.open_files = []  # قائمة الملفات المفتوحة
        self.current_file_index = -1  # فهرس الملف الحالي
        self.running_process = None  # العملية قيد التشغيل
        self.is_running = False  # حالة التنفيذ
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
        
        codegen_action = QAction("🐍 عرض الكود المولد", self)
        codegen_action.triggered.connect(self.show_generated_code)
        view_menu.addAction(codegen_action)
        
        view_menu.addSeparator()
        
        theme_action = QAction("🎨 تغيير النمط (فاتح / داكن)", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        
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
        
        # ربط تغيير النص
        self.text_editor.textChanged.connect(self.on_text_changed)
        
    # وظائف القوائم
    def new_file(self):
        """إنشاء ملف جديد"""
        if self.text_editor.toPlainText().strip() and self.text_editor.document().isModified():
            reply = QMessageBox.question(
                self, "ملف جديد", 
                "هل تريد حفظ التغييرات الحالية؟",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return
        
        self.text_editor.clear()
        self.current_file = None
        self.current_file_index = -1
        
        self.file_info_label.setText("ملف جديد")
        self.file_name_label.setText("📁 ملف جديد")
        self.log_to_console("📄 تم إنشاء ملف جديد")
        
        # إضافة ملف جديد للقائمة (اختياري)
        # يمكنك حذف هذا الجزء إذا لم ترد إضافة ملفات جديدة للقائمة قبل حفظها

        
    def open_file(self):
        """فتح ملف وإضافته للقائمة الجانبية"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "فتح ملف", "", 
            "ملفات نصية (*.txt);;ملفات الكود (*.code);;جميع الملفات (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                # التحقق إذا كان الملف مفتوح مسبقاً
                if file_path in self.open_files:
                    # الانتقال إلى الملف المفتوح
                    index = self.open_files.index(file_path)
                    self.switch_to_file(index)
                    self.log_to_console(f"📂 الملف مفتوح مسبقاً: {os.path.basename(file_path)}")
                else:
                    # إضافة الملف الجديد
                    self.text_editor.setPlainText(content)
                    self.current_file = file_path
                    
                    # إضافة للقائمة
                    self.open_files.append(file_path)
                    self.current_file_index = len(self.open_files) - 1
                    
                    # تحديث القائمة الجانبية
                    self.update_files_list()
                    
                    file_name = os.path.basename(file_path)
                    self.file_info_label.setText(file_name)
                    self.file_name_label.setText(f"📁 {file_name}")
                    self.log_to_console(f"📂 تم فتح الملف: {file_name}")
                    
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"لا يمكن فتح الملف:\n{str(e)}")

    def update_files_list(self):
        """تحديث قائمة الملفات المفتوحة في الشريط الجانبي"""
        self.files_list.clear()
        
        for i, file_path in enumerate(self.open_files):
            file_name = os.path.basename(file_path)
            item = QListWidgetItem(f"📄 {file_name}")
            
            # تلوين الملف الحالي
            if i == self.current_file_index:
                # اللون الأزرق للملف النشط
                item.setBackground(QColor(52, 152, 219))  # أزرق
                item.setForeground(QColor(255, 255, 255))  # نص أبيض
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            
            # حفظ مسار الملف في البيانات
            item.setData(Qt.UserRole, file_path)
            self.files_list.addItem(item)

    def switch_to_file(self, index):
        """الانتقال إلى ملف معين"""
        if 0 <= index < len(self.open_files):
            # حفظ محتوى الملف الحالي إذا كان هناك تغييرات
            if self.current_file_index >= 0 and self.text_editor.document().isModified():
                reply = QMessageBox.question(
                    self, "حفظ التغييرات", 
                    "هل تريد حفظ التغييرات قبل التبديل؟",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
                if reply == QMessageBox.Yes:
                    self.save_file()
                elif reply == QMessageBox.Cancel:
                    return
            
            # التبديل إلى الملف الجديد
            file_path = self.open_files[index]
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.text_editor.setPlainText(content)
                self.current_file = file_path
                self.current_file_index = index
                
                file_name = os.path.basename(file_path)
                self.file_info_label.setText(file_name)
                self.file_name_label.setText(f"📁 {file_name}")
                
                # تحديث القائمة لتمييز الملف النشط
                self.update_files_list()
                
                self.log_to_console(f"🔄 تم التبديل إلى: {file_name}")
                
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"لا يمكن قراءة الملف:\n{str(e)}")

                
    def save_file(self):
        """حفظ الملف الحالي"""
        if self.current_file:
            # الملف موجود، احفظه مباشرة
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.toPlainText())
                
                # إعادة تعيين حالة التعديل
                self.text_editor.document().setModified(False)
                
                file_name = os.path.basename(self.current_file)
                self.log_to_console(f"💾 تم حفظ الملف: {file_name}")
                
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"لا يمكن حفظ الملف:\n{str(e)}")
        else:
            # لا يوجد ملف، استخدم حفظ باسم
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
                
                # تحديث المسار الحالي
                old_file = self.current_file
                self.current_file = file_path
                
                # تحديث القائمة
                if old_file and old_file in self.open_files:
                    # استبدال المسار القديم بالجديد
                    index = self.open_files.index(old_file)
                    self.open_files[index] = file_path
                else:
                    # إضافة ملف جديد
                    self.open_files.append(file_path)
                    self.current_file_index = len(self.open_files) - 1
                
                # تحديث الواجهة
                file_name = os.path.basename(file_path)
                self.file_info_label.setText(file_name)
                self.file_name_label.setText(f"📁 {file_name}")
                self.update_files_list()
                
                # إعادة تعيين حالة التعديل
                self.text_editor.document().setModified(False)
                
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
            self.is_running = True

            # مسح الكونسول
            self.console_output.clear()
            
            # الحصول على الكود المصدري 
            source_code = self.text_editor.toPlainText()
            if not source_code.strip():
                self.console_output.setPlainText("❌ لا يوجد كود للتشغيل!")
                return
            
           
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

   
    def stop_execution(self):
        """إيقاف التنفيذ"""
        if self.is_running:
            self.is_running = False
            
            # إيقاف العملية إذا كانت موجودة
            if self.running_process:
                try:
                    self.running_process.terminate()
                    self.running_process = None
                except:
                    pass
            
            self.log_to_console("🛑 تم إيقاف التنفيذ", "error")
            
        else:
            self.log_to_console("⚠️ لا يوجد تنفيذ قيد العمل", "warning")
        

        
    
    def show_lexical_analysis(self):
        """عرض التحليل المعجمي الفعلي"""
        code = self.text_editor.toPlainText().strip()
        if not code:
            self.log_to_console("⚠️ لا يوجد كود للتحليل", "warning")
            return
        
        try:
            # الحصول على التحليل المعجمي الفعلي
            result = get_lexical_analysis(code)
            
            self.log_to_console("📜 ═══════════════ التحليل المعجمي ═══════════════")
            
            if result['success']:
                self.log_to_console(f"✅ تم التحليل بنجاح - عدد الرموز: {result['token_count']}")
                self.log_to_console("")
                self.log_to_console("الرموز المستخرجة:")
                self.log_to_console("─" * 70)
                
                for i, token in enumerate(result['tokens'], 1):
                    token_line = f"{i}. [{token['type']}] '{token['text']}' (سطر: {token['line']}, عمود: {token['column']})"
                    self.log_to_console(token_line)
                
                self.log_to_console("─" * 70)
                self.log_to_console(f"✅ إجمالي الرموز: {len(result['tokens'])}")
            else:
                self.log_to_console(f"❌ خطأ في التحليل المعجمي: {result.get('error', 'خطأ غير معروف')}", "error")
            
        except Exception as e:
            self.log_to_console(f"❌ خطأ في التحليل المعجمي: {str(e)}", "error")

            
    def show_syntax_analysis(self):
        """عرض التحليل النحوي الفعلي بشكل منسق"""
        code = self.text_editor.toPlainText().strip()
        if not code:
            self.log_to_console("⚠️ لا يوجد كود للتحليل", "warning")
            return
        
        try:
            # الحصول على التحليل النحوي الفعلي
            result = get_syntax_analysis(code)
            
            self.log_to_console("🧠 ═══════════════ التحليل النحوي ═══════════════")
            
            if result['success']:
                self.log_to_console("✅ التحليل النحوي ناجح - لا توجد أخطاء نحوية")
                self.log_to_console("")
                self.log_to_console("🌲 شجرة التحليل النحوي (Parse Tree):")
                self.log_to_console("─" * 70)
                
                if result.get('tree_formatted'):
                    # عرض الشجرة المنسقة
                    for line in result['tree_formatted']:
                        self.log_to_console(line)
                elif result.get('tree_raw'):
                    # fallback للعرض الخام إذا فشل التنسيق
                    self.log_to_console("📋 العرض الخام للشجرة:")
                    tree_lines = result['tree_raw'].split('\n')
                    for line in tree_lines[:30]:  # عرض أول 30 سطر
                        self.log_to_console(line)
                    
                    if len(tree_lines) > 30:
                        self.log_to_console(f"... ({len(tree_lines) - 30} سطر إضافي)")
                
                self.log_to_console("─" * 70)
                self.log_to_console("✅ البنية النحوية صحيحة")
            else:
                self.log_to_console(f"❌ عدد الأخطاء النحوية: {result.get('error_count', 0)}", "error")
                if 'error' in result:
                    self.log_to_console(f"❌ {result['error']}", "error")
            
        except Exception as e:
            self.log_to_console(f"❌ خطأ في التحليل النحوي: {str(e)}", "error")


            
    def show_semantic_analysis(self):
        """عرض التحليل الدلالي الفعلي بشكل شامل (بدون جدول الرموز)"""
        code = self.text_editor.toPlainText().strip()
        if not code:
            self.log_to_console("⚠️ لا يوجد كود للتحليل", "warning")
            return
        
        try:
            # الحصول على التحليل الدلالي الفعلي
            result = get_semantic_analysis(code)
            
            self.log_to_console("🧩 ═══════════════════════════════════════════════════")
            self.log_to_console("         التحليل الدلالي - Semantic Analysis")
            self.log_to_console("═══════════════════════════════════════════════════")
            self.log_to_console("")
            
            # ═══════════ القسم 1: الحالة العامة ═══════════
            if result['success']:
                self.log_to_console("✅ التحليل الدلالي ناجح - لا توجد أخطاء دلالية")
            else:
                self.log_to_console(f"❌ فشل التحليل الدلالي - عدد الأخطاء: {len(result['errors'])}", "error")
            
            self.log_to_console("")
            self.log_to_console("─" * 70)
            
            # ═══════════ القسم 2: الإحصائيات ═══════════
            if 'statistics' in result and result['statistics']:
                self.log_to_console("")
                self.log_to_console("📊 إحصائيات التحليل الدلالي:")
                self.log_to_console("─" * 70)
                stats = result['statistics']
                self.log_to_console(f"  📌 إجمالي الرموز المعرفة: {stats['total_symbols']}")
                self.log_to_console(f"  📊 المتغيرات: {stats['variables']}")
                self.log_to_console(f"  🔒 الثوابت: {stats['constants']}")
                self.log_to_console(f"  ⚙️ الإجراءات: {stats['procedures']}")
                self.log_to_console(f"  📝 المعاملات: {stats['parameters']}")
                self.log_to_console(f"  🏷️ الأنواع المخصصة: {stats['types']}")
                self.log_to_console(f"  ❌ الأخطاء الدلالية: {stats['total_errors']}")
                self.log_to_console("─" * 70)
            
            # ═══════════ القسم 3: شجرة AST ═══════════
            if result.get('ast_formatted'):
                self.log_to_console("")
                self.log_to_console("🌳 شجرة البناء المجردة (Abstract Syntax Tree - AST):")
                self.log_to_console("─" * 70)
                self.log_to_console("الشجرة بعد الإثراء الدلالي (Semantic Enrichment):")
                self.log_to_console("")
                
                for line in result['ast_formatted']:
                    self.log_to_console(line)
                
                self.log_to_console("─" * 70)
                self.log_to_console("✅ تم بناء شجرة AST بنجاح")
            
            # ═══════════ القسم 4: تقرير الأخطاء الدلالية ═══════════
            if result.get('errors_formatted') and len(result['errors_formatted']) > 0:
                self.log_to_console("")
                self.log_to_console("❌ تقرير الأخطاء الدلالية (Semantic Error Report):", "error")
                self.log_to_console("─" * 70)
                
                for error in result['errors_formatted']:
                    self.log_to_console("", "error")
                    self.log_to_console(f"🔴 خطأ رقم {error['number']}:", "error")
                    self.log_to_console(f"   النوع: {error.get('type', 'غير محدد')}", "error")
                    self.log_to_console(f"   الرسالة: {error['message']}", "error")
                    
                    if error.get('line'):
                        self.log_to_console(f"   الموقع: السطر {error['line']}", "error")
                        if error.get('column'):
                            self.log_to_console(f"            العمود {error['column']}", "error")
                    
                    self.log_to_console(f"   الخطورة: {error['severity']}", "error")
                    self.log_to_console("   " + "─" * 60, "error")
                
                self.log_to_console("")
                self.log_to_console(f"❌ إجمالي الأخطاء: {len(result['errors_formatted'])}", "error")
            elif result['success']:
                self.log_to_console("")
                self.log_to_console("✅ لا توجد أخطاء دلالية - البرنامج صحيح دلالياً")
            
            # ═══════════ القسم 5: ملخص التحليل ═══════════
            self.log_to_console("")
            self.log_to_console("═══════════════════════════════════════════════════")
            self.log_to_console("                   ملخص التحليل")
            self.log_to_console("═══════════════════════════════════════════════════")
            
            if result['success']:
                self.log_to_console("✅ اكتمل التحليل الدلالي بنجاح", "success")
                self.log_to_console("✓ تم بناء شجرة AST")
                self.log_to_console("✓ تم التحقق من الأنواع")
                self.log_to_console("✓ تم التحقق من النطاقات")
                self.log_to_console("✓ البرنامج جاهز لتوليد الكود")
            else:
                self.log_to_console("❌ فشل التحليل الدلالي - يرجى تصحيح الأخطاء", "error")
            
            self.log_to_console("═══════════════════════════════════════════════════")
            
        except Exception as e:
            self.log_to_console(f"❌ خطأ في التحليل الدلالي: {str(e)}", "error")

            
    
    def show_generated_code(self):
        """عرض الكود المولد (Python Code Generation)"""
        code = self.text_editor.toPlainText().strip()
        if not code:
            self.log_to_console("⚠️ لا يوجد كود لتوليده", "warning")
            return
        
        try:
            # استيراد دالة توليد الكود
            from compiler_analyzer import generate_intermediate_code
            
            # توليد الكود
            result = generate_intermediate_code(code)
            
            self.log_to_console("🐍 ═══════════════════════════════════════════════════")
            self.log_to_console("         توليد الكود - Code Generation")
            self.log_to_console("═══════════════════════════════════════════════════")
            self.log_to_console("")
            
            if result['success']:
                self.log_to_console("✅ تم توليد الكود بنجاح")
                self.log_to_console("")
                self.log_to_console("📝 الكود المولد (Python Code):")
                self.log_to_console("─" * 70)
                self.log_to_console("")
                
                # عرض الكود المولد مع أرقام الأسطر
                generated_code = result['code']
                lines = generated_code.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # إضافة رقم السطر
                    line_num = f"{i:3d} │ "
                    self.log_to_console(line_num + line)
                
                self.log_to_console("")
                self.log_to_console("─" * 70)
                self.log_to_console(f"✅ عدد الأسطر المولدة: {len(lines)}")
                self.log_to_console("")
                self.log_to_console("💡 ملاحظة: هذا الكود جاهز للتنفيذ في بيئة Python")
                
            else:
                self.log_to_console("❌ فشل توليد الكود", "error")
                self.log_to_console("")
                
                if 'errors' in result and result['errors']:
                    self.log_to_console("قائمة الأخطاء:", "error")
                    for i, error in enumerate(result['errors'], 1):
                        self.log_to_console(f"  {i}. {error}", "error")
                
                if 'error' in result:
                    self.log_to_console(f"تفاصيل الخطأ: {result['error']}", "error")
            
            self.log_to_console("")
            self.log_to_console("═══════════════════════════════════════════════════")
            
        except Exception as e:
            self.log_to_console(f"❌ خطأ في توليد الكود: {str(e)}", "error")

        
        
    def toggle_theme(self):
        """تبديل النمط"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_theme()
            self.log_to_console("🌙 تم تطبيق النمط الداكن")
        else:
            self.apply_light_theme()
            self.log_to_console("☀️ تم تطبيق النمط الفاتح")
            
    def run_compiler_and_capture(self, code):
        """استدعي الدالة compile_and_run من main1 واحتجز مخرجات stdout/stderr (بما في ذلك مخرجات العمليات الفرعية).

        Returns: (success, generated_code, ast, errors, captured_output_str)
        """
        
        

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
        
        
    def on_file_selected(self, item):
        """معالج اختيار ملف من القائمة الجانبية"""
        # الحصول على مسار الملف من البيانات
        file_path = item.data(Qt.UserRole)
        
        if file_path and file_path in self.open_files:
            index = self.open_files.index(file_path)
            self.switch_to_file(index)

        
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