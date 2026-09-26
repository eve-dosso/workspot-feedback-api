import json
import boto3


dynamodb = boto3.resource("dynamodb", region_name="eu-west-3")
table = dynamodb.Table("WorkSpotFeedback")


def lambda_handler(event, context):
    try:
        feedback_id = event["pathParameters"]["feedback_id"]
        body = json.loads(event["body"])

        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "At least one field is required"
                })
            }

        allowed_fields = [
            "wifi_score",
            "comfort_score",
            "outlets",
            "noise_level",
            "work_pass",
            "call_friendly",
            "stay_policy"
        ]

        for field in body:
            if field not in allowed_fields:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": field + " cannot be updated"
                    })
                }

        if "wifi_score" in body:
            if body["wifi_score"] < 1 or body["wifi_score"] > 5:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "wifi_score must be between 1 and 5"
                    })
                }

        if "comfort_score" in body:
            if body["comfort_score"] < 1 or body["comfort_score"] > 5:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "comfort_score must be between 1 and 5"
                    })
                }

        existing = table.get_item(
            Key={"feedback_id": feedback_id}
        )

        if "Item" not in existing:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "Feedback not found"
                })
            }

        update_parts = []
        attribute_names = {}
        attribute_values = {}

        for field, value in body.items():
            name_placeholder = "#" + field
            value_placeholder = ":" + field

            update_parts.append(
                name_placeholder + " = " + value_placeholder
            )

            attribute_names[name_placeholder] = field
            attribute_values[value_placeholder] = value

        update_expression = "SET " + ", ".join(update_parts)

        response = table.update_item(
            Key={"feedback_id": feedback_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=attribute_names,
            ExpressionAttributeValues=attribute_values,
            ReturnValues="ALL_NEW"
        )

        updated_item = response["Attributes"]

        if "wifi_score" in updated_item:
            updated_item["wifi_score"] = int(updated_item["wifi_score"])

        if "comfort_score" in updated_item:
            updated_item["comfort_score"] = int(
                updated_item["comfort_score"]
            )

        return {
            "statusCode": 200,
            "body": json.dumps(updated_item)
        }

    except Exception as error:
        print(error)

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }