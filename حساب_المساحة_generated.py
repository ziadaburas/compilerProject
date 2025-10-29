#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج: حساب_المساحة
Program: حساب_المساحة
مولّد تلقائياً من مترجم اللغة العربية البرمجية
Auto-generated from Arabic Programming Language Compiler
"""

import sys
import math

# ===== المتغيرات - Variables =====
# طول, عرض, مساحة: صحيح

# ===== البرنامج الرئيسي - Main Program =====
def main():
    طول = 0
    عرض = 0
    مساحة = 0
    طول = int(input())
    عرض = int(input())
    مساحة = (طول * عرض)
    print(مساحة)

if __name__ == '__main__':
    main()