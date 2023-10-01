from .models import Post, PostReview, FavouritePost
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, PostReviewSerializer
from rest_framework.permissions import IsAuthenticated


class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return Response(template_name='home.html')
        else:
            return Response(template_name='403_not_authorised.html')


class GalleryPageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            queryset = Post.objects.all()
            serialized_posts = PostSerializer(queryset, many=True).data
            return Response({'posts': serialized_posts,
                             'template_name': 'gallery.html'}, template_name='gallery.html')
        return Response(template_name='403_not_authorised.html')


class GalleryPostView(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    @staticmethod
    def user_liked_post(current_user_id, post_id):
        try:
            fav_post = FavouritePost.objects.get(post_id=post_id, user_id=current_user_id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_post(self, request, post_id):
        if request.user.is_authenticated:
            current_user_id = request.user.id
            liked_post = self.user_liked_post(current_user_id, post_id)
            post = Post.objects.get(pk=post_id)
            post_reviews = PostReview.objects.filter(post=post)
            serialized_post_reviews = PostReviewSerializer(post_reviews, many=True).data
            serialized_post = PostSerializer(post).data
            return Response({'post': serialized_post, 'post_reviews': serialized_post_reviews,
                                  'user_id': current_user_id, 'liked_post': liked_post}, template_name='post.html')
        return Response(template_name='403_not_authorised.html')

    @staticmethod
    def like_post(request, post_id):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            post = Post.objects.get(pk=post_id)

            if request.data['cancel_like']:
                fav_post = FavouritePost.objects.get(post=post, user=user)
                fav_post.delete()

                post.count_likes -= 1
                post.save()

                return JsonResponse(data={'likes': post.count_likes, 'post_id': post_id}, status=status.HTTP_200_OK)

            new_fav_post = FavouritePost.objects.create(post=post, user=user)
            new_fav_post.save()

            post.count_likes += 1
            post.save()

            return JsonResponse(data={'likes': post.count_likes, 'post_id': post_id}, status=status.HTTP_200_OK)

        return Response(template_name='403_not_authorised.html')


class GalleryPostReview(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]

    @staticmethod
    def create_review(request, post_id):
        if request.user.is_authenticated:
            user_id = request.user.id

            reviewed_post = Post.objects.get(pk=post_id)
            reviewed_user = User.objects.get(pk=user_id)

            new_review = PostReview.objects.create(post=reviewed_post, author=reviewed_user, review_text=request.data['review_text'])
            new_review.save()

            return Response({
                'review_id': new_review.id,
                'review_text': new_review.review_text,
                'review_author': new_review.author.username
            }, status=status.HTTP_200_OK)
        return Response(template_name='403_not_authorised.html')

    @staticmethod
    def delete_review(request, post_id):
        if request.user.is_authenticated:
            review_id = request.data['review_id']
            review_obj = PostReview.objects.get(pk=review_id)
            review_obj.delete()

            return Response({}, status=status.HTTP_200_OK)
        return Response(template_name='403_not_authorised.html')

