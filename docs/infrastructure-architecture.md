# Infrastructure Architecture

The infrastructure is hosted using [Amazon Web Services](https://aws.amazon.com/) (AWS) and their various cloud computing services.

## Data Pipeline Infrastructure

### Invoking Lambda Functions

The payload for invoking the private lambda function contains a parameter specifying the format to extract information from.

```
{"format": "gen8vgc2022"}
```

The lambda function is scheduled with a cron job trigger using AWS EventBridge. The cron expression used is `0 9 * * ? *`, meaning it will trigger at 09:00:00 GMT everyday.
