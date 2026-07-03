# Troubleshooting

## The integration does not appear in the list

Clear your browser cache and reload, then try adding it again.

## The sensor state is unavailable

The value is captured once, when Home Assistant reports it has finished
initializing. Restart Home Assistant and check again after startup completes.

## Logs

Settings → System → Logs, then filter by `start_time`.
