import uuid

user_key = 'uid'
ten_years = 60 * 60 * 24 * 365 * 10

class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(user_key, uid, max_age=ten_years, httponly=True)
        return response

    def generate_uid(self,request):
        try:
            uid = request.COOKIES[user_key]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid