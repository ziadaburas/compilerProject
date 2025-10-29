#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج: حساب_الدائرة
Program: حساب_الدائرة
مولّد تلقائياً من مترجم اللغة العربية البرمجية
Auto-generated from Arabic Programming Language Compiler
"""

import sys
import math

# ===== الثوابت - Constants =====
باي = 3.14  # ثابت - Constant

# ===== المتغيرات - Variables =====
# نصف_القطر: حقيقي
# المساحة: حقيقي

# ===== الإجراءات - Procedures =====
def احسب_مساحة(س, ر):
    """اجراء - Procedure: احسب_مساحة"""
    نتيجة = 0.0
    نتيجة = ((باي * ر) * ر)
    س = نتيجة
    print("المساحة: ", س)


# ===== البرنامج الرئيسي - Main Program =====
def main():
    نصف_القطر = 0.0
    المساحة = 0.0
    نصف_القطر = float(input())
    احسب_مساحة(المساحة, نصف_القطر)
    print("المساحة: ", المساحة)

if __name__ == '__main__':
    main()