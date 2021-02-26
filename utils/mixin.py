from django.contrib.auth.decorators import login_required


class LoginRequiredMixin():
    @classmethod
    def as_view(cls, **initkwargs):  # 该as_view方法需要和原版的as_view方法参数一致
        # 调用父类as_view
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)