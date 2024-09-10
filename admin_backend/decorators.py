from django.shortcuts import redirect,render
# from functools import wraps

def super_login_required(function):
    def wrappeer(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            if request.user.role != 'ADMIN':
                return render(request, "unauthorized.html")
        return function(request,*args,**kwargs)
    return wrappeer