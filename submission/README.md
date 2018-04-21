## Submission App 架构设计

### Model层设计:
+ submission_id: 主键,每个提交的唯一id.
+ language: 提交所用的语言.
+ judge_status: 存储`Osiris-Judge-Core`的判断结果.
+ code: 存储提交的代码.

### View层设计:
+ 接受`Judge`请求并返回相应的`submission_id`.