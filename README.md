# FDU-Grade-Checker

该脚本借助Github Action，每隔一段时间向复旦大学教务服务系统请求GPA数据，与仓库中加密存储的历史信息比对，当GPA数据发生变动时可通过微信通知指定用户。

## 使用方法

1. 注册[推送加](http://www.pushplus.plus)，获取自己的token (token同时会作为加密算法秘钥，若不希望暴露自己的排名，请妥善保管)

<center><img width="295" alt="Screenshot 2023-01-05 at 6 22 31 AM" src="https://user-images.githubusercontent.com/98612013/210661348-2783bb0f-f6dd-4099-b5b4-ee00cdcb7a92.png"></center>

2. 注册Github账号，Fork此仓库

3. 在你 Fork 的副本中，依次点击 Settings, Secrets, Actions 和 New repository secret

4. 新建如下Secrets，其中STD_ID为你的学号，PASSWORD为你的密码，TOKEN为第一步获取的token

<center><img width="787" alt="Screenshot 2023-01-05 at 6 24 01 AM" src="https://user-images.githubusercontent.com/98612013/210661446-d0ff335c-6f54-4dcc-8ae8-83eae1c83279.png"></center>

5. 建议[关闭Action的邮件通知](https://github.com/settings/notifications)，以防通知Action执行结果的邮件过多。
