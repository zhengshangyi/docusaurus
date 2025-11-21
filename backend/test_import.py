#!/usr/bin/env python3
"""测试导入脚本"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from import_docs import main
    print("开始执行导入...")
    main()
    print("导入完成！")
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

