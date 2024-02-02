# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupForm


@login_required
def group_list(request):
    groups = Group.objects.filter(members=request.user)
    return render(request, 'groups/group_list.html', {'groups': groups})


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)
            return redirect('groups:group_list')
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})



@login_required
def join_group(request, pk):
    group = Group.objects.get(id=pk)
    group.members.add(request.user)
    return render(request, 'groups/join_group.html', {'groups': group})
    # return redirect('groups:group_list')
