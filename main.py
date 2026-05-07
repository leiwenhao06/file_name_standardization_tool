#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实验报告文件名自动规范化工具（多科目 + 实验次数动态替换）
用法：
    python main.py [文件夹路径] [--subject 科目名] [--exp-num 实验编号] [--execute]
    --subject, -s : 选择使用哪个科目的映射字典（必须存在于 config.SUBJECTS 中）
    --exp-num, -e : 实验次数，将替换映射值中的 {exp_num} 占位符
    --execute      : 实际执行重命名，否则仅预览

示例：
    python main.py ./reports -s 操作系统 -e 1          # 仅预览操作系统实验1的文件夹
    python main.py ./reports -s 操作系统 -e 2 --execute  # 执行操作实验2重命名
"""

import os
import re
import sys
import argparse
from config import SUBJECTS

WORD_EXTENSIONS = ('.doc', '.docx', '.pdf')


def match_name(filename_no_ext: str, mapping: dict) -> tuple:
    """
    使用映射字典的 key 对文件名进行正则匹配。
    返回 (匹配的key, 对应的标准名称模板) 或 (None, None)
    """
    for key, std_template in mapping.items():
        # 默认对 key 进行普通字符串匹配（忽略大小写）
        # 若希望 key 为正则表达式，请将下一行改为 pattern = key
        pattern = re.escape(key)
        if re.search(pattern, filename_no_ext, re.IGNORECASE):
            return key, std_template
    return None, None


def generate_standard_name(template: str, exp_num: str) -> str:
    """
    将模板中的 {exp_num} 替换为实际实验次数。
    如果模板不含占位符，则直接返回原字符串。
    """
    try:
        return template.format(exp_num=exp_num)
    except KeyError:
        # 模板中没有 {exp_num}，忽略替换
        return template


def get_new_filename(old_name: str, std_name: str) -> str:
    """根据原文件扩展名和最终标准名称生成新文件名"""
    base, ext = os.path.splitext(old_name)
    return std_name + ext


def rename_reports(directory: str, mapping: dict, exp_num: str, execute: bool = False):
    """遍历目录，预览或执行重命名"""
    if not os.path.isdir(directory):
        print(f"错误：目录不存在 -> {directory}")
        return

    print(f"目标目录: {os.path.abspath(directory)}")
    print(f"实验次数: {exp_num}")
    print(f"{'预览模式' if not execute else '执行模式'}\n")

    files = [f for f in os.listdir(directory)
             if os.path.isfile(os.path.join(directory, f))
             and f.lower().endswith(WORD_EXTENSIONS)]

    if not files:
        print("未找到 Word 文档（.doc/.docx）。")
        return

    renamed_count = 0
    skipped_count = 0
    matched_names = set()

    for filename in files:
        name_no_ext, ext = os.path.splitext(filename)
        key, template = match_name(name_no_ext, mapping)

        if template is None:
            print(f"[跳过] {filename}  ->  未匹配到任何姓名")
            skipped_count += 1
            continue
        matched_names.add(key)

        # 生成最终标准名称（替换 {exp_num}）
        std_name = generate_standard_name(template, exp_num)
        new_filename = std_name + ext
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)

        # 冲突检查
        if os.path.exists(new_path) and old_path != new_path:
            print(f"[冲突] {filename}  ->  {new_filename}  (目标文件已存在)")
            skipped_count += 1
            continue

        if execute:
            try:
                os.rename(old_path, new_path)
                print(f"[重命名] {filename}  ->  {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"[错误] {filename}  ->  重命名失败: {e}")
                skipped_count += 1
        else:
            print(f"[预览] {filename}  ->  {new_filename}")
            renamed_count += 1

    print("\n" + "="*50)
    print(f"处理完成: 共 {len(files)} 个文件")
    print(f"可重命名: {renamed_count} 个, 跳过: {skipped_count} 个")
    print()
    # 未提交人员名单
    missing = set(mapping.keys()) - matched_names
    if missing:
        print(f"未提交人员名单 ({len(missing)}/{len(mapping)}):")
        for name in sorted(missing):
            print(f"  {name}")
    else:
        print("所有同学均已提交报告。")
    if not execute:
        print("提示: 使用 --execute 参数实际执行重命名。")


def main():
    parser = argparse.ArgumentParser(description="实验报告文件名规范化工具（多科目/实验次数）")
    parser.add_argument("directory", nargs="?", default=".",
                        help="要处理的文件夹路径（默认当前目录）")
    parser.add_argument("-s", "--subject", required=True,
                        help=f"科目名称，可选值: {', '.join(SUBJECTS.keys())}")
    parser.add_argument("-e", "--exp-num", required=True,
                        help="实验次数（如 1、2、3），将替换映射值中的 {exp_num}")
    parser.add_argument("--execute", action="store_true",
                        help="实际执行重命名操作，否则仅预览")
    args = parser.parse_args()

    # 检查科目是否存在
    if args.subject not in SUBJECTS:
        print(f"错误：未知科目 '{args.subject}'，可用科目: {', '.join(SUBJECTS.keys())}")
        sys.exit(1)

    mapping = SUBJECTS[args.subject]
    if not mapping:
        print(f"警告：科目 '{args.subject}' 的映射字典为空，请先配置。")
        return

    rename_reports(args.directory, mapping, args.exp_num, args.execute)


if __name__ == "__main__":
    main()
