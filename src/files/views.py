from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.utils.decorators import method_decorator


from cfehome.aws.utils import AWS
from .models import S3File

User = get_user_model()

class DownloadView(View):
    def get(self, request, id, *args, **kwargs):
        file_obj = get_object_or_404(S3File, id=id)
        if request.user != file_obj.user:
            raise Http404
        url  = file_obj.get_download_url()
        return HttpResponseRedirect(url)

class UploadView(TemplateView):
    template_name = 'upload.html'


@method_decorator(csrf_exempt, name='dispatch')
class UploadPolicyView(View):
    def get(self, request, *args, **kwargs):
        #key = request.GET.get('key', 'unknown.jpg')
        #botocfe = AWS()
        #presigned_data = botocfe.presign_post_url(key=key)
        return JsonResponse({"detail": "Method not allowed"}, status=403)

    
    def post(self, request, *args, **kwargs):
        """
        Requires Security
        """
        user    = User.objects.first() #cfe user # request.user
        qs      = S3File.objects.filter(user=user)
        count   = qs.count() + 1
        key     = f'users/{user.id}/files/{count}/filename.png'
        obj     = S3File.objects.create(
                    user=user,
                    key=key,
                    name='default.png'
                )
        #key = request.POST.get('key', 'unknown.jpg')
        botocfe = AWS()
        presigned_data = botocfe.presign_post_url(key=key)
        return JsonResponse(presigned_data)






