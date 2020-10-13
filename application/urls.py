from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    # path('index', views.index, name="index"),
    path('register', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('becomenative', views.becomenative, name="becomenative"),
    path('documents', views.documents, name="documents"),
    path('upload-work', views.upload_work, name="upload-work"),
    path('submitwork', views.submitwork, name="submitwork"),
    path('deliverNow', views.deliverNow, name="deliverNow"),
    path("getDeliveries", views.getDeliveries, name="getDeliveries"),
    path("make_it_as", views.make_it_as, name="make_it_as"),
    path("inbox/<person_id>", views.inbox, name="inbox"),
    path("sendMsg", views.sendMsg, name="sendMsg"),
    path("getMsgs", views.getMsgs, name="getMsgs")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
