import os
import subprocess
from threading import Thread

from loguru import logger


def stream_reader(pipe, log_function):
    with pipe:
        for line in iter(pipe.readline, ''):
            if line:
                print(line, end='')
                log_function(line.strip())
            else:
                break
    logger.info("Stream reader completed.")


def my_job(task_file, python_path, job_id, env_variable):
    log_name = 'logs/log_{}/{}.log'.format(job_id, job_id)
    logger.remove()
    logger.add(log_name, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", rotation="00:00",
               retention="30 days", encoding='utf-8')

    env = os.environ.copy()
    env['PYTHONPATH'] = env_variable

    process = subprocess.Popen(
        [python_path, task_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding='utf-8',
        env=env
    )

    stdout_thread = Thread(target=stream_reader, args=(process.stdout, logger.info))
    stderr_thread = Thread(target=stream_reader, args=(process.stderr, logger.error))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    return_code = process.wait()

    if return_code != 0:
        logger.error(f"Script exited with return code {return_code}")

    process.stdout.close()
    process.stderr.close()

    logger.info("Process completed and streams closed.")
