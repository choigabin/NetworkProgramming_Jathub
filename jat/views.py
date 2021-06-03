from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from jat.models import Repository, Introduction


class RepositoryListView(generic.ListView):
    model = Repository


class RepositoryDetailView(generic.DetailView):
    model = Repository


class RepositoryCreateView(generic.CreateView):
    model = Repository
    fields = ['name', 'description', 'deadline']  # '__all__'
    template_name_suffix = '_create'
    # success_url = reverse_lazy('jat:repository_list')
    def get_initial(self):
        repository = get_object_or_404(Repository, pk=self.kwargs['repository_pk'])
        introduction = repository.introduction_set.aggregate(Max('version'))
        version = introduction['version_max'] #repository의 introduction의 최댓값
        if version == None: #introduction이 아예 없으면, version 기본값 1
            version = 1
        else:               #introduction이 있으면, version 최댓값에서 +1
            version += 1
        return {'repository': repository, 'version': version}

    def get_success_url(self):
        return reverse_lazy('jat:repository_detail', kwargs={'pk':self.kwargs['repository_pk']})


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