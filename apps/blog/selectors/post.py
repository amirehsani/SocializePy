from django.db.models import QuerySet
from apps.blog.models import Post, Subscription
from apps.users.models import BaseUser
from apps.blog.filters import PostFilter


def get_subscribers(*, user: BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)


def post_detail(*, slug: str, user: BaseUser, self_include: bool = True) -> QuerySet[Post]:
    subscription = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscription.append(user.id)

    return Post.objects.get(slug=slug, author__in=subscription)


def post_list(*, filters=None, user: BaseUser, self_include: bool = True) -> QuerySet[Post]:
    filters = filters or {}
    subscription = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscription.append(user.id)
    if subscription:
        qs = Post.objects.filter(author__in=subscription)
        return PostFilter(filters, qs).qs
    return Post.objects.none()
