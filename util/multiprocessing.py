def exception_handle_task(task):
    def new_task(*args, **kwargs):
        try:
            result = task(*args, **kwargs)
            return TaskResult(result=result)
        except Exception as e:
            return TaskResult(exception=e)

    return new_task


class TaskResult:
    def __init__(self, result=None, exception=None):
        self._result = result
        self._exception = exception

    def get_or_die(self):
        if self._exception is None:
            return self._result
        else:
            print(self._exception)
            raise self._exception
