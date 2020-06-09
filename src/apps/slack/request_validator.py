"""Validate slack request"""
import hashlib
import hmac
import os

class RequestValidator: # pylint: disable=too-few-public-methods
    """RequestValidator contains a single method that
       validates the slack request
    """
    def __init__(self):
        self.request_header_timestamp = "X-Slack-Request-Timestamp"
        self.request_header_signature = "X-Slack-Signature"
        self.version_number = "v0"
        self.slack_signing_secret = os.environ['SLACK_SIGNING_SECRET']

    def is_valid(self, headers, data, current_time) -> bool:
        """Compute HMAC-SHA256 keyed hash to validate slack request
        see slack documentation for further detail
        https://api.slack.com/authentication/verifying-requests-from-slack
        """
        request_timestamp = headers[self.request_header_timestamp]

        # check timestamp to protect against replay attack
        elapsed_time = abs(int(current_time) - int(request_timestamp))
        if elapsed_time > 60 * 5:
            return False

        slack_signature = headers[self.request_header_signature]
        body = data.decode("utf-8")
        signature_base_string = f"{self.version_number}:{request_timestamp}:{body}"

        signing_secret_key_bytes = self.slack_signing_secret.encode("utf-8")
        signature_base_string_bytes = signature_base_string.encode("utf-8")

        hexdigest = hmac.new(
            signing_secret_key_bytes,
            msg=signature_base_string_bytes,
            digestmod=hashlib.sha256,
        ).hexdigest()

        computed_signature = f"v0={hexdigest}"

        return slack_signature == computed_signature
