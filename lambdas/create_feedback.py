import json
import boto3
import random


dynamodb = boto3.resource("dynamodb", region_name="eu-west-3")
table = dynamodb.Table("WorkSpotFeedback")


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        if "location_name" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "location_name is required"
                })
            }

        if "city" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "city is required"
                })
            }

        if "location_type" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "location_type is required"
                })
            }

        if "wifi_score" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "wifi_score is required"
                })
            }

        if "comfort_score" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "comfort_score is required"
                })
            }

        wifi_score = body["wifi_score"]
        comfort_score = body["comfort_score"]

        if wifi_score < 1 or wifi_score > 5:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "wifi_score must be between 1 and 5"
                })
            }

        if comfort_score < 1 or comfort_score > 5:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "comfort_score must be between 1 and 5"
                })
            }

        feedback_id = "FB-" + str(random.randint(100, 999))

        item = {
            "feedback_id": feedback_id,
            "location_name": body["location_name"],
            "city": body["city"],
            "location_type": body["location_type"],
            "wifi_score": wifi_score,
            "comfort_score": comfort_score
        }

        if "outlets" in body:
            item["outlets"] = body["outlets"]

        if "noise_level" in body:
            item["noise_level"] = body["noise_level"]

        if "work_pass" in body:
            item["work_pass"] = body["work_pass"]

        if "call_friendly" in body:
            item["call_friendly"] = body["call_friendly"]

        if "stay_policy" in body:
            item["stay_policy"] = body["stay_policy"]

        table.put_item(
            Item=item
        )

        return {
            "statusCode": 201,
            "body": json.dumps(item)
        }

    except Exception as error:
        print(error)

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }