from functools import wraps


def exception_handle_task(task):
    @wraps(task)
    def new_task(*args, **kwargs):
        try:
            result = task(*args, **kwargs)
            return TaskResult(result=result)
        except Exception as e:
            return TaskResult(exception_message=str(e))

    return new_task


class ExecutionTaskException(Exception):
    def __init__(self, message):
        super(ExecutionTaskException, self).__init__(message)


class TaskResult:
    def __init__(self, result=None, exception_message=None):
        self._result = result
        if exception_message is not None:
            self._exception = ExecutionTaskException(exception_message)
        else:
            self._exception = None

    def get_or_die(self):
        if self._exception is None:
            return self._result
        else:
            raise self._exception
