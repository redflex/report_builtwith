# report_builtwith
Human-friendly report from builtwith json

## What it does

This container accepts a `result` object in base64-encoded json via the `SCAN`
environment variable, and returns a base64-encoded markdown or csv report,
depending on the `OUTPUT_FORMAT` environment variable.


## Building

`docker build -t report_builtwith .`

## Running

Run the `report_builtwith` container with the following environment variables:

| Variable         | Purpose                                               |
|------------------|-------------------------------------------------------|
| `SCAN`           | Base64-encoded json of one builtwith `result` object. |
| `OUTPUT_FORMAT`  | CSV or MD                                             |

Example (markdown output):
```
docker run \
  -it \
  --rm \
  -e SCAN=$SCAN \
  -e FORMAT=MD \
  --read-only \
  report_builtwith:latest | base64 -d > ./output.md
```
