import boto3


# from global_var import CFG

# END_POINT = CFG.get('cognito', 'endpoint')
# POOL_ID = CFG.get('cognito', 'pool_id')
# CLIENT_ID = CFG.get('cognito', 'client_id')
UserPoolId="us-east-1_D6DyvBjr6"
client_id='4c5r41apul44f1p77e0fqbf5od'

params = {}
params['aws_access_key_id'] = "AKIAIZ7DJS3EF4TVYVIQ"
params['aws_secret_access_key'] = "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"

COGNITO_CLIENT = boto3.client('cognito-idp', **params)

# response = COGNITO_CLIENT.admin_confirm_sign_up(
#     # AuthFlow='USER_PASSWORD_AUTH',
#     # AuthParameters={
#     #     'USERNAME': 'testclient',
#     #     'PASSWORD': 'Fzy#1mima'
#     # },
#     Username="testclient",
#     UserPoolId="us-east-1_D6DyvBjr6"
# )

# print(response)

# from warrant import Cognito

# u = Cognito(UserPoolId,client_id,
#     username='testclient')

# u.authenticate(password='Fzy#1mima')
# tokens = {
#  'id_token': u['access_token'],
#  'refresh_token' : u['refresh_token'],
#  'access_token' : u['access_token']
# }

# u = Cognito(UserPoolId,client_id,
#     **tokens)

# u.change_password('Fzy#1mima','Fzy#1newmima')

import boto3
from warrant.aws_srp import AWSSRP

class MyAws(AWSSRP):
    def __init__(self, **kwargs):
        super(MyAws, self).__init__(**kwargs)

    def myset_new_password_challenge(self, new_password, client=None):
        boto_client = self.client or client
        auth_params = self.get_auth_params()
        response = boto_client.initiate_auth(
            AuthFlow='USER_SRP_AUTH',
            AuthParameters=auth_params,
            ClientId=self.client_id
        )
        if response['ChallengeName'] == self.PASSWORD_VERIFIER_CHALLENGE:
            challenge_response = self.process_challenge(response['ChallengeParameters'])
            tokens = boto_client.respond_to_auth_challenge(
                ClientId=self.client_id,
                ChallengeName=self.PASSWORD_VERIFIER_CHALLENGE,
                ChallengeResponses=challenge_response)

            if tokens['ChallengeName'] == self.NEW_PASSWORD_REQUIRED_CHALLENGE:
                challenge_response = {
                    'USERNAME': auth_params['USERNAME'],
                    'NEW_PASSWORD': new_password,
                    'userAttributes.phone_number': '+019176795949',
                    'userAttributes.given_name': 'Zhiyu',
                    'userAttributes.family_name': 'Feng',
                }
                new_password_response = boto_client.respond_to_auth_challenge(
                    ClientId=self.client_id,
                    ChallengeName=self.NEW_PASSWORD_REQUIRED_CHALLENGE,
                    Session=tokens['Session'],
                    ChallengeResponses=challenge_response)
                return new_password_response
            return tokens
        else:
            raise NotImplementedError('The %s challenge is not supported' % response['ChallengeName'])

aws = MyAws(username='testclient', password='Fzy#newmima123', pool_id='us-east-1_D6DyvBjr6',
             client_id='4c5r41apul44f1p77e0fqbf5od', client=COGNITO_CLIENT)
# print(aws.myset_new_password_challenge('Fzy#newmima123')['AccessToken'])
print(aws.authenticate_user()['AuthenticationResult']['AccessToken'])
# try:
#     tokens = aws.authenticate_user()
# except Exception as e:
#     print(e)

# print(tokens)