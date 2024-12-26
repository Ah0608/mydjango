# import os
# import subprocess
# import sys
# from threading import Thread
# from loguru import logger
#
#
# def stream_reader(pipe, log_function):
#     with pipe:
#         for line in iter(pipe.readline, ''):
#             if line:
#                 log_function(line.strip())
#             else:
#                 break
#     log_function("Stream reader completed.")
#
#
# def create_logger(job_id):
#     log_name = f'logs/log_{job_id}/{job_id}.log'
#     logger.remove()  # 移除默认的 logger 配置
#     logger_instance = logger.bind(job_id=job_id)  # 创建一个绑定了 job_id 的 logger 实例
#     logger_instance.add(
#         log_name,
#         format="{time:YYYY-MM-DD HH:mm:ss}-{extra[job_id]}-{level}-{message}",
#         filter=lambda record: record["extra"].get("job_id") == job_id,
#         rotation="00:00",
#         retention="30 days",
#         encoding='utf-8',
#         enqueue=True  # 使用 enqueue=True 确保线程安全
#     )
#     logger_instance.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss}-{extra[job_id]}-{level}-{message}")
#     return logger_instance
#
#
# def my_job(task_file, python_path, job_id, env_variable):
#     log = create_logger(job_id)  # 创建独立的 logger 实例
#
#     env = os.environ.copy()
#     env['PYTHONPATH'] = env_variable
#
#     process = subprocess.Popen(
#         [python_path, '-u', task_file],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,
#         bufsize=1,
#         encoding='utf-8',
#         env=env
#     )
#
#     stdout_thread = Thread(target=stream_reader, args=(process.stdout, log.info))
#     stderr_thread = Thread(target=stream_reader, args=(process.stderr, log.error))
#
#     stdout_thread.start()
#     stderr_thread.start()
#
#     stdout_thread.join()
#     stderr_thread.join()
#
#     return_code = process.wait()
#
#     if return_code != 0:
#         log.error(f"Script exited with return code {return_code}")
#
#     process.stdout.close()
#     process.stderr.close()
#
#     log.info("Process completed and streams closed.")

# import os
# import subprocess
# import sys
# import threading
# from loguru import logger
#
#
# class CMDProcess(threading.Thread):
#
#     def __init__(self, cmd, logger_instance,env_variable):
#         threading.Thread.__init__(self)
#         self.cmd = cmd
#         self.logger = logger_instance
#         self.env_variable = env_variable
#
#     def run(self):
#         env = os.environ.copy()
#         env['PYTHONPATH'] = self.env_variable
#         self.proc = subprocess.Popen(
#             self.cmd,
#             bufsize=0,
#             shell=False,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             encoding='utf-8',
#             env=env
#         )
#
#         for line in self.proc.stdout:
#             if line:
#                 self.logger.info(line.strip())
#
#         for line in self.proc.stderr:
#             if line:
#                 self.logger.error(line.strip())
#
#
# def my_job(task_file, python_path='python', job_id=None, env_variable=''):
#     log_name = f'logs/log_{job_id}/{job_id}.log'
#
#     logger.remove()  # 移除默认的 logger 配置
#     logger_instance = logger.bind(job_id=job_id)
#     logger_instance.add(log_name, format="{time:YYYY-MM-DD HH:mm:ss}-{extra[job_id]}-{level}-{message}",
#                         filter=lambda record: record["extra"].get("job_id") == job_id,
#                         rotation="00:00",
#                         retention="30 days", encoding='utf-8', enqueue=True)
#     logger_instance.add(sys.stdout,format="{time:YYYY-MM-DD HH:mm:ss}-{extra[job_id]}-{level}-{message}")
#
#     cmd = [
#         python_path,
#         '-u',
#         task_file
#     ]
#
#     testProcess = CMDProcess(cmd, logger_instance,env_variable)
#     testProcess.start()


import os
import subprocess
import asyncio

from loguru import logger


class CMDProcess:
    def __init__(self, cmd, logger_instance, env_variable):
        self.cmd = cmd
        self.logger = logger_instance
        self.env_variable = env_variable

    async def run(self):
        env = os.environ.copy()
        env['PYTHONPATH'] = self.env_variable

        process = await asyncio.create_subprocess_exec(
            *self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )

        async def read_stream(stream, log_method):
            while True:
                line = await stream.readline()
                if not line:
                    break
                log_method(line.decode().strip())

        await asyncio.gather(
            read_stream(process.stdout, self.logger.info),
            read_stream(process.stderr, self.logger.error)
        )

        await process.wait()


# 全局字典存储已创建的日志实例
job_loggers = {}


def get_logger(job_id):
    global job_loggers
    if job_id not in job_loggers:
        log_name = f'logs/log_{job_id}/{job_id}.log'
        logger_instance = logger.bind(job_id=job_id)
        logger_instance.add(log_name, format="{time:YYYY-MM-DD HH:mm:ss}-{extra[job_id]}-{level}-{message}",
                            filter=lambda record: record["extra"].get("job_id") == job_id,
                            rotation="00:00",
                            retention="30 days", encoding='utf-8', enqueue=True)
        job_loggers[job_id] = logger_instance
    return job_loggers[job_id]


# 定义 my_job 函数
async def my_job(task_file, python_path='python', job_id=None, env_variable=''):
    logger_instance = get_logger(job_id)

    cmd = [
        python_path,
        '-u',
        task_file
    ]

    test_process = CMDProcess(cmd, logger_instance, env_variable)
    await test_process.run()


def wrapper_my_job(*args, **kwargs):
    asyncio.run(my_job(*args, **kwargs))
