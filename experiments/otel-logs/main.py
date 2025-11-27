
from dataclasses import dataclass
import random
from typing import Any, List, Tuple

import requests
import datetime
import enum

class Severity (enum.Enum):
    TRACE = (4,  "Trace")
    DEBUG = (8,  "Debug")
    INFO  = (12, "Information")
    WARN  = (16, "Warning")
    ERROR = (20, "Error")
    FATAL = (24, "Fatal")

@dataclass
class LogRecord:
    timeUnix: datetime.datetime
    severity: Severity

    traceId: str | None
    spanId : str | None

    body : str

    attributes : List[Tuple[str, Any]]

SERVICE_NAME = "iris.experiments"
LIBRARY_NAME = "iris.experiments.logger"
LIBRARY_VERSION = "1.0.0"

OTEL_LOG_URL = "http://localhost:4318/v1/logs"

def make_resource_json ():
    return { "attributes": [ { "key": "service.name", "value": { "stringValue": SERVICE_NAME } } ] }
def make_scope_json ():
    return { "name": LIBRARY_NAME, "version": LIBRARY_VERSION }

def make_log_json (log_records):
    return {
        "resourceLogs": [
            {
                "resource": make_resource_json(),
                "scopeLogs": [
                    {
                        "scope": make_scope_json(),
                        "logRecords" : log_records
                    }
                ]
            }
        ]
    }

def make_attribute_json (attribute: Any):
    if isinstance(attribute, str):
        return { "stringValue": attribute }
    if isinstance(attribute, bool):
        return { "boolValue": attribute }
    if isinstance(attribute, int):
        return { "intValue": str(attribute) }
    if isinstance(attribute, float):
        return { "doubleValue": attribute }
    if isinstance(attribute, list):
        return { "arrayValue": { "values": list(map(make_attribute_json, attribute)) } }
    if isinstance(attribute, dict):
        res = []
        for key, val in attribute.items():
            res.append({ "key": key, "value": make_attribute_json(val) })
        return { "kvlistValue": { "values": res } }

    assert False, f"Attribute not implemented: {attribute}"
def make_attributes_json (attributes: List[Tuple[str, Any]]):
    res = []
    for key, val in attributes:
        res.append({ "key": key, "value": make_attribute_json(val) })
    return res

def make_record_json (record: LogRecord):
    unixTime = int(record.timeUnix.timestamp() * 1e9)

    print(record.timeUnix)
    
    result = {
        "timeUnixNano" : unixTime,
        "observedTimeUnixNano" : unixTime,

        "severityNumber": record.severity.value[0],
        "severityText": record.severity.value[1],

        "body": {
            "stringValue": record.body
        },

        "attributes": make_attributes_json(record.attributes)
    }

    if record.traceId is not None:
        result["traceId"] = record.traceId
    if record.spanId is not None:
        result["spanId"] = record.spanId
    
    return result

def log (record: LogRecord):
    content = make_record_json(record)

    total = make_log_json([ content ])

    print(total)

    response = requests.post(url = OTEL_LOG_URL, json = total)
    print(response.status_code, response.content)
log(LogRecord( datetime.datetime(2025, 10, 17, 0, 30, 12, random.randint(0, 1000)), Severity.FATAL,
    None, None, "A first fatal error",
    [ ("key1", "value"), ("key2", 1), ("key3", 1.23), ("key4", True), 
        ("key5", [ "val1", 1 ]), ("key6", { "a": 1, "b": "c" }) ] ))
for _ in range(100):
    log(LogRecord( datetime.datetime(2025, 10, 18, 0, 31, 12, _), Severity.FATAL,
        None, None, f"A {_} fatal error",
        [ ("key1", "value"), ("key2", 1), ("key3", 1.23), ("key4", True), 
            ("key5", [ "val1", 1 ]), ("key6", { "a": 1, "b": "c" }) ] ))
#for _ in range(100):
#    log(LogRecord( datetime.datetime(2025, 11, 16, 12, 32, 12, _), Severity.FATAL,
#                None, None, f"A {_} fatal error",
#                [ ("key1", "value"), ("key2", 1), ("key3", 1.23), ("key4", True), 
#                    ("key5", [ "val1", 1 ]), ("key6", { "a": 1, "b": "c" }) ] ))
# log(LogRecord( datetime.datetime.now(), Severity.ERROR, None, None, "An error", [] ))
# log(LogRecord( datetime.datetime.now(), Severity.FATAL, None, None, "A second fatal error", [] ))
# log(LogRecord( datetime.datetime.now(), Severity.FATAL, None, None, "A third fatal error", [] ))
