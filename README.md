# todo
1. 任务列表用 qscrollarea 应该就行
2. subprocess job 可以使用 python 自带的 subprocess 模块来做， subprocess.Popen() 会新建进程，并且是异步的，但是主进程死亡不会杀死子进程
   据说可以使用 atexit 库来实现父进程退出时候的清理(no! 这个只能处理正常退出的情况，异常退出时候不会被调用!)
   那有一个办法就是在子程序中开一个线程，判断父进程是否还在，发现父进程挂了就自杀？
3. filters > get_files > middleware > put_files
4. schedule 怎么做？
   可以使用 APScheduler 库，这个库有点庞大了，但是好在支持直接从 crontab 表达式来调度作业。
   `sched.add_job(job_function, CronTrigger.from_crontab('0 0 1-15 may-aug *'))`
   或者使用 python 自带的 sched，每分钟运行一次，然后调用第三方库（比如 croniter，croniter.match() 只支持到分钟级）解析每个作业的 cron-expression，在这个时间的，就调 subprocess 执行。
5. 小文件不落地，直接在内存里转发可以吗？
6. 除了发送文件的超时，要不要加个作业超时，超过多久就删掉子进程？
7. 普通 ftp server 对 LIST 命令的响应 与 IIS ftp server 对 LIST 命令的响应不一样！
   （可以在 iis - ftp目录浏览 - 目录列表样式 中将其修改为 unix 类型）
   累了，不想去支持 iis！就输出个告警！让用户自己改去！
   另外，iis 又不支持 mlsd()，干。
8. sftp 用 Paramiko 库



# Thanks to
1. [PyQt](https://www.riverbankcomputing.com/software/pyqt/)
2. [SQLite](https://www.sqlite.org/index.html)
3. [peewee](https://github.com/coleifer/peewee)
4. [flaticon](https://www.flaticon.com/icon-fonts-most-downloaded/2?weight=bold&corner=rounded&type=uicon)
