#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/05 14:46:48

import logging

from transfer_worker.worker.middle_file import Abort, MiddleFile

DESCRIPTION = """中间件示例
你可以通过自己编写的中间件脚本来修改 TransferWorker 的传输逻辑。

有效的中间件应该可选地包含两个函数: pre_process(mid_file, arg) 与 process(mid_file, arg).

你可以在中间件函数中决定目标文件的文件路径，决定是否中止传输，甚至通过 mid_file.middle 修改上传的文件内容。

参数 mid_file 代表处于 下载 >> 上传 中间状态的临时文件。TransferWorker 从源地址下载源文件，形成 mid_file, 然后将 mid_file 上传到目标地址。
    MiddleFile {
        source:         源文件的相对路径, Path 类型
        source_mtime:   源文件的文件修改时间, str 类型
        middle:         临时文件, Path 类型或者字节流类型
        dest:           目标文件的相对路径, Path 类型
        abort:          是否中止后续操作, middle_file.Abort 枚举。包括 Abort.ABORT, Abort.NO_ABORT, Abort.ABORT_AND_RECORD。
                        三个枚举值分别表示 中止、不中止、中止并记录为已处理。默认为 NO_ABORT。
    }

参数 arg 是由任务配置中的 task.middleware_arg 字段传递的。两个函数共享该字段，由你自己决定如何划分该参数。
    比如你可以决定 arg.split(',')[0] 给 pre_process 用， arg.split(',')[1] 给 process() 用。

"""

def pre_process(mid_file: MiddleFile, arg: str) -> None:
    """TransferWorker 在过滤出待处理的源文件之后，准备下载该源文件之前，会尝试调用中间件的 pre_process() 函数。

    此时的 mid_file 只有 {source, source_mtime, abort} 属性
    
    你可以在 pre_process() 中设置 mid_file 的 dest 与 abort 属性

    Args:
        mid_file (MiddleFile): _description_
        arg (str): _description_
    """
    logger = logging.getLogger(__name__)
    logger.debug('Just do nothing.')
    pass

def process(mid_file: MiddleFile, arg: str) -> None:
    """TransferWorker 在下载完源文件，生成 mid_file.middle 之后，准备上传该 mid_file 之前，会尝试调用中间件的 process() 函数。
    
    此时的 mid_file 只有 {source, source_mtime, middle, abort 属性}

    你可以在 process() 中设置 mid_file 的 dest 与 abort 属性。甚至修改 mid_file.middle 临时文件的内容。

    Args:
        mid_file (MiddleFile): _description_
        arg (str): _description_
    """
    logger = logging.getLogger(__name__)
    logger.debug('Just do nothing.')
    pass