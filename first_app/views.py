from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from first_app.forms import PostWriteForm
from first_app.models import House, Board
from django.contrib import messages
from django.http import JsonResponse


def index(request):

    # 동기 처리 (매번 새로고침을 해야 정보를 보여주는것)
    # 비동기 처리 (새로고침 없어도 정보를 보여줄수 있는것)
    # ajax => javascript => view(받아줌) => javascript로 return

    test = House.objects.all()

    get_request = request.POST.get('search_text', None)

    if get_request:
        boards = Board.objects.filter(hidden=False, title__contains=get_request).order_by('-created_at')
    else:
        boards = Board.objects.filter(hidden=False).order_by('-created_at')

    context = {
        'hello': 'Hello World!!!!!',
        'test': test,
        'boards': boards
    }
    return render(request, 'first_app/index.html', context)


def post_detail(request, pk):

    board = Board.objects.get(pk=pk)

    context = {
        'board': board
    }

    return render(request, 'first_app/post_detail.html', context)


@login_required
def post_write(request):
    print(request.user)

    if request.method == 'POST':
        print(request.POST)  # {'title': '테니스가 잼있어요', 'content': '정말 끌잼'}

        get_title = request.POST.get('title')
        print(get_title)
        if '테니스' in get_title or 'tennis' in get_title:
            messages.info(request, '테니스가 들어가는 제목이 들어있어요.')
            return redirect('index')

        form = PostWriteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('post_detail', pk=obj.pk)
    else:
        form = PostWriteForm()

    context = {
        'form': form
    }
    return render(request, 'first_app/post_write.html', context)


@login_required
def post_update(request, pk):
    print(request.user)

    data = Board.objects.get(pk=pk)

    if request.method == 'POST':
        print(request.POST)
        form = PostWriteForm(request.POST, instance=data)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('post_detail', pk=obj.pk)
    else:
        form = PostWriteForm(instance=data)

    context = {
        'form': form,
        'data': data
    }
    return render(request, 'first_app/post_write.html', context)


@login_required
def post_delete(request, pk):
    obj = Board.objects.get(pk=pk)
    obj.delete()

    return redirect('index')


@login_required
def ajax_study(request):
    return render(request, 'first_app/ajax_study.html')


def text_data_ajax(request):

    get_data = request.GET.get('text_data', None)

    custom_data = get_data + '_Hello'

    print(custom_data)

    context = {
        'custom_data': custom_data
    }

    return JsonResponse(context)  # request한 곳으로 json 형식의 response를 하겠다.
