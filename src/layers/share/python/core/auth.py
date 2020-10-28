from jose import jwt
from urllib.request import urlopen
from core.error import LambdaException
import json
import logging
import os


class Auth:

    def get_token(self, event):
        '''
        event = {
            'type': 'TOKEN',
            'methodArn': 'arn:aws:execute-api:ap-northeast-1:xxxxx:yyyyy/stage/GET/items',
            'authorizationToken': 'Bearer xxxxxx'
        }
        '''
        if event.get('authorizationToken') is None:
            raise LambdaException(
                status_code=500,
                error_code='PARAMETER_ERROR',
                message='authorizationToken not found')
        token = event['authorizationToken']
        return token.split(' ')[1]

    def generate_policy(self, principal_id, effect, resource):
        return {
            'principalId': principal_id,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": effect,
                        "Resource": resource
                    }
                ]
            }
        }

    def verify(self, token, resource):
        domain = os.getenv('AUTH0_DOMAIN')
        jwks_url = f'https://{domain}/.well-known/jwks.json'
        issuer = os.getenv('TOKEN_ISSUER')
        audience = os.getenv('AUTH0_AUDIENCE')

        jsonurl = urlopen(jwks_url)
        jwks = json.loads(jsonurl.read())
        rsa_key = {}
        unverified_header = jwt.get_unverified_header(token)
        logging.debug(jwks)
        logging.debug(unverified_header)
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        logging.debug(rsa_key)

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms='RS256',
                audience=audience,
                issuer=issuer)
            logging.debug(payload)

            # TODO: 権限チェック

            # トークンが有効であれば、適切なIAMポリシーを返す
            # resource = f'arn:aws:execute-api:*:{context.accountId}:{context.apiId}/{context.stage}/*/*'
            return self.generate_policy(payload['sub'], 'Allow', resource)
        except Exception as error:
            logging.error(error)
            return self.generate_policy('sample', 'Deny', '*')
