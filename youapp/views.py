from django.shortcuts import render, redirect
from django.views.generic import View

from pytube import YouTube

# Create your views here.

class index(View):
    def __init__(self, url=None):
        self.url = url

    def get(self, request):
        return render(request, 'youapp/index.html')  
    
    def post(self,request):
        if request.POST.get('fetch-vid'):
            self.url = request.POST.get('given_url')
            video = YouTube(self.url)
            vidTitle, vidThumbnail = video.title, video.thumbnail_url
            qual, stream = [], []
            for vid in video.streams.filter(progressive=True):
                qual.append(vid.resolution)
                stream.append(vid)

            context = {'vidTitle':vidTitle, 'vidThumbnail': vidThumbnail,
                        'qual':qual, 'stream': stream,
                        'url': self.url}
            
            return render(request, 'youapp/index.html', context)

        elif request.POST.get('download-vid'):
            self.url = request.POST.get('given_url')
            video = YouTube(self.url)
            stream = [x for x in video.streams.filter(progressive=True)]
            video_qual = video.streams[int(request.POST.get('download-vid')) - 1]
            video_qual.download()

            return redirect('home')

        return render(request, 'youapp/index.html')