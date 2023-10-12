from django.urls import path
from .views import HomePageView, GalleryPageView, GalleryPostView, GalleryPostReview

urlpatterns = [
    path('', HomePageView.as_view(), name='Home'),
    path('gallery/', GalleryPageView.as_view()),
    path('gallery/<int:post_id>/', GalleryPostView.as_view({'get': 'get_post'})),
    path('gallery/<int:post_id>/leave_review/', GalleryPostReview.as_view({'post': 'create_review'})),
    path('gallery/<int:post_id>/delete_review/', GalleryPostReview.as_view({'post': 'delete_review'})),
    path('gallery/<int:post_id>/like_post/', GalleryPostView.as_view({'post': 'like_post'})),

]
