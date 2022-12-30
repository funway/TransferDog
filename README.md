# todo
1. 任务列表用 qscrollarea 应该就行
2. subprocess job 可以使用 python 自带的 subprocess 模块来做， subprocess.Popen() 会新建进程，并且是异步的，而且主进程死亡不会杀死子进程
   据说可以使用 atexit 库来实现父进程退出时候的清理(no! 这个只能处理正常退出的情况，异常退出时候不会被调用!)
   那有一个办法就是在子程序中开一个线程，判断父进程是否还在，发现父进程挂了就自杀？