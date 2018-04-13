## Problem App 架构设计

### Models层:
+ problem_id: 题目编号,主键
+ title: 题目标题
+ content: 题面内容
+ standard_input: 题目输入
+ standard_output: 题目输出
+ constraints: 输入限制
+ sample_input: 样例输入
+ sample_output: 样例输出
+ sample_explanation: 样例解释
+ resource: 题目来源
+ time_limit: 时间限制,默认为2s
+ memory_limit: 内存限制,默认为128mb
+ solved_number: 解决这个题目的人数
+ try_number: 尝试这个题目的人数
+ special_judge: 题目是否需要Checker
+ visible: 题目是否可见
