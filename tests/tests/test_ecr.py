import pytest
import random
from aws_easy_use import ecr
# import aws_easy_use

@pytest.mark.parametrize(
    "repo_name, tag, expected",[
        ("client-api-service", "23", True),
        ("client-api-service", "147", True),
        ("client-api-service", "299", True),
        ("client-api-service", "400", False),
    ]
)
def test_does_repo_has_tag(mocker, repo_name: str, tag: str, expected: bool):
    imageIds = [ {"imageDigest": str(i), "imageTag": str(i)} for i in range(300) ]
    random.shuffle(imageIds)

    class FakeClient:
        def __init__(self, *arg, **kwarg):
            pass

        def list_images(self, **input_dict):
            print(f"fake_client receives {input_dict}")
            if not input_dict.get("next_token"):
                response = {
                    "imageIds": imageIds[:100],
                    "nextToken": 'next_100_199'
                }
            elif input_dict.get("next_token") == 'next_100_199':
                response = {
                    "imageIds": imageIds[100:200],
                    "nextToken": 'next_200_299'
                }
            elif input_dict.get("next_token") == 'next_200_299':
                response = {
                    "imageIds": imageIds[200:300],
                    "nextToken": None
                }
            # print(response)
            return response

    mocker.patch('aws_easy_use.ecr.boto3.client', FakeClient)
    result = ecr.does_repo_has_tag(repo_name, tag)
    assert result == expected