# FDU_grade_checker

本项目受[pafd-automated](https://github.com/FDUCSLG/pafd-automated)启发

每隔15分钟自动查询你的期末成绩，如有新的一门课程出分，则通过微信推送通知。

# 使用方法

1. 注册[推送加](http://www.pushplus.plus)，获取自己的token

<img width="295" alt="Screenshot 2023-01-05 at 6 22 31 AM" src="https://user-images.githubusercontent.com/98612013/210661348-2783bb0f-f6dd-4099-b5b4-ee00cdcb7a92.png">



2. 注册Github账号，Fork此仓库

3. 然后在你 Fork 的副本中，依次点击 Settings, Secrets , Actions 和 New repository secret

4. 新建如下Secrets，其中STD_ID为你的学号，PASSWORD为你的密码，TOKEN为第一步获取的token

<img width="787" alt="Screenshot 2023-01-05 at 6 24 01 AM" src="https://user-images.githubusercontent.com/98612013/210661446-d0ff335c-6f54-4dcc-8ae8-83eae1c83279.png">

通过 GitHub Action, 该脚本将每隔15分钟查询一次你的期末成绩，并在有新一门课程出分时通过微信提醒你。

