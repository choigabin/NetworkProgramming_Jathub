from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from jat.forms import IntroductionForm
from jat.models import Repository, Introduction, Comment


class RepositoryListView(generic.ListView):
    model = Repository


class RepositoryDetailView(generic.DetailView):
    model = Repository


class RepositoryCreateView(generic.CreateView):
    model = Repository
    fields = ['name', 'description', 'deadline']  # '__all__'
    template_name_suffix = '_create'
    success_url = reverse_lazy('jat:repository_list')


class RepositoryUpdateView(generic.UpdateView):
    model = Repository
    fields = ['name', 'description', 'deadline']  # '__all__'
    template_name_suffix = '_update'
    success_url = reverse_lazy('jat:repository_list')


class RepositoryDeleteView(generic.DeleteView):
    model = Repository
    success_url = reverse_lazy('jat:repository_list')


class IntroductionDetailView(generic.DetailView):
    model = Introduction

class IntroductionCreatView(generic.CreateView):
    model = Introduction
    fields = ['repository', 'version', 'contents', 'access']  # '__all__'
    template_name_suffix = '_create'

    # success_url = reverse_lazy('jat:repository_detail') #repository_detail은 pk가 필요함(ImproperlyConfigured at /repository/3/introduction/add/)
    def get_initial(self):
        repository = get_object_or_404(Repository, pk=self.kwargs['repository_pk'])
        introduction = repository.introduction_set.aggregate(
            Max('version'))  # 해당 repository의 introduction 중 version 최대값 구하자
        version = introduction['version__max']
        if version == None:  # introduction이 아예 없으면 version 기본값: 1
            version = 1
        else:  # introduction이 있으면 version 최대값에서 +1
            version += 1
        return {'repository': repository, 'version': version}

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})


def add_introduction(request, repository_pk): # return render(request, '템플릿 이름', 그 템플릿에 넘겨주는 context)

    if request.method == 'POST':    #post라면
        form = IntroductionForm(request.POST)   #introduction 만드는 form에서 입력한 정보 가져오기
        if form.is_vaild():      #그 정보가 valid(허가된, 입증된) 확인되면,
            form.save()       #DB에 저장
        return redirect('jat:repository_detail', pk=repository_pk)#repository_detail로 redirect


    else:    #post가 아니라면 (요청한 것 : introduction 만들기 위한 form 보여주기) 순서상으로는 얘가 먼저임!
        repository = get_object_or_404(Repository, pk=repository_pk) #repository를 DB에서 꺼내기
        introduction = repository.introduction_set.order_by('-version').first()
        # version을 구하기
        # contents(introduction의 내용) 가져오기
        if introduction == None:
            version = 1    #introduction이 없으면, (version +1)
            contents = ''  #introduction이 없으면 ' '
            access = 1
        else:
            version = introduction.version + 1  #version 구하기 (repository에 있는 introduction 중 가장 큰 버전 +1)ㅎ
            contents = introduction.contents    #introduction이 있으면 가장 큰 버전의 contents를 가져오기
            access = introduction.access
        inital = {'repository': repository, 'version': version, 'contents': contents, 'access': access}
        form = IntroductionForm(inital=inital)   #form 가져오기
        context = {'form': form, 'repository': repository}   #context = form, repository
    return render(request, 'jat/introduction_create.html', context)

class IntroductionUpdateView(generic.UpdateView):
    model = Introduction
    fields = ['repository', 'version', 'contents', 'access']  # '__all__'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})


class IntroductionDeleteView(generic.DeleteView):
    model = Introduction

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk': self.kwargs['repository_pk']})

class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['introduction', 'comment']  # '__all__'
    template_name_suffix = '_create'

    def get_initial(self):
        repository = get_object_or_404(Repository, pk=self.kwargs['repository_pk'])
        introduction = repository.introduction_set.aggregate(
            Max('version'))  # 해당 repository의 introduction 중 version 최대값 구하자
        version = introduction['version__max']
        return {'repository': repository}

    def get_success_url(self):
        return reverse_lazy('jat:introduction_detail', kwargs={'repository_pk': self.kwargs['repository_pk'], 'pk': self.kwargs['introduction_pk']})

class CommentUpdateView(generic.UpdateView):
    model = Comment
    fields = ['introduction', 'comment']  # '__all__'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse_lazy('jat:introduction_detail', kwargs={'repository_pk': self.kwargs['repository_pk'], 'pk': self.kwargs['introduction_pk']})


class CommentDeleteView(generic.DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('jat:introduction_detail', kwargs={'repository_pk': self.kwargs['repository_pk'], 'pk': self.kwargs['introduction_pk']})