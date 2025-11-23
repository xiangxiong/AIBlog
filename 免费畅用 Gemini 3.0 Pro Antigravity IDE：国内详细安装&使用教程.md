# 免费畅用 Gemini 3.0 Pro Antigravity IDE：国内详细安装&使用教程
<img width="3542" height="2000" alt="image" src="https://github.com/user-attachments/assets/3cd24892-3ed6-43a6-8442-d11ee16fffb9" />


本文档旨在指导用户完成 Antigravity 的安装，并针对常见的登录和运行问题提供解决方案。

1. 安装步骤 (Installation)
* 获取安装包：请从官方渠道下载最新版本的 Antigravity 安装程序。
* 官网地址：https://antigravity.google/
* 运行安装：双击安装包，按照屏幕提示完成安装过程。
* 启动应用：安装完成后，从桌面或开始菜单启动 Antigravity。

2. 登录问题：目前已知的解决方案 (Login Issues: Known Solutions)
* 如果您无法登录 Antigravity，请按以下顺序尝试目前已知的解决方案：

## 方案一：排查账号权限 (Account Status)
* 问题描述：提示无权限、账号未激活或验证失败。
* 解决方案：Antigravity 目前处于早期测试阶段，仅对白名单用户开放。请首先确认您的 Google 账号是否已收到邀请或在授权列表中。


## 方案二：网络配置 + 全局代理 (Network Configuration) + Proxifier [本人遇到的是这种情况]
这是最常见的登录失败原因。Antigravity 的登录服务和部分组件流量可能无法被普通代理模式捕获。

* 操作步骤：
* 打开您的网络代理软件。
* 将代理模式设置为 全局模式 (Global Mode)。
* 下载Proxifier 并安装 https://www.proxifier.com/download/
* 
  <img width="2036" height="1396" alt="image" src="https://github.com/user-attachments/assets/d825a7d3-a2d0-4561-9809-3f20f4338616" />
  设置代理
  <img width="1070" height="1070" alt="image" src="https://github.com/user-attachments/assets/ab062494-f15e-4fe5-b9a9-94a7754f3929" />
  设置规则
  <img width="1800" height="1290" alt="image" src="https://github.com/user-attachments/assets/bfec29a9-d9bc-472d-8878-fd164a19ccf8" />

* 设置代码转发地址
重启 Antigravity 并尝试登录。


## 方案三：修改账号国家/地区 (Change Account Region)
如果以上方法均无效，可能是您的 Google 账号归属地受限。您可以尝试修改账号的国家/地区设置。

参考教程：如何修改谷歌账号的国家或地区
简要步骤：
确认当前地区：访问 https://policies.google.com/terms 查看账号当前归属地。
申请修改：访问 https://policies.google.com/country-association-form 提交修改申请。

注意：
每年仅允许修改一次。
申请理由建议填写：“因工作需要使用特定服务，请协助更改地区”。
需要配合对应地区的网络节点使用。
重启 Antigravity 并尝试登录。
