import os
from datetime import datetime, timedelta
import jwt

SECRET = os.getenv('JWT_SECRET')


def create_token(token_data, **timedelta_kwargs):
    if not timedelta_kwargs:
        timedelta_kwargs = {'days': 2}
    current_time = datetime.utcnow()
    payload = {
        'data': token_data,
        'exp': current_time + timedelta(**timedelta_kwargs),
        'iat': current_time,
    }
    return jwt.encode(payload, SECRET,
                      algorithm='HS256')

def decode_token(token, verify=True):
    token_data = jwt.decode(token,
                            SECRET,
                            algorithms=['HS256'],
                            verify=verify)
    return token_data
