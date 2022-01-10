import json
def sendResJson(data, message, code):
    if code != 200:
        return json.dumps(
            {
                'code': code,
                'message': message
            }
        )
    else:
        return json.dumps(
            {
                'code': code,
                'message': 'success',
                'data':data
            }
        )