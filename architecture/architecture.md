# WorkSpot Feedback API — Architecture

WorkSpot Feedback API is a serverless REST API built on AWS.

## Architecture Diagram

```mermaid
flowchart TD
    Client["Client<br/>curl"]

    APIGW["Amazon API Gateway<br/>HTTP API"]

    Create["AWS Lambda<br/>create-feedback"]
    Get["AWS Lambda<br/>get-feedback"]
    Update["AWS Lambda<br/>update-feedback"]

    DDB[("Amazon DynamoDB<br/>WorkSpotFeedback")]

    Logs["Amazon CloudWatch<br/>Logs"]

    Client -->|HTTPS Request| APIGW

    APIGW -->|POST /feedback| Create
    APIGW -->|GET /feedback/{feedback_id}| Get
    APIGW -->|PATCH /feedback/{feedback_id}| Update

    Create -->|PutItem| DDB
    Get -->|GetItem| DDB
    Update -->|GetItem + UpdateItem| DDB

    Create --> Logs
    Get --> Logs
    Update --> Logs
```

## Request Flow

The client sends HTTP requests to API Gateway.

API Gateway routes each request to the appropriate Lambda function:

- `POST /feedback` → `create-feedback`
- `GET /feedback/{feedback_id}` → `get-feedback`
- `PATCH /feedback/{feedback_id}` → `update-feedback`

The Lambda functions interact with the `WorkSpotFeedback` DynamoDB table using least-privilege IAM permissions.

Lambda execution logs are sent to Amazon CloudWatch.
