from django.conf.urls import url

from . import views as quick_notes_views

app_name = "quick_notes"

urlpatterns = [
    url(r'^$', quick_notes_views.QuickNotesListView.as_view(), name='index'),
    url(r'^Notes/$', quick_notes_views.QuickNotesListView.as_view(), name='list'),
    url(r'^Note/(?P<note>[\w\d\-]+)?$', quick_notes_views.QuickNotesDetailView.as_view(), name='detail'),
    url(r'^Note/update/(?P<note>[\w\d\-]+)?$', quick_notes_views.QuickNotesFormView.as_view(), name='update'),
    url(r'^Note/new/$', quick_notes_views.QuickNotesFormView.as_view(), name='new'),
]

