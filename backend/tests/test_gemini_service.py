from app.services.gemini_service import normalize_api_key, gemini_error_message


def test_normalize_api_key_strips_whitespace_and_quotes():
    assert normalize_api_key('  "abc123"  ') == 'abc123'
    assert normalize_api_key('  abc123  ') == 'abc123'


def test_gemini_error_message_for_quota_error():
    error = RuntimeError("429 You exceeded your current quota, please check your plan and billing details.")
    message = gemini_error_message(error)
    assert 'quota' in message.lower()
    assert 'billing' in message.lower()
