
import datetime
import json
import random

payload = json.loads("""{
  "resourceMetrics": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": {
              "stringValue": "my.service"
            }
          }
        ]
      },
      "scopeMetrics": [
        {
          "scope": {
            "name": "my.library",
            "version": "1.0.0",
            "attributes": [
              {
                "key": "my.scope.attribute",
                "value": {
                  "stringValue": "some scope attribute"
                }
              }
            ]
          },
          "metrics": [
            {
              "name": "my.gauge2",
              "unit": "1",
              "description": "I am a Gauge",
              "gauge": {
                "dataPoints": [
                  
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}""")

base = datetime.datetime.now()
for id in range(1000):
  time = base - datetime.timedelta(3, 0, 0, 99990 - 10 * id) + datetime.timedelta(0, 30)
  unix = int(time.timestamp() * 1e9)
  print(time)

  payload["resourceMetrics"][0]["scopeMetrics"][0]["metrics"][0]["gauge"]["dataPoints"].append(
    {
      "asDouble": str(random.randint(0, 20)),
      "timeUnixNano": str(unix),
      "attributes": [
        {
          "key": "my.gauge.attr",
          "value": {
            "stringValue": "some value"
          }
        }
      ]
    }
  )


import requests

OTEL_METRICS_URL = "http://localhost:4318/v1/metrics"

response = requests.post(url = OTEL_METRICS_URL, json = payload)
print(response.status_code, response.content)