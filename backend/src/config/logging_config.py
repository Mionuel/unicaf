import logging
import sys
import structlog # Structlog for logs in JSON format

def ignore_empty_values(logger, method_name, event_dict):
    filtered_dict = {}
    
    for key, value in event_dict.items():
        if value is not None: # only keep the values that are not None
            filtered_dict[key] = value
            
    return filtered_dict

# Pretty much the default except for the switching between json and human-readable formats
def setup_logging(json_logs: bool = False, level: int = logging.INFO) -> None:
    logging.basicConfig(stream=sys.stdout, level=level, format="%(message)s")

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        # automatically adds the module and function name in which a log was generated
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            }
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        ignore_empty_values
    ]

    # switches between printing in JSON format and formatted lines for easiear readability
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
