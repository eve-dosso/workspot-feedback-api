import json
import boto3


dynamodb = boto3.resource("dynamodb", region_name="eu-west-3")
table = dynamodb.Table("WorkSpotFeedback")


def lambda_handler(event, context):
    try:
        feedback_id = event["pathParameters"]["feedback_id"]

        response = table.get_item(
            Key={"feedback_id": feedback_id}
        )

        if "Item" in response:
            item = response["Item"]

            item["wifi_score"] = int(item["wifi_score"])
            item["comfort_score"] = int(item["comfort_score"])

            return {
                "statusCode": 200,
                "body": json.dumps(item)
            }

        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Feedback not found"
            })
        }

    except Exception as error:
        print(error)

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }