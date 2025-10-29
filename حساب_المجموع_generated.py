#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج: حساب_المجموع
Program: حساب_المجموع
مولّد تلقائياً من مترجم اللغة العربية البرمجية
Auto-generated from Arabic Programming Language Compiler
"""

import sys
import math

# ===== المتغيرات - Variables =====
# عداد, مجموع, عدد: صحيح

# ===== البرنامج الرئيسي - Main Program =====
def main():
    عداد = 0
    مجموع = 0
    عدد = 0
    مجموع = 0
    for عداد in range(1, 3 + 1):
        عدد = int(input())
        if (عدد > 0):
            مجموع = (مجموع + عدد)
    print("المجموع: ", مجموع)

if __name__ == '__main__':
    main()