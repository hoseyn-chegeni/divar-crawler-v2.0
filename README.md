# divar-crawler-v2.0
## ساختار پروژه
پروژه از دو بخش سرور جاب ها و کرالر تشکیل شده است \
کرالر به صورت منظم  وضغیت خود را به سرور جاب اطلاع میدهد  و اگر وضعیت کرالر  free  باشد درخواست دریافت جاب به سرور جاب ها ارسال می نماید \
سرور جاب ها متشکل از صف درخواست ها و داده های کرال شده می باشد  \
سرور کرالر علاوه بر وضعیت کرالر وضعیت جاب را نیز برمیگرداند \
برای فیلد شهر ها از  enum  استفاده شد  دلیل استفاده از دیکشنری در تغییرات قبلی امکان وارد کردن شهر در پارامتر ها به زبان فارسی بوده تا مشکل  misspell  برطرف شود 


## متد های موجود در سرور جاب ها 
| Endpoint         | Method | Description                                       |
|-------------------|--------|---------------------------------------------------|
| /crawler/status   | GET    | مشاهده وضعیت کرالر        |
| /crawler/status   | POST   | اپدیت وضعیت کرالر     .                 |
| /jobs             | GET    | مشاهده تمام جاب های ارسال شده.                          |
| /jobs             | POST   | ایجاد جاب جدید.                                 |
| /save-job         | POST   | ارسال جاب به صف .                 |
| /send-job         | GET    | واکشی اولین جاب از صف برای ارسال به کرالر. |
| /save-posts         | POST    | برای دریافت داده های کرال شده از کرالر. |
|  /posts/       | GET    | مشاهده سرچ و فیلتر تمام داده های کرال شده. |
| /queue_instances         | GET    | مشاهده جاب های موجود در صف. |
| status/{job_id}         | GET    | مشاهده وضعیت جاب. |
| //update-job-status/{job_id}        | PUT    | برای اپدیت وضعیت جاب توسط کرالر. |


## متد های موجود در سرویس کرالر 

| Endpoint         | Method | Description                                       |
|-------------------|--------|---------------------------------------------------|
| /fetch-data   | POST    |   کرالر        |
| /status   | GET   | دریافت وضعیت کرالر برای ارسال به سرور جاب ها|


## جداول دیتابس اصلی 
### جدول جاب ها 

| FIELDS          | Description                                       |
|------------------------|---------------------------------------------------|
| id       ||
| city_ids      ||
| category      ||
| query      |برای بخش سرچ سایت دیوار |
| num_posts      |تعداد آگهی ها|
| status      ||




### جدول  آگهی ها

| FIELDS          | Description                                       |
|------------------------|---------------------------------------------------|
| id       ||
| title      ||
| token      ||
| city      ||
| district      |منطقه|
| url      |آدرس صفحه جزییات آگهی|










