# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.template import RequestContext
from django.utils import simplejson

from huxley.core.models import *
from huxley.shortcuts import render_template


def dispatch(request, page='welcome'):
    """ Dispatch to the appropriate view per the request after checking
        for authentication and permissions. """
    if not request.user.is_authenticated():
        return render_template(request, 'auth.html')

    views = {'welcome': welcome,
             'preferences': preferences,
             'roster': roster,
             'attendance': attendance,
             'help': help,
             'bugs': bugs}

    try:
        return views[page](request, request.user.advisor_profile)
    except KeyError:
        return HttpResponseNotFound()
    except AdvisorProfile.DoesNotExist:
        return HttpResponseForbidden()


def welcome(request, profile):
    """ Display and/or edit the advisor's profile information. """
    school = profile.school
    if request.method == 'GET':
        return render_template(request, 'welcome.html', {'school': school})

    elif request.method == 'POST':
        # TODO (wchieng): refactor this into a Django form.
        request.user.first_name = request.POST.get('firstname')
        request.user.last_name = request.POST.get('lastname')
        request.user.save();
        school.name = request.POST.get('schoolname')
        school.address = request.POST.get('address')
        school.city = request.POST.get('city')
        school.zip = request.POST.get('zip')
        school.programtype = request.POST.get('programtype')
        school.timesattended = request.POST.get('attendance')
        school.primaryname = request.POST.get('primaryname')
        school.primaryemail = request.POST.get('primaryemail')
        school.primaryphone = request.POST.get('primaryphone')
        school.secondaryname = request.POST.get('secname')
        school.secondaryemail = request.POST.get('secemail')
        school.secondaryphone = request.POST.get('secphone')
        school.mindelegationsize = request.POST.get('minDel')
        school.maxdelegationsize = request.POST.get('maxDel')
        school.save();
        
        return HttpResponse()    


def preferences(request, profile):
    """ Display and/or update the advisor's country and committee
        preferences. """
    school = profile.school

    if request.method == 'POST':
        country_ids = request.POST.getlist('CountryPrefs')
        country_ids = [country_ids[i] for i in range(0,10,2)] + \
                      [country_ids[j] for j in range(1,11,2)]
        
        # Clear and reset country preferences, discounting duplicates.
        school.countrypreferences.clear()
        seen = set()
        for rank, country_id in enumerate(country_ids, start=1):
            if country_id and country_id not in seen:
                seen.add(country_id)
                CountryPreference.objects.create(school=school,
                                                 country_id=country_id,
                                                 rank=rank)
        
        # Clear and reset committee preferences.
        school.committeepreferences.clear()
        for committee in Committee.objects.filter(special=True):
            if committee.name in request.POST:
                school.committeepreferences.add(committee)
            
        school.save()
        return HttpResponse()

    # Interleave the country preferences for double-columning in the template.
    countries = Country.objects.filter(special=False).order_by('name')
    ctyprefs = list(school.countrypreferences.all()
                    .order_by("countrypreference__rank"))
    ctyprefs += [None]*(10 - len(ctyprefs)) # Pad the list to length 10.
    countryprefs = [(i+1, ctyprefs[i], ctyprefs[i+5]) for i in range(0, 5)]
    
    # Split the committees into pairs for double-columning in the template.
    committees = Committee.objects.filter(special=True)
    committees = [committees[i:i+2] for i in range(0, len(committees), 2)]
    committeeprefs = school.committeepreferences.all()
    
    return render_template(request, 'preferences.html',
                           {'countryprefs': countryprefs,
                            'countries': countries,
                            'committees': committees,
                            'committeeprefs':committeeprefs})


def roster(request, profile):
    """ Display the advisor's editable roster, or update information as
        necessary. """
    if request.method == 'POST':
        slot_data = simplejson.loads(request.POST['delegates'])
        for slot_id, delegate_data in slot_data.items():
            slot = DelegateSlot.objects.get(id=slot_id)
            if 'name' in delegate_data and 'email' in delegate_data:
                try:
                    delegate = slot.delegate
                    delegate.name = delegate_data['name']
                    delegate.email = delegate_data['email']
                    delegate.save()
                except Delegate.DoesNotExist:
                    Delegate.objects.create(name=delegate_data['name'],
                                            email=delegate_data['email'],
                                            delegateslot=slot)
            else:
                try:
                    slot.delegate.delete()
                except:
                    pass

        return HttpResponse()

    slots = DelegateSlot.objects.filter(assignment__school=profile.school) \
                                .order_by('assignment__committee__name')
    return render_template(request, 'roster_edit.html', {'slots' : slots})


def attendance(request, profile):
    """ Display the advisor's attendance list. """
    delegate_slots = DelegateSlot.objects.filter(
        assignment__school=profile.school)
    return render_template(request, 'check-attendance.html',
                           {'delegate_slots': delegate_slots})


def help(request, profile):
    """ Display a FAQ view. """
    questions = {category.name : HelpQuestion.objects.filter(category=category)
                 for category in HelpCategory.objects.all()}
    return render_template(request, 'help.html', {'categories': questions})


def bugs(request, profile):
    """ Display a bug reporting view. """
    return render_template(request, 'bugs.html')