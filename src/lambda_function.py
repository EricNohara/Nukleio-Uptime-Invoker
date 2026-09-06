import os
import requests

ENVIRONMENTS = {
    "prod": {
        "url": os.environ["PROD_API_URL"],
        "api_key": os.environ["PROD_PRIVATE_API_KEY"],
        "user_email": os.environ["PROD_USER_EMAIL"],
    },
    "dev": {
        "url": os.environ["DEV_API_URL"],
        "api_key": os.environ["DEV_PRIVATE_API_KEY"],
        "user_email": os.environ["DEV_USER_EMAIL"],
    },
}

REQUEST_TIMEOUT_SECONDS = 30


def invoke_uptime_endpoint(environment):
    """Invoke one environment without preventing the other from being checked."""
    config = ENVIRONMENTS[environment]
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "User-Email": config["user_email"],
    }

    try:
        response = requests.get(
            config["url"],
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return {
            "success": response.ok,
            "statusCode": response.status_code,
            "body": response.text,
        }
    except requests.RequestException as error:
        return {
            "success": False,
            "error": str(error),
        }

def lambda_handler(event, context):
    results = {
        environment: invoke_uptime_endpoint(environment)
        for environment in ENVIRONMENTS
    }

    return {
        "statusCode": 200 if all(result["success"] for result in results.values()) else 502,
        "body": results,
    }
