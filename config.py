# config.py 示例文件
# 本文件由 generate_config.py 自动生成
# 如需更新，请重新运行脚本

SUBJECTS = {}

操作系统_MAPPING = {
   "张三": "实验{exp_num}_2026001_张三",
   "李四": "实验{exp_num}_2026002_李四",
}

计算机组成原理_MAPPING = {
    "张三": "实验{exp_num} - 2026001 - 张三",
    "李四": "实验{exp_num} - 2026002 - 李四",
}   

SUBJECTS = {
    "操作系统": 操作系统_MAPPING,
    "计算机组成原理": 计算机组成原理_MAPPING,
}    
