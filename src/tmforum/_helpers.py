import json

import requests


def parse_response(response: requests.Response, context) -> dict:
    context.logger.debug(
        f"{response.status_code} - {response.headers.get('X-Trace-Id', '...')} - {response.text}"
    )
    item = json.loads(response.text) if response.text else {}
    if isinstance(item, dict):
        if item_id := item.get("id"):
            item_type = item.get("@type", "Item")
            item_status = item.get(
                "status",
                item.get(
                    "state",
                    item.get(
                        "lifecycleState",
                        item.get(
                            "lifecycleStatus",
                            "n/a",
                        ),
                    ),
                ),
            )
            context.logger.info(f"{item_type}: {item_id}  Status: {item_status}")
            return item
    return item
