from django.core.urlresolvers import reverse

from social.exceptions import AuthAlreadyAssociated, AuthCanceled
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware


class RedirectOnCancelMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return '/auth-canceled'
        else:
            return super(RedirectOnCancelMiddleware, self).get_redirect_uri(request, exception)


class ExampleSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def raise_exception(self, request, exception):
        return False

    def get_message(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            return 'Somebody is already using that account!'
        return super(SocialAuthExceptionMiddleware, self) \
            .get_message(request, exception)

    def get_redirect_uri(self, request, exception):
        if request.user.is_authenticated():
            return reverse('done')
        else:
            return reverse('error')
