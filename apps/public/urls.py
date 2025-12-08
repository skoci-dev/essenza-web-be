from django.urls import path, include

urlpatterns = [
    path("/v1/subscribers", include("apps.public.subscriber.urls")),
    path("/v1/contact-messages", include("apps.public.contact_message.urls")),
    path("/v1/contact-messages", include("apps.public.contact_message.urls")),
    path("/v1/articles", include("apps.public.article.urls")),
    path("/v1/social-media", include("apps.public.social_media.urls")),
    path("/v1/banners", include("apps.public.banner.urls")),
    path("/v1/distributors", include("apps.public.distributor.urls")),
    path("/v1/stores", include("apps.public.store.urls")),
    path("/v1/projects", include("apps.public.project.urls")),
]
