#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
根据班级花名册 Excel 文件自动生成 config.py 配置文件。
Excel 要求：第一列为学号，第二列为姓名，无标题行。

使用方法：
    python generate_config.py 班级花名册.xlsx
"""

import sys
import os

# 尝试导入 pandas，若未安装则给出友好提示
try:
    import pandas as pd
except ImportError:
    print("错误：未找到 pandas 库。")
    print("请先安装 pandas 和 openpyxl：")
    print("    pip install pandas openpyxl")
    sys.exit(1)


def generate_config(excel_path: str, output_path: str = "config.py"):
    """读取 Excel 并生成 config.py"""
    if not os.path.exists(excel_path):
        print(f"错误：文件不存在 -> {excel_path}")
        sys.exit(1)

    try:
        df = pd.read_excel(excel_path, header=None, names=["学号", "姓名"])
    except Exception as e:
        print(f"读取 Excel 文件失败：{e}")
        sys.exit(1)

    if df.empty:
        print("警告：Excel 文件中没有数据，生成的配置文件将为空。")

    # 科目名称与对应的命名模板（{exp_num} 为占位符）
    SUBJECT_TEMPLATES = [
        ("操作系统", "实验{exp_num}_{学号}_{姓名}"),
        ("计算机组成原理", "实验{exp_num} - {学号} - {姓名}"),
        ("电子设计基础", "实验{exp_num}_{学号}_{姓名}"),
        ("深度学习实验", "实验{exp_num}_{学号}_{姓名}"),
        ("深度学习实践", "实践{exp_num}_{学号}_{姓名}"),
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# config.py\n")
        f.write("# 本文件由 generate_config.py 自动生成，请勿手动修改\n")
        f.write("# 如需更新，请重新运行脚本\n\n")
        f.write("SUBJECTS = {}\n\n")

        for subject, template in SUBJECT_TEMPLATES:
            # 将科目名转换为合法的 Python 变量名（全大写，空格替换为下划线）
            var_name = subject.upper().replace(" ", "_") + "_MAPPING"
            f.write(f"{var_name} = {{\n")
            for _, row in df.iterrows():
                student_id = row["学号"]
                name = row["姓名"]
                # 将模板中的 {exp_num} 保留为字符串占位符，学号和姓名直接填入
                standard_name = template.format(exp_num="{exp_num}", 学号=student_id, 姓名=name)
                f.write(f'    "{name}": "{standard_name}",\n')
            f.write("}\n\n")

        f.write("SUBJECTS = {\n")
        for subject, _ in SUBJECT_TEMPLATES:
            var_name = subject.upper().replace(" ", "_") + "_MAPPING"
            f.write(f'    "{subject}": {var_name},\n')
        f.write("}\n")

    print(f"✅ 配置文件已生成：{os.path.abspath(output_path)}")
    print(f"   包含 {len(df)} 名学生，{len(SUBJECT_TEMPLATES)} 门科目。")


def main():
    if len(sys.argv) != 2:
        print("使用方法：python generate_config.py <花名册文件.xlsx>")
        print("示例：python generate_config.py 班级花名册.xlsx")
        sys.exit(1)

    excel_file = sys.argv[1]
    generate_config(excel_file)


if __name__ == "__main__":
    main()