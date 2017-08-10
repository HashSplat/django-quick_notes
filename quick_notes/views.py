from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView

from .models import QuickNotes, Attachment
from .forms import QuickNotesForm


class QuickNotesListView(ListView):
    model = QuickNotes
    template_name = "quick_notes/quick_notes_list.html"
    context_object_name = "quick_notes_list"


class QuickNotesDetailView(DetailView):
    model = QuickNotes
    template_name = "quick_notes/quick_notes_details.html"
    context_object_name = "quick_note"


class QuickNotesFormView(FormView):
    template_name = "quick_notes/quick_notes_form.html"
    form_class = QuickNotesForm
    success_url = "quick_notes:quick_note"
