
import datetime
import json
import random

for id in range(200):
  time = datetime.datetime.now() - datetime.timedelta(10, 200 * 60 - id * 60)
  unix = int(time.timestamp() * 1e9)

  payload = json.loads("""
  {
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
                  {
                    "asDouble": %(value),
                    "timeUnixNano": "%(time)",
                    "attributes": [
                      {
                        "key": "my.gauge.attr",
                        "value": {
                          "stringValue": "some value"
                        }
                      }
                    ]
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
  }""".replace("%(time)", str(unix)).replace("%(value)", str(random.randint(0, 20))))

  import requests

  OTEL_METRICS_URL = "http://localhost:4318/v1/metrics"

  response = requests.post(url = OTEL_METRICS_URL, json = payload)
  print(response.status_code, response.content)