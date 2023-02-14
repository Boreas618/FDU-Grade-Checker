# FDU_grade_checker

本项目受[pafd-automated](https://github.com/FDUCSLG/pafd-automated)启发。

This project is inspired by [pafd-automated](https://github.com/FDUCSLG/pafd-automated)启发。

每隔5分钟自动查询你的期末成绩，如有新的一门课程出分，则通过微信推送通知。

This Python script queries your final grades every 5 minutes. Once the grade of a new course is released, a notification will be pushed to your WeChat.

# 使用方法 Getting started

1. 注册[推送加](http://www.pushplus.plus)，获取自己的token 

Sign up for [pushplus](http://www.pushplus.plus) and get your own token

<img width="295" alt="Screenshot 2023-01-05 at 6 22 31 AM" src="https://user-images.githubusercontent.com/98612013/210661348-2783bb0f-f6dd-4099-b5b4-ee00cdcb7a92.png">

2. 注册Github账号，Fork此仓库

Sign up for Github and fork this repository

> 注意：请务必确认record.json的初始内容为{}，否则请修改其内容为{}
> 
> Notice: make sure that the initial content of record.json is {}. Otherwise you need to alter its content with {}
>
> <img width="90" alt="Screenshot 2023-01-05 at 11 44 45 PM" src="https://user-images.githubusercontent.com/98612013/210821671-d4b40c5b-e629-4501-8fd5-cb1684ac04db.png">

3. 然后在你 Fork 的副本中，依次点击 Settings, Secrets , Actions 和 New repository secret

In your repository, click on the button Settings, Secrets , Actions and New repository secret consecutively

4. 新建如下Secrets，其中STD_ID为你的学号，PASSWORD为你的密码，TOKEN为第一步获取的token

Create the secrets below: STD_ID is your student id. TOKEN is the token you got in the first step.

<img width="787" alt="Screenshot 2023-01-05 at 6 24 01 AM" src="https://user-images.githubusercontent.com/98612013/210661446-d0ff335c-6f54-4dcc-8ae8-83eae1c83279.png">

通过 GitHub Action, 该脚本将每隔5分钟查询一次你的期末成绩，并在有新一门课程出分时通过微信提醒你。

Through GitHub Action, the script queries your final grades every 5 minutes.

5. 建议[关闭Action的邮件通知](https://github.com/settings/notifications)，否则你每天会收到数百封Github的邮件🤡

I advise anyone who has gone though the steps above to turn off the [Email notification of Action](https://github.com/settings/notifications). Otherwise, your mailbox will be filled with hundreds of emails everyday.

<img width="809" alt="Screenshot 2023-01-05 at 6 45 51 AM" src="https://user-images.githubusercontent.com/98612013/210664207-2e6aa917-eecf-44c7-b3d7-1f3919f7e77b.png">
