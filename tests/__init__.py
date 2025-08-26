#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# 自动添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
