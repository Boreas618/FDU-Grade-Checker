# FDU_grade_checker

This project is inspired by [pafd-automated](https://github.com/FDUCSLG/pafd-automated).

This Python script queries your final grades every 5 minutes. Once the grade of a new course is released, a notification will be pushed to your WeChat.

# Getting started

1. Sign up for [pushplus](http://www.pushplus.plus) and get your own token

<img width="295" alt="Screenshot 2023-01-05 at 6 22 31 AM" src="https://user-images.githubusercontent.com/98612013/210661348-2783bb0f-f6dd-4099-b5b4-ee00cdcb7a92.png">

2. Sign up for Github and fork this repository

> Notice: make sure that the initial content of record.json is {}. Otherwise you need to alter its content with {}
>
> <img width="90" alt="Screenshot 2023-01-05 at 11 44 45 PM" src="https://user-images.githubusercontent.com/98612013/210821671-d4b40c5b-e629-4501-8fd5-cb1684ac04db.png">

3. In your repository, click on the button Settings, Secrets , Actions and New repository secret consecutively

4. Create the secrets below: STD_ID is your student id. TOKEN is the token you got in the first step.

<img width="787" alt="Screenshot 2023-01-05 at 6 24 01 AM" src="https://user-images.githubusercontent.com/98612013/210661446-d0ff335c-6f54-4dcc-8ae8-83eae1c83279.png">

Through GitHub Action, the script queries your final grades every 5 minutes.

5. I advise anyone who has gone though the steps above to turn off the [Email notification of Action](https://github.com/settings/notifications). Otherwise, your mailbox will be filled with hundreds of emails everyday.

<img width="809" alt="Screenshot 2023-01-05 at 6 45 51 AM" src="https://user-images.githubusercontent.com/98612013/210664207-2e6aa917-eecf-44c7-b3d7-1f3919f7e77b.png">
