from auth0.v3.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier

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
        jwks_url = os.getenv('JWKS_URL')
        issuer = os.getenv('TOKEN_ISSUER')
        audience = os.getenv('AUTH0_AUDIENCE')
        logging.info(jwks_url)
        logging.info(issuer)
        logging.info(audience)
        try:
            signature_verifier = AsymmetricSignatureVerifier(jwks_url)
            token_verifier = TokenVerifier(
                signature_verifier=signature_verifier,
                issuer=issuer,
                audience=audience)
            token_verifier.verify(token)

            # トークンが有効であれば、適切なIAMポリシーを返す
            # resource = f'arn:aws:execute-api:*:{context.accountId}:{context.apiId}/{context.stage}/*/*'
            return self.generate_policy('sample', 'Allow', resource)
        except Exception as error:
            logging.error(error)
            return self.generate_policy('sample', 'Deny', '*')
