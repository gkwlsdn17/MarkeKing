from django.db import connection
from django.http import HttpResponseRedirect

# view_func : @login_required가 붙어 있는 함수
# request : view_func의 첫번째 인자
def login_required(view_func, login_url='/login'):

    def decorator(request, *args, **kwargs):
        # 로그인된 상태이므로 원래 view 함수를 실행한다
        if 'user_name' in request.session.keys():
            return view_func(request, *args, **kwargs)
        # 로그인을 하지 않았으므로, 로그인페이지로 redirect
        else:
            return HttpResponseRedirect(login_url)

    return decorator


