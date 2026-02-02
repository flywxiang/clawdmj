# MySQL 报表生成系统

## 功能说明

- 每周一凌晨自动执行MySQL查询
- 将结果导出为Excel格式
- 自动提交到GitHub仓库

## 目录结构

```
/root/mysql_report/
├── mysql_to_excel.py      # 主脚本
├── config.json            # MySQL配置和查询语句
├── .gitignore            # Git忽略文件
└── mysql_report_*.xlsx   # 生成的Excel报表
```

## 配置说明

### 1. 修改MySQL连接信息

编辑 `config.json` 文件：

```json
{
  "mysql": {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "你的密码",
    "database": "你的数据库名"
  },
  "queries": [...]
}
```

### 2. 配置查询语句

在 `config.json` 的 `queries` 数组中添加你的查询：

```json
{
  "name": "查询名称",
  "sheet_name": "Excel工作表名称",
  "sql": "SELECT * FROM your_table"
}
```

### 3. 配置GitHub认证

推送到GitHub需要配置认证，选择以下方式之一：

**方式一：使用个人访问令牌（推荐）**
```bash
git remote set-url origin https://TOKEN@github.com/flywxiang/clawdmj.git
```

**方式二：使用SSH密钥**
```bash
git remote set-url origin git@github.com:flywxiang/clawdmj.git
```

## 手动执行

```bash
python3 /root/mysql_report/mysql_to_excel.py
```

## 定时任务

- 执行时间：每周一凌晨 0:00
- Cron表达式：`0 0 * * 1`
- 任务ID：[待创建]

## 生成的Excel文件

命名格式：`mysql_report_YYYYMMDD_HHMMSS.xlsx`

每个查询结果会保存在独立的Sheet中，Sheet名称由配置中的 `sheet_name` 指定。

## 注意事项

1. ⚠️ 首次使用前请修改 `config.json` 中的MySQL密码
2. 🔐 不要将包含敏感信息的 `config.json` 提交到公开仓库
3. 📝 确保MySQL数据库可以正常访问
4. 🔑 GitHub推送需要配置认证信息

## 测试

使用示例配置测试（查询MySQL版本信息）：

```bash
python3 /root/mysql_report/mysql_to_excel.py
```

成功后会在 `/root/mysql_report/` 目录生成Excel文件。
