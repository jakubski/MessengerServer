import os
from messenger_server.responses import Responses

def test_sign_up_positive_response():
    assert Responses.SignUpResponse.get_positive_response() == (0).to_bytes(1, "big") + (4).to_bytes(1, "big")

def test_bait():
    assert 4 == 5
