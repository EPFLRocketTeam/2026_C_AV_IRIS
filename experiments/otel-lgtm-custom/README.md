
# otel-lgtm-custom

This experiment modifies the default configuration of grafana/otel-lgtm for us to be able to replicate really old historical data.

In particular, it modifies the Dockerfile to make the build time shorter, and adds configuration parameters for
- Loki to allow for historic data (block_builder and limits_config), current setup is for 1 month old data
- Tempo to allow for historic data, current setup is for 1 month old data
  - query_frontend.search.query_ingesters_until
  - storage.trace.wal.ingestion_time_range_slack
- OpenTelemetry Collector to remove the batch processor on logs
