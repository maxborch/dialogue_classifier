from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import MediaForm, UploadForm  # , CaseForm
from .models import Upload, Media  # , Case, Disease
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
import pickle
import pandas as pd
import mimetypes
from django.http import HttpResponse
from django.conf import settings
from ml_model.extract_features import ExtractFeatures


def moderator_or_author_only(user, object):
    if user != object.user and not user.groups.filter(name='administrator').exists():
        raise PermissionDenied()


def moderator_only(user, object):
    if user.groups.filter(name='administrator').exists():
        raise PermissionDenied()


@login_required
def upload_file(request):
    if request.method == 'GET':
        form = UploadForm()
        media_form = MediaForm()
    elif request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        media_form = MediaForm(request.POST, request.FILES)
        if form.is_valid() and media_form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            files = request.FILES.getlist("files")
            for file in files:
                Media(upload=instance, file=file).save()
                messages.success(request,
                                 f'File successfully uploaded. Conversations will be classified... This may take a few seconds')
                make_predictions(instance, file)

                messages.success(request,
                                 f'Conversations from file "{file}" have been classified. You can view the results in the "My Dialogues" section.')
    return render(request, 'catalogue/form.html',
                  {'form': form, 'model_name': 'Upload', 'media_form': media_form})


def make_predictions(instance, file):
    path = '/Users/maxvonborch/Documents/Master_Thesis/Django/dialogue_classifier/models/lg'
    with open(path, 'rb') as model:
        ml_model = pickle.load(model)

    input_file = ExtractFeatures(f'{settings.MEDIA_ROOT}/{instance}/{file}').make_calcs()
    results = ml_model.predict(input_file)
    confidence = ml_model.predict_proba(input_file)
    confidence_bad = ["{0:.1f}%".format(confidence[i][1]*100) for i in range(len(confidence))]
    confidence_good = ["{0:.1f}%".format(confidence[i][0]*100) for i in range(len(confidence))]

    g_b = []
    for i in results:
        if i == 1:
            g_b.append("Bad")
        elif i == 0:
            g_b.append("Good")

    results_df = pd.DataFrame()
    results_df["Conversation"] = [f"Conversation {i}" for i in range(1, len(results)+1)]
    results_df["Results"] = g_b
    results_df["Confidence class 'Good'"] = confidence_good
    results_df["Confidence class 'Bad'"] = confidence_bad
    results_df.to_csv(f'{settings.MEDIA_ROOT}/{instance}/results.{file}')

    upload_instance = Upload.objects.get(id=str(instance))
    upload_instance.result = results
    upload_instance.save()
    # auto-delete uploaded files --> keep in?
    # Media.objects.get(upload_id=instance).delete()


def download_file(request, upload_id):
    file = Media.objects.get(upload=upload_id)
    # fill these variables with real values
    fl_path = f'{settings.MEDIA_ROOT}/{upload_id}/results.{file.filename()}'
    filename = f'results.{file.filename()}'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response


@login_required()
def edit_upload(request, upload_id):
    upload = Upload.objects.get(id=upload_id)
    moderator_or_author_only(request.user, upload)
    if request.method == 'GET':
        form = UploadForm(instance=upload)
        media_form = MediaForm()
    elif request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, instance=upload)
        media_form = MediaForm(request.POST, request.FILES)
        if form.is_valid() and media_form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            files = request.FILES.getlist("files")
            for file in files:
                Media(case=instance, file=file).save()
            messages.success(request, 'Upload successfully edited.')
            return redirect('/data/my-uploads')
    return render(request, 'catalogue/form.html', {'form': form, 'model_name': 'Upload', 'media_form': media_form})


def upload_detail(request, upload_id):
    if request.method == 'GET':
        upload = Upload.objects.get(id=upload_id)
        media = Media.objects.filter(upload_id=upload_id)

        return render(request, 'catalogue/upload_detail.html',
                      {'upload': upload, 'media': media, 'results': upload.result[1:-1].split(",")})


def delete_archive(request, archive_id):
    if request.method == 'POST':
        archive = Media.objects.get(id=archive_id)
        if request.user == archive.upload.user:
            upload_id = archive.upload_id
            archive.delete()
            return redirect(f'/data/upload/{upload_id}')
        else:
            raise PermissionDenied()


class UploadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    """
    model = Upload
    success_url = '/data/my-uploads'
    success_message = 'Upload successfully deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(UploadDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        upload = self.get_object()
        if (self.request.user.groups.filter(name='administrator').exists()) or self.request.user == upload.user:
            return True
        else:
            return False

    def handle_no_permission(self):
        return redirect(f'/data/upload/{self.get_object().id}')


def my_uploads(request):
    users_uploads = Upload.objects.filter(user_id=request.user)
    return render(request, 'catalogue/my_uploads.html', {'users_uploads': users_uploads})
