from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from api.models import Posts, UserDetail
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email','password','is_active','is_staff','is_superuser', 'last_login']
        allowed_methods = ['get']
        filtering = {
            'username': ALL,
        }
        #TO DO
        # authentication = ApiKeyAuthentication()
        # authorization = DjangoAuthorization()

class DetailResource(ModelResource):
    user = GenericForeignKeyField({
        User: UserResource,
    }, 'user')
    class Meta:
        queryset = UserDetail.objects.all()
        resource_name = 'detail'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class PostResource(ModelResource):
    author = GenericForeignKeyField({
        User: UserResource,
    }, 'author')
    last_modified_by = GenericForeignKeyField({
        User: UserResource,
    }, 'last_modified_by')
    class Meta:
        queryset = Posts.objects.all()
        resource_name = 'post'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
