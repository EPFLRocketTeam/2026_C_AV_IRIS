
import datetime
import enum
import random
from typing import Any, List, Tuple

import requests

def render_attribute (attribute: Any):
    if isinstance(attribute, str):
        return { "stringValue": attribute }
    if isinstance(attribute, bool):
        return { "boolValue": attribute }
    if isinstance(attribute, int):
        return { "intValue": str(attribute) }
    if isinstance(attribute, float):
        return { "doubleValue": attribute }
    if isinstance(attribute, list):
        return { "arrayValue": { "values": list(map(render_attribute, attribute)) } }
    if isinstance(attribute, dict):
        res = []
        for key, val in attribute.items():
            res.append({ "key": key, "value": render_attribute(val) })
        return { "kvlistValue": { "values": res } }

    assert False, f"Attribute not implemented: {attribute}"
def render_kv_attributes (attributes: List[Tuple[str, Any]]):
    res = []
    for key, val in attributes:
        res.append({ "key": key, "value": render_attribute(val) })
    return res

class SpanKind (enum.Enum):
    UNSPECIFIED = 0
    INTERNAL = 1
    SERVER = 2
    CLIENT = 3
    PRODUCER = 4
    CONSUMER = 5

class Event:
    name: str

    timeUnix: datetime.datetime

    attributes: List[Tuple[str, Any]]

    def __init__ (self, name: str, time: datetime.datetime):
        self.name = name
        self.timeUnix = time
        self.attributes = []

    def render_json (self):
        return {
            "name": self.name,
            "timeUnixNano": int(1e9 * self.timeUnix.timestamp()),
            "attributes": render_kv_attributes(self.attributes)
        }

class StatusCode(enum.Enum):
    UNSET = 0
    OK = 1
    ERROR = 2

class Status:
    message: str
    status_code: StatusCode

    def __init__ (self, message: str, status_code: StatusCode):
        self.message = message
        self.status_code = status_code

    def render_json (self):
        return {
            "message": self.message,
            "code": self.status_code.value
        }

class Span:
    spanId: str
    parent: "Span | None"

    childs: "List[Span]"

    name: str

    startTimeUnix: datetime.datetime
    endTimeUnix:   datetime.datetime

    attributes: List[Tuple[str, Any]]

    kind: SpanKind

    events: List[Event]
    status: Status

    @staticmethod
    def root (
            name: str,
            start: datetime.datetime,
            end: datetime.datetime,
            status: Status
        ):
        return Span(None, name, start, end, status)
    def subspan (
            self,
            name: str,
            start: datetime.datetime,
            end: datetime.datetime,
            status: Status
        ):
        return Span(self, name, start, end, status)

    def __init__ (
            self,
            parent: "Span | None",
            name: str,
            start: datetime.datetime,
            end: datetime.datetime,
            status: Status
        ):
        self.parent = parent
        self.name = name
        self.startTimeUnix = start
        self.endTimeUnix = end
        self.status = status
        self.spanId = "".join( [ random.choice("ABCDEF0123456789") for _ in range(16) ] )
        self.attributes = []
        self.events = []
        self.childs = []
        self.kind = SpanKind.SERVER

        if self.parent is not None:
            self.parent.childs.append(self)
    def with_attribute (self, key: str, val: Any):
        self.attributes.append((key, val))
        return self
    def with_event (self, event: Event):
        self.events.append(event)
        return self

    def render_json (self, traceId: str):
        payload = {
            "traceId": traceId,
            "spanId": self.spanId,
            "parentSpanId": "",
            "name": self.name,
            "kind": self.kind.value,
            "startTimeUnixNano": int(1e9 * self.startTimeUnix.timestamp()),
            "endTimeUnixNano": int(1e9 * self.endTimeUnix.timestamp()),
            "attributes": render_kv_attributes(self.attributes),
            "events": list(map(lambda event: event.render_json(), self.events)),
            "status": self.status.render_json()
        }

        if self.parent is not None:
            payload["parentSpanId"] = self.parent.spanId
        
        return payload

class Trace:
    traceId: str
    root: Span

    def __init__ (self, root: Span):
        self.traceId = "".join( [ random.choice("ABCDEF0123456789") for _ in range(32) ] )
        self.root = root
    
    def render_json (self):
        total = []

        def dfs (span: Span):
            total.append(span.render_json(self.traceId))
            for child in span.childs:
                dfs(child)
        
        dfs(self.root)

        return total

SERVICE_NAME = "iris.experiments"
LIBRARY_NAME = "iris.experiments.logger"
LIBRARY_VERSION = "1.0.0"

OTEL_TRACE_URL = "http://localhost:4318/v1/traces"

def make_resource_json ():
    return { "attributes": [ { "key": "service.name", "value": { "stringValue": SERVICE_NAME } } ] }
def make_scope_json ():
    return { "name": LIBRARY_NAME, "version": LIBRARY_VERSION }

def make_trace_json (trace: Trace):
    return {
        "resourceSpans": [
            {
                "resource": make_resource_json(),
                "scopeSpans": [
                    {
                        "scope": make_scope_json(),
                        "spans" : trace.render_json()
                    }
                ]
            }
        ]
    }


def trace (span: Span):
    total = make_trace_json(Trace(span))

    print(total)

    response = requests.post(url = OTEL_TRACE_URL, json = total)
    print(response.status_code, response.content)

def day_at (seconds: int):
    now = datetime.datetime.now() - datetime.timedelta(30, 0)
    return datetime.datetime( 
        now.year, now.month, now.day, now.hour, now.minute, seconds )

for _ in range(100):
    root = Span.root( "Some span", day_at(0), day_at(30), Status( "All good", StatusCode.OK ) )
    root.with_event( Event( "Some event", day_at(10) ) )

    sub = root.subspan( "Some subspan", day_at(15), day_at(25), Status( "Error parsing", StatusCode.ERROR) )

    trace(root)
