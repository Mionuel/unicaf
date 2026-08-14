import logging
import sys
import structlog

# Structlog for logs in JSON format
def setup_logging(json_logs: bool = False, level: int = logging.INFO) -> None:
    logging.basicConfig(stream=sys.stdout, level=level, format="%(message)s")

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    # Pretty much the default except for this part
    # switches between printing in more readable format and in JSON via the json_logs flag
    renderer = (
        structlog.processors.JSONRenderer()
        if json_logs
        else structlog.dev.ConsoleRenderer()  
    )

    structlog.configure(
        processors=processors + [renderer],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
