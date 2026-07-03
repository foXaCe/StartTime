# Troubleshooting

## The integration does not appear in the list

Clear your browser cache and reload, then try adding it again.

## The sensor state is unavailable

The value is captured once, when Home Assistant reports it has finished
initializing. Restart Home Assistant and check again after startup completes.

## Logs

Settings → System → Logs, then filter by `start_time`.

## Known limitations

- The value is captured once per startup and never changes until the next
  restart.
- Added on a running instance, the sensor shows the restored previous value
  (or stays unknown on the very first install) until the next restart.
- The capture relies on the `Home Assistant initialized in X.XXs` log record
  from `homeassistant.bootstrap`; there is no public API for this value. The
  test suite guards the message format on every supported release.
- Per-integration attributes are not recorded in history by design; they are
  available live and in the integration diagnostics.
