import datetime as dt
import json
import logging

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class MyJSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
        exclude_keys: list[str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}
        self.exclude_keys = set(
            exclude_keys) if exclude_keys is not None else set()

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "@timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["error"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["log.origin.stack"] = self.formatStack(
                record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        
        if hasattr(record, 'user_id'):
            message['user'] = {
                'id': record.user_id
            }
        
        message.update(
            {key: val for key, val in always_fields.items()}
        )

        # Remove keys specified in exclude_keys
        for key in self.exclude_keys:
            message.pop(key, None)

        # Use list() to avoid modifying the dict during iteration
        for key in list(message.keys()):
            if key in self.exclude_keys:
                del message[key]

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS and key not in self.exclude_keys:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO
