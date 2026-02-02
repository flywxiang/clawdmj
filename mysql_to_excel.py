#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL报表生成脚本
每周一凌晨执行，将MySQL查询结果导出为Excel文件
"""

import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 配置
OUTPUT_DIR = '/root/mysql_report'
CONFIG_FILE = '/root/mysql_report/config.json'

# 默认MySQL配置（用户需要修改）
DEFAULT_CONFIG = {
    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'your_password',
        'database': 'your_database'
    },
    'queries': [
        {
            'name': '示例查询1',
            'sheet_name': 'Sheet1',
            'sql': 'SELECT * FROM users LIMIT 100'
        }
    ]
}


def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 创建默认配置文件
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        logger.info(f"已创建默认配置文件: {CONFIG_FILE}")
        logger.warning("请修改配置文件中的MySQL连接信息和查询语句")
        return DEFAULT_CONFIG


def connect_mysql(config):
    """连接MySQL数据库"""
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset='utf8mb4'
        )
        logger.info("MySQL连接成功")
        return conn
    except mysql.connector.Error as e:
        logger.error(f"MySQL连接失败: {e}")
        return None


def execute_queries(conn, queries):
    """执行查询并返回结果"""
    results = []
    cursor = conn.cursor()

    for query in queries:
        try:
            logger.info(f"执行查询: {query['name']}")
            cursor.execute(query['sql'])

            # 获取列名
            columns = [desc[0] for desc in cursor.description]

            # 获取数据
            data = cursor.fetchall()

            # 转换为DataFrame
            df = pd.DataFrame(data, columns=columns)

            results.append({
                'name': query['name'],
                'sheet_name': query['sheet_name'],
                'data': df,
                'rows': len(df)
            })

            logger.info(f"查询完成，共 {len(df)} 行")

        except mysql.connector.Error as e:
            logger.error(f"查询执行失败 [{query['name']}]: {e}")
            results.append({
                'name': query['name'],
                'sheet_name': query['sheet_name'],
                'data': pd.DataFrame(),
                'error': str(e)
            })

    cursor.close()
    return results


def save_to_excel(results):
    """保存为Excel文件"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'mysql_report_{timestamp}.xlsx'
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for result in results:
                if 'error' not in result and len(result['data']) > 0:
                    result['data'].to_excel(
                        writer,
                        sheet_name=result['sheet_name'],
                        index=False
                    )
                else:
                    # 创建空Sheet并写入错误信息
                    pd.DataFrame({'Error': [result.get('error', 'No data')]})\
                        .to_excel(writer, sheet_name=result['sheet_name'], index=False)

        logger.info(f"Excel文件已保存: {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"保存Excel失败: {e}")
        return None


def commit_to_github(filepath):
    """提交到GitHub仓库"""
    repo_path = OUTPUT_DIR
    repo_url = 'https://github.com/flywxiang/clawdmj.git'

    try:
        # 检查是否是Git仓库
        if not os.path.exists(os.path.join(repo_path, '.git')):
            logger.info("初始化Git仓库...")
            os.chdir(repo_path)
            os.system('git init')
            os.system(f'git remote add origin {repo_url}')
        else:
            os.chdir(repo_path)

        # 添加文件
        os.system(f'git add {os.path.basename(filepath)}')

        # 提交
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = f"MySQL报表 - {timestamp}"
        os.system(f'git commit -m "{commit_msg}"')

        # 推送
        logger.info("推送到GitHub...")
        result = os.system('git push origin main')

        if result == 0:
            logger.info("GitHub推送成功")
        else:
            logger.warning("GitHub推送可能失败，请检查认证配置")

    except Exception as e:
        logger.error(f"Git操作失败: {e}")


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始执行MySQL报表生成任务")

    # 加载配置
    config = load_config()

    # 检查配置是否已修改
    if config['mysql']['password'] == 'your_password':
        logger.error("请先修改配置文件中的MySQL密码！")
        logger.error(f"配置文件位置: {CONFIG_FILE}")
        return

    # 连接数据库
    conn = connect_mysql(config['mysql'])
    if not conn:
        return

    try:
        # 执行查询
        results = execute_queries(conn, config['queries'])

        # 保存Excel
        filepath = save_to_excel(results)

        if filepath:
            # 提交到GitHub
            commit_to_github(filepath)

            logger.info("=" * 50)
            logger.info("任务执行完成！")
        else:
            logger.error("任务执行失败")

    finally:
        conn.close()
        logger.info("MySQL连接已关闭")


if __name__ == '__main__':
    main()
