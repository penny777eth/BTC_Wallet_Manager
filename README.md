# BTC 钱包管理工具

这个 BTC 钱包管理工具脚本帮助您管理多个 BTC 钱包，查询其余额和最近的交易时间。结果以格式化表格的形式显示。该脚本支持多个 API，以确保稳定性和可靠性。

由于本代码由 ChatGPT 撰写（连 README 基本也是），所以如有任何问题，建议直接问 ChatGPT，请勿询问上传者，谢谢配合！

## 功能

- 查询 BTC 钱包余额
- 查询最近的交易时间
- 支持多个 API 接口以减少速率限制问题
- 从 Excel 文件读取钱包详细信息
- 以格式化表格显示结果
- 显示 BTC 和 USDT 的总余额

## 需求

- Python
- 需要的 Python 包：`requests`、`pandas`、`tabulate`、`python-dateutil`、`openpyxl`

## 下载代码文件

### 1. 下载文件包
下载文件包到本地文件夹，或是 clone 也可以。


## 下载并安装 Python 环境（Windows）

### 1. 安装 Python
从 [Python 官网](https://www.python.org/downloads/) 下载适用于 Windows 的安装包并进行安装。

### 2. 安装 `pip`（如果未包含在安装中）
打开 PowerShell 或命令提示符 (Command Prompt)，输入以下命令以下载并安装 `pip`：
```powershell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### 3. 验证安装
在 PowerShell 或命令提示符中输入以下命令以验证安装：
```powershell
python --version
pip --version
```

## 准备你的 Excel 文件

打开 wallets.xlsx 文件，将 Example 钱包信息改为自己的钱包信息；可以无限添加钱包个数，但过多的钱包会导致 API 请求较慢或是挂掉，请自己酌情处理。

范例如下：

| Address                                            | Label          | Browser  | Type         |
|----------------------------------------------------|----------------|----------|--------------|
| bc1q20w8qxtvcn7qsv7pn9l9cafmptrasdcmx6m727ajztmm9pzmhh2sa5ktxf | Example           | Chrome   | UniSat     |

## 运行程序

确保您的 Excel 文件 wallets.xlsx 与脚本在同一目录中。然后运行脚本：

```sh
python btc_wallet_check.py
```
