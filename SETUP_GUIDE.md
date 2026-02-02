# MySQL报表系统设置完成

## 已完成配置

### ✅ 文件结构
```
/root/mysql_report/
├── mysql_to_excel.py      # 主脚本（可执行）
├── config.json            # MySQL配置和查询语句（需要修改）
├── .gitignore            # Git忽略文件
├── README.md             # 使用说明
├── SETUP_GUIDE.md        # 本文件
└── .git/                 # Git仓库（已初始化）
```

### ✅ Python依赖包
- mysql-connector-python
- pandas
- openpyxl

### ✅ 定时任务
- **执行时间**：每周一凌晨 0:00
- **Cron表达式**：`0 0 * * 1`
- **任务ID**：5f61438b-4b50-4634-951a-cdccbc752128

### ✅ GitHub仓库
- 仓库地址：https://github.com/flywxiang/clawdmj
- 仓库路径：/root/mysql_report/
- 已初始化Git仓库

---

## ⚠️ 需要用户完成的配置

### 1. 修改MySQL连接信息

编辑 `/root/mysql_report/config.json`：

```json
{
  "mysql": {
    "host": "localhost",        // MySQL服务器地址
    "port": 3306,               // 端口
    "user": "root",             // 用户名
    "password": "你的密码",      // ⬅️ 修改这里
    "database": "你的数据库名"   // ⬅️ 修改这里
  }
}
```

### 2. 配置查询语句

在 `config.json` 的 `queries` 数组中添加你的SQL查询：

```json
{
  "queries": [
    {
      "name": "订单汇总",
      "sheet_name": "订单数据",
      "sql": "SELECT * FROM orders WHERE create_time > DATE_SUB(NOW(), INTERVAL 7 DAY)"
    },
    {
      "name": "用户统计",
      "sheet_name": "用户数据",
      "sql": "SELECT COUNT(*) as total, status FROM users GROUP BY status"
    }
  ]
}
```

### 3. 配置GitHub认证

推送到GitHub需要配置认证，选择以下方式之一：

**方式一：使用个人访问令牌（推荐）**

1. 访问 https://github.com/settings/tokens
2. 生成新的Personal Access Token（权限：repo）
3. 执行：
```bash
cd /root/mysql_report
git remote set-url origin https://YOUR_TOKEN@github.com/flywxiang/clawdmj.git
```

**方式二：使用SSH密钥**

```bash
cd /root/mysql_report
git remote set-url origin git@github.com:flywxiang/clawdmj.git
```

---

## 测试运行

配置完成后，手动测试：

```bash
cd /root/mysql_report
python3 mysql_to_excel.py
```

成功后会：
1. 连接MySQL数据库
2. 执行配置中的查询
3. 生成Excel文件（格式：`mysql_report_YYYYMMDD_HHMMSS.xlsx`）
4. 提交到GitHub仓库

---

## 生成的Excel格式

每个查询对应一个Sheet：

```
mysql_report_20260202_134530.xlsx
├── Sheet1（配置的sheet_name）
│   ├── 列1 | 列2 | 列3 | ...
│   └── 数据行...
├── Sheet2
└── ...
```

---

## 定时任务管理

### 查看所有任务
```bash
openclaw cron list
```

### 查看MySQL报表任务
```bash
openclaw cron runs --id 5f61438b-4b50-4634-951a-cdccbc752128
```

### 禁用/启用任务
```bash
# 禁用
openclaw cron update --id 5f61438b-4b50-4634-951a-cdccbc752128 --patch '{"enabled": false}'

# 启用
openclaw cron update --id 5f61438b-4b50-4634-951a-cdccbc752128 --patch '{"enabled": true}'
```

### 立即执行（测试）
```bash
openclaw cron run --id 5f61438b-4b50-4634-951a-cdccbc752128
```

---

## 关于Excel格式

当前保存的是基础格式。如果你需要特定的Excel格式（如：
- 样式（字体、颜色、边框）
- 表头样式
- 数据格式化
- 图表
- 合并单元格
等），请提供具体要求，我会更新脚本。

---

## 故障排查

### MySQL连接失败
- 检查MySQL服务是否运行：`systemctl status mysql`
- 检查配置文件中的用户名、密码、数据库名是否正确
- 检查网络连接和防火墙设置

### 查询执行失败
- 在MySQL客户端中先测试SQL语句是否正确
- 检查表名、字段名是否正确
- 检查SQL语法是否正确

### Git推送失败
- 检查GitHub认证配置是否正确
- 检查仓库是否存在且有写入权限
- 检查网络连接

---

## 下一步

1. 修改 `/root/mysql_report/config.json`
2. 配置GitHub认证
3. 运行测试：`python3 /root/mysql_report/mysql_to_excel.py`
4. 如需定制Excel格式，请告知具体要求
