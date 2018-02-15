import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response, Http404
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory

from .models import Contact, Contact_Group
from .forms import ContactForm, BaseContactFormSet, Contact_GroupForm, UploadFileForm
from .resources import ContactResource

from tablib import Dataset


# Contact list.
@login_required(login_url='/login/')
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user).order_by('-created')
    return render(request, 'contacts/contacts.html', {'contacts': contacts})


@login_required(login_url='/login/')
def contact_count(request):
    contact_count = Contact.objects.filter(user=request.user).count()
    return render(request, 'contacts/contact_count.html',
                  {'contact_count': contact_count})


@login_required(login_url='/login/')
def contact_create(request):
    user = request.user

    # Create the formset, specifying the form and formset we want to use.
    ContactFormSet = formset_factory(ContactForm, formset=BaseContactFormSet)

    if request.method == 'POST':
        contact_formset = ContactFormSet(request.POST)
        if contact_formset.is_valid():
            # Now save the data for each form in the formset
            new_contacts = []

            for form in contact_formset:
                full_name = form.cleaned_data.get('full_name')
                mobile = form.cleaned_data.get('mobile')
                category = form.cleaned_data.get('category')

                if full_name and mobile and category:
                    new_contacts.append(Contact(user=user, 
                        full_name=full_name, mobile=mobile, category=category))

            try:
                with transaction.atomic():
                    #Replace the old with the new
                    Contact.objects.filter(user=user).delete()
                    Contact.objects.bulk_create(new_contacts)

                    # And notify our users that it worked
                    messages.success(request, 'You have created contacts')

            except IntegrityError: #If the transaction failed
                messages.error(request, 'There was an error saving your contacts.')
                return redirect(reverse('contact_create'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    else:
        contact_formset = ContactFormSet(request.user)
    return render(request, 'contacts/contact_create.html', {'contact_formset': contact_formset})



"""Detail of a person.
   :param template: Add a custom template.
"""
@login_required(login_url='/login/')
def contact_detail(request, pk, template='contacts/contact_detail.html'):
    try:
        contact_detail = Contact.objects.get(pk__iexact=pk)
    except Contact.DoesNotExist:
        raise Http404("Contact does not exists.")

    kwvars = {
        'object': contact_detail,
    }
    return render_to_response(request, template, kwvars)


@login_required(login_url='/login/')
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.user, request.POST, instance=contact)
        if form.is_valid():
            contact_update = form.save(commit=False)
            contact_update.user = request.user
            contact_update.save()
            messages.success(request, "Contact Successfully Updated")
    else:
        form = ContactForm(request.user, instance=contact)
    return render(request, 'contacts/contact_update.html', {'form': form})


@login_required(login_url='/login/')
def contact_delete(request,
                   pk,
                   template_name='contacts/confirm_contact_delete.html'):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Contact Successfully Deleted")
        return redirect('contact_list')
    return render(request, template_name, {'object': contact})


@login_required(login_url='/login/')
def group_list(request):
    groups = Contact_Group.objects.filter(
        user=request.user).order_by('-created')
    return render(request, 'contacts/group_list.html', {'groups': groups})


@login_required
def group_count(request):
    group_count = Contact_Group.objects.filter(user=request.user).count()
    return render(request, 'contacts/group_count.html',
                  {'group_count': group_count})


@login_required(login_url='/login/')
def group_create(request):
    if request.method == 'POST':
        form = Contact_GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            if Contact_Group.objects.filter(
                user = request.user).exists() and Contact_Group.objects.filter(
                name = form.cleaned_data['name']).exists():
                messages.error(request, "Contact with that phone number Already Exists")
            else:
                group.save()
                form = Contact_GroupForm()
                messages.success(request, "Group Successfully Created")
    else:
        form = Contact_GroupForm()
    return render(request, 'contacts/group_create.html', {'form': form})


@login_required(login_url='/login/')
def group_update(request, pk):
    group = get_object_or_404(Contact_Group, pk=pk)
    if request.method == 'POST':
        form = Contact_GroupForm(request.POST, instance=group)
        if form.is_valid():
            group_update = form.save(commit=False)
            group_update.user = request.user
            group_update.save()
            messages.success(request, "Group Successfully Updated")
    else:
        form = Contact_GroupForm(instance=group)
    return render(request, 'contacts/group_update.html', {'form': form})


@login_required(login_url='/login/')
def group_delete(request,
                 pk,
                 template_name='contacts/confirm_group_delete.html'):
    group = get_object_or_404(Contact_Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Group Successfully Deleted")
        return redirect('group_list')
    return render(request, template_name, {'object': group})


@login_required(login_url='/login/')
def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            import_sheet = request.FILES['file'].save_to_database(
                model=Contact,
                mapdict=[
                    'first_name', 'last_name', 'mobile', 'id_number',
                    'category'
                ],
                commit=False)
            import_sheet.user = request.user
            import_sheet.save_to_database()
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest("Bad Request")
    else:
        form = UploadFileForm()
    return render(request, 'contacts/upload_form.html', {'form': form})


@login_required
def export_contact_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ['first_name', 'last_name', 'email', 'mobile', 'category'])
    contacts = Contact.objects.filter(user=request.user).values_list(
        'first_name', 'last_name', 'email', 'mobile', 'category_id')
    for contact in contacts:
        writer.writerow(contact)
    return response


@login_required
def contact_upload(request):
    if request.method == 'POST':
        contact_resource = ContactResource()
        dataset = Dataset()
        new_contact = request.FILES['myfile']
        imported_data = dataset.load(new_contact.read())
        result = contact_resource.import_data(dataset, dry_run=True)  # Test the data import
        if not result.has_errors():
            contact_resource.import_data(dataset, dry_run=False)  # Actually import now
    return render(request, 'contacts/contact_upload.html')


@login_required
def search(request):
    item = request.GET['q']
    search = Contact.objects.annotate(search=SearchVector(
        'first_name', 'last_name', 'mobile', 'email')).filter(search=item)
    return render(request, 'contacts/contact_search.html', {'object': search})
