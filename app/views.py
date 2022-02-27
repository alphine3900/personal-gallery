
from django.shortcuts import render, redirect
from .models import Category, Photo
from .forms import newPhoto
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# Create your views here.



def gallery(request):
    photos = Photo.objects.all()

    context = { 'photos': photos}
    return render(request, 'app/gallery.html', context)



def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'app/photos.html', {'photo': photo})



def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Image.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'app/add.html', context)


def Image(request):
    form=newPhoto()
    if request.method=="POST":
        output=newPhoto(request.POST, request.FILES)
        if output.is_valid():
            output.save()
            return  redirect('gallery')

    context={"form":form}
    return render(request, 'app/add.html', context)

