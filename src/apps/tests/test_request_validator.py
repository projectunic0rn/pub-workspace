from ..slack.request_validator import RequestValidator

class TestRequestValidator:
    def test_hashcomputedsuccessfully_resultstrue(self):
        request_validator = RequestValidator()
        headers = {
            "X-Slack-Request-Timestamp":
            "1591546129",
            "X-Slack-Signature":
            "v0=d851131193ea4c08d01341f1312633206159cf8f2373f583b4de23097d42b0db",
        }
        data = b'{"token":"u7WkldfRg56a2d0WSpPGSbgA","challenge":"UcklIBxssrA5qby12qpcCy9oYOKg6631OZ8tKBIim7DGYZ09taV3","type":"url_verification"}'
        # Act
        result = request_validator.is_valid(headers, data, "1591546129")
        # Assert
        assert result == True

    def test_potentialreplayattack_resultsfalse(self):
        # Arrange
        request_validator = RequestValidator()
        headers = {
            "X-Slack-Request-Timestamp":
            "1591546129",
            "X-Slack-Signature":
            "v0=d851131193ea4c08d01341f1312633206159cf8f2373f583b4de23097d42b0db",
        }
        data = b'{"token":"u7WkldfRg56a2d0WSpPGSbgA","challenge":"UcklIBxssrA5qby12qpcCy9oYOKg6631OZ8tKBIim7DGYZ09taV3","type":"url_verification"}'
        # Act
        result = request_validator.is_valid(headers, data, "1591546430")
        # Assert
        assert result == False
