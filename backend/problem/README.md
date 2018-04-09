## Problem App 架构设计

### Models层:
+ problemId: 题目编号,主键
+ title: 题目标题
+ content: 题面内容
+ standardInput: 题目输入
+ standardOutput: 题目输出
+ constraints: 输入限制
+ sampleInput: 样例输入
+ sampleOutput: 样例输出
+ sampleExplanation: 样例解释
+ resource: 题目来源
+ timeLimit: 时间限制,默认为2s
+ memoryLimit: 内存限制,默认为128mb
+ solvedNumber: 解决这个题目的人数
+ tryNumber: 尝试这个题目的人数
+ specialJudge: 题目是否需要Checker
+ visible: 题目是否可见
