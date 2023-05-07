# 代码框架
## transfer_dog
transfer_dog 模块是程序的 GUI 框架，负责
1. 增删查改任务、显示任务运行状态
2. 根据任务的 schedule 定时调度任务

### 关于任务调度
1. 每隔 N 毫秒轮询所有任务
2. 如果需要执行任务，使用 `psutil.Popen()` 启动任务子进程
3. 如果检测到任务超时，则 `kill` 任务子进程
4. 如果 GUI 进程退出，任务子进程会自动检测到父进程已死并自动退出

## transfer_worker
transfer_worker 模块是底层的任务执行代码，可以独立于 GUI 运行。

### 执行逻辑
- Getter 对象负责过滤与下载源文件
- Putter 对象负责上传目标文件
- MiddleFile 对象负责保存临时文件的状态，包括临时文件本身，以及对应的源文件路径、目标文件路径
- middleware 负责对 MiddleFile 进行中间处理，并确定目标路径

> Getter 过滤 > middleware 预处理 > Getter 下载 > middleware 后处理 > Putter 上传

1. 启动时候先打开 getter 与 putter。并进行有效性检查，异常的直接报错退出。
2. getter.validate_src 验证源目录有效性
3. getter.next() 获取下一个待传输文件
   1. 遍历源目录
   2. 判断文件更新时间是否小于 interval
   3. 判断文件名是否匹配正则表达式
   4. 判断 (文件名, mtime) 是否已存在于 processed 数据库中
   5. 返回一个 mid_file = MiddleFile(源文件相对路径, 源文件修改时间)
4. middleware.pre_process() 进行预处理。<br>
   可以用来生成目标文件路径，或者修改 mid_file.abort 属性
5. getter.get() 下载该文件，生成 mid_file.middle 中间临时文件
6. middleware.process() 进行后处理。<br>
   可以用来生成目标文件路径，或者修改 mid_file.abort 属性
7. putter.put(mid_file) 将临时文件上传到目标路径。
8. 删除源文件以及清理临时文件


# todo
5. 小文件不落地，直接在内存里转发可以吗？
7. 普通 ftp server 对 LIST 命令的响应 与 IIS ftp server 对 LIST 命令的响应不一样！
   （可以在 iis - ftp目录浏览 - 目录列表样式 中将其修改为 unix 类型）
   累了，不想去支持 iis！就输出个告警！让用户自己改去！
   另外，iis 又不支持 mlsd()，干。
8. sftp 用 Paramiko 库


# Thanks to
1. [PySide6](https://pypi.org/project/PySide6/) for GUI
2. [SQLite](https://www.sqlite.org/index.html) for Database
3. [peewee](https://github.com/coleifer/peewee) for ORM
4. [remixicon](https://remixicon.com/) for Icon
4. [flaticon](https://www.flaticon.com/icon-fonts-most-downloaded/2?weight=bold&corner=rounded&type=uicon) for Icon
