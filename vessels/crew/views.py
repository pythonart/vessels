from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404 , get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import UpdateView , CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django_tables2 import RequestConfig, SingleTableView



from crew.tables import *



from .forms import PersonForm,  SeaTimeModelFormset, SeaTimeForm, ContractModelFormset,ContractForm,CrewCertificatesForm

# Create your views here.

from django.http import HttpResponse

from crew.models import *   


class IndexView(LoginRequiredMixin,generic.ListView):
    template_name='crew/index.html'
    context_object_name='person'
    paginate_by=10
   
   
    def get_queryset(self):
        if self.request.user.is_staff:
            return Person.objects.all().order_by('rank__display_rank_priority')
        else :
            return get_list_or_404(Person, user=self.request.user )    



class PersonCreateView(PermissionRequiredMixin,CreateView):
    permission_required='crew.add_person'
    form_class=PersonForm
    model=Person
    template_name='crew/modelform.html'
    context_object_name='person'

class PersonUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required='crew.change_person'
    form_class=PersonForm
    model=Person
    template_name='crew/modelform.html'
    context_object_name='person'

class PersonDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required='crew.delete_person'
    form_class=PersonForm
    model=Person
    template_name='crew/deleteview.html'
    context_object_name='person'    
    success_url=reverse_lazy('crew:index')


class PersonDetailView(LoginRequiredMixin,DetailView):
      model=Person
      template_name='crew/person_detail.html'
      context_object_name='person'

      def get_queryset(self):
            if self.request.user.is_staff:
                return Person.objects.all().filter(pk=self.kwargs['pk'])
            else :
                return Person.objects.all().filter(user=self.request.user)
    # unable to user get_object_or_404 above. Also dont automatically get users view when
    # trying person detail id for another user.

@login_required
def personNriDetail(request,pk):
    '''
    Display NRI Status of a person, showing NRI Days completed in each 
    financial year, showing Days required to complete NRI and also 
    if person is on vacation, when he should join by to complete his NRI.
    If Person has not yet signed off, it calculates based on todays date.
    
    Module Required :nritime
    TODO: Pagination
    Bugs: Need to test and verify results.
    '''
    if request.user.is_staff :
        person=get_object_or_404(Person,pk=pk)
        seatimes=person.seatime_set.all()
        li=[]
    else :
        person=get_object_or_404(Person,user=request.user)
        seatimes=person.seatime_set.all()
        li=[]        

    for seatime in seatimes:
        li=join_nri_list(li, seatime.nrt().nriList)
    #sortedli=sorted(li, key=lambda nri: nri.yr.finYrName)
    li.sort(key=lambda nri: nri.yr , reverse=True )
    context={'nrilist':li , 'person':person }
    template_name='crew/nritime.html'    
    return render(request,template_name,context)

def personNriShipList(request,pk,finyr):
    '''
    This Views Shows the Ships Sailed on in a 
    Financial year, along with date on and off
    and NRI Days for that year.
    '''
    if request.user.is_staff :
        person=get_object_or_404(Person,pk=pk)
        seatimes=person.seatime_set.all()
        
    else :
        person=get_object_or_404(Person,user=request.user)
        seatimes=person.seatime_set.all()
    li=[]                   
    for seatime in seatimes:
        for obj in seatime.nrt().nriList:
            if obj.yr.finYrName==str(finyr):
                li.append(seatime)
                continue
         #if seatime.nrt().fson.finYrName== str(finyr) or seatime.nrt().fsoff.finYrName ==str(finyr) :
           # li.append(seatime)
    template_name='crew/shipnrilist.html'      
    context={'seatimes':li, 'person':person,'finyr':finyr }  
    return render(request,template_name,context)        


@login_required
@permission_required('crew.add_seatime')      
def SeaTimeBulkCreateView(request): 
    if request.method=="POST":
        formset=SeaTimeModelFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('crew:index'))
    else:
        formset=SeaTimeModelFormset()
    return render(request,'crew/formset.html',{'formset':formset})

@login_required
def SeaTimePersonDetailView(request,person_id):
    if request.user.is_staff:
        personseatime=Seatime.objects.all().filter(person=person_id)
        crew=get_object_or_404(Person,id=person_id)
    else:
        personseatime=Seatime.objects.all().filter(person__user=request.user)
        crew=get_object_or_404(Person,user=request.user)     
    
    paginator=Paginator(personseatime,10)
    page=request.GET.get('page')

    try :
        person_seatime=paginator.page(page)
    except PageNotAnInteger:
        person_seatime=paginator.page(1)   
    except EmptyPage:
        person_seatime=paginator.page(paginator.num_pages)     

    template_name='crew/seatime_detail.html'
    context={'seatime_list':person_seatime, 'crew': crew, }
    return render(request,template_name,context)

class SeaTimeUpdateView(UserPassesTestMixin,UpdateView):
      form_class=SeaTimeForm
      model=Seatime
      template_name='crew/modelform.html'
      context_object_name='seatime' 
      success_url=reverse_lazy('crew:index')

      def test_func(self):
          if self.request.user.has_perm('crew.change_seatime'):
              return True
          if self.request.user.is_staff :
              return True 
          else :
                 seatimeobj=get_object_or_404(Seatime, pk=self.kwargs['pk'])
                 if seatimeobj.person.user==self.request.user:
                    return True
                 else:
                    return False    
                  

class SeaTimeDeleteView(PermissionRequiredMixin,DeleteView):
      permission_required='crew.delete_seatime'
      form_class=SeaTimeForm
      model=Seatime
      template_name='crew/deleteview.html'
      context_object_name='seatime' 
      success_url=reverse_lazy('crew:index') 

@login_required
@permission_required('crew.add_contract')
def ContractBulkCreateView(request): 
    if request.method=="POST":
        formset=ContractModelFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('crew:index'))
    else:
        formset=ContractModelFormset()
    return render(request,'crew/formset.html',{'formset':formset})


class ContractListView(LoginRequiredMixin,generic.ListView):
      model=Contract
      fields=['date_started','date_expired','vessel','person','rank','wage_scale']
      template_name='crew/contract_list.html'
      context_object_name='contract'
      paginate_by=10

      def get_queryset(self):
          if self.request.user.is_staff:
              contracts=Contract.objects.all().order_by('date_started')
              return contracts
          else :
              p=get_object_or_404(Person, user=self.request.user)
              contracts=p.contract_set.all().order_by('date_started')
              return contracts


class ContractUpdateView(PermissionRequiredMixin,UpdateView):
      permission_required='crew.change_contract'
      form_class=ContractForm
      model=Contract
      template_name='crew/modelform.html'
      context_object_name='contract'
      success_url=reverse_lazy('crew:certificate_index')

      #widgets={ 'date_started':DateInput(attrs={ 'class':'datepicker'}),'date_expired':DateInput(attrs={ 'class':'datepicker'})    }


class ContractCreateView(PermissionRequiredMixin,CreateView):
    """
    Enables single entry of a contract
    """
    permission_required='crew.add_contract'
    form_class=ContractForm
    model=Contract
    template_name='crew/modelform.html'
    context_object_name='contract'
    success_url=reverse_lazy('crew:contract_view')

class ContractDeleteView(PermissionRequiredMixin,DeleteView):
      permission_required='crew.delete_contract'
      model=Contract
      template_name='crew/deleteview.html'
      context_object_name='contract' 
      success_url=reverse_lazy('crew:index')   


@login_required
def ContractPersonDetailView(request,person_id):
    try   : 
        if  request.user.is_staff :
            contracts=Contract.objects.all().filter(person=person_id)
        else:
            p=get_object_or_404(Person,user=request.user)
            contracts=p.contract_set.all()    
    except :
         return Http404(" No Person Found ")

    paginator=Paginator(contracts ,1)
    page=request.GET.get('page')
    
    try :
        person_contract=paginator.page(page)
    except PageNotAnInteger:
        person_contract=paginator.page(1)   
    except EmptyPage:
        person_contract=paginator.page(paginator.num_pages) 

    template_name='crew/contract_list.html'
    context={'contract':person_contract, 'page_obj':person_contract }
    return render(request,template_name,context)


class CrewCertificatesCreateView(LoginRequiredMixin ,CreateView):
      '''
      Upload a Certificate for a person
      '''
      form_class=CrewCertificatesForm
      model=CrewCertificates
      template_name='crew/modelform.html'
      context_object_name='crew_certificate'
      success_url=reverse_lazy('crew:index') 

      #Raise a validation error for entering a cert under another user.  
      #instead of directly assigning the cert. under that user.
      def form_valid(self,form):
            if request.user.is_staff or request.user.has_persm('crew.add_crewcertificates'):
                return super().form_valid(form)
            else :      
                person=get_object_or_404(Person, user=self.request.user)
                form.instance.person=person
                return super().form_valid(form)
        




class CrewCertificatesUpdateView(UserPassesTestMixin, UpdateView):
      '''
      Update a Certificate for a person
      '''
      form_class=CrewCertificatesForm
      model=CrewCertificates
      template_name='crew/modelform.html'
      context_object_name='crew_certificate'
      success_url=reverse_lazy('crew:index')

      def test_func(self):
          if self.request.user.has_perm('crew.change_crewcertificates'):
              return True
          if self.request.user.is_staff :
              return True 
          else :
                 certobj=get_object_or_404(CrewCertificates, pk=self.kwargs['pk'])
                 if certobj.person.user==self.request.user:
                    return True
                 else:
                    return False 



class CrewCertificatesDeleteView(PermissionRequiredMixin,DeleteView):
      '''
      Delte a Persons Certficiate
      '''
      permission_required='crew.delete_crewcertificates'
      model=CrewCertificates
      template_name='crew/deleteview.html'
      context_object_name='crew_certificate'
      success_url=reverse_lazy('crew:index')


class PersonsCertificatesListView(UserPassesTestMixin ,generic.ListView):
      '''
      List of certificates of all crew members uploaded
      '''
      model=CrewCertificates
      template_name='crew/person_certificate_index.html'
      context_object_name='crew_certificate'
      paginate_by = 10 

      def test_func(self):
          if self.request.user.is_staff:
              return True
          else:
              False 



class PersonCertificates(LoginRequiredMixin,generic.ListView):
      '''
      List of certificates of a particular crew member uploaded
      '''
      model=CrewCertificates
      template_name='crew/person_certificate_index.html'
      context_object_name='crew_certificate'  
      paginate_by = 10

      def get_queryset(self):
          self.person=get_object_or_404(Person,id=self.kwargs['pk'] )
          return self.person.crewcertificates_set.all()




class CrewCertificateListCreatView(PermissionRequiredMixin ,CreateView):
      '''
      Add new type of certificates
      '''
      permission_required='crew.add_crewcertificatelist'
      model=CrewCertificateList
      template_name='crew/modelform.html'
      context_object_name='certificate'
      fields=['certificate_name','national_cert','flag_cert','company_required',
              'renewal_required','required_for_ranks','paid_for_by','reminder_required']        
      success_url=reverse_lazy('crew:certificate_index')


class CrewCertificateListUpdateView(PermissionRequiredMixin,UpdateView):
      '''
      Update new type of certificates
      '''
      permission_required='crew.change_crewcertificatelist'
      model=CrewCertificateList
      template_name='crew/modelform.html'
      context_object_name='certificate'  
      fields=['certificate_name','national_cert','flag_cert','company_required',
              'renewal_required','required_for_ranks','paid_for_by','reminder_required']      
      success_url=reverse_lazy('crew:certificate_index')    

class CrewCertificateListDeleteView(PermissionRequiredMixin ,DeleteView):
      '''
      Delete new type of certificates
      '''
      permission_required='crew.delete_crewcertificatelist'
      model=CrewCertificateList
      template_name='crew/deleteview.html'
      context_object_name='certificate'       
      success_url=reverse_lazy('crew:certificate_index')

class CrewCertificateIndexView(PermissionRequiredMixin,generic.ListView):
      '''
      List of types of certificates
      '''
      permission_required='crew.change_crewcertificatelist'
      model=CrewCertificateList
      template_name='crew/certificate_index.html'
      context_object_name='certificate_list' 
      paginate_by=10    



# Rank Views Start-----------

class RankIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_rank'
      template_name='crew/tables.html'
      model=Rank
      table_class=RankListTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Rank List'
          return context
      


class RankCreateView(PermissionRequiredMixin,CreateView):
      '''
      Add a Rank for a Ship and Also for Shore based personnel.
      '''
      permission_required='crew.add_rank'
      model=Rank
      template_name='crew/modelform.html'
      context_object_name='rank'  
      fields=['rank_name','rank_short_name','rank_department','display_rank_priority']

class RankUpdateView(PermissionRequiredMixin, UpdateView):
      '''
      Update A Ranks Details
      '''
      permission_required='crew.change_rank'
      model=Rank
      template_name='crew/modelform.html'
      context_object_name='rank'
      fields=['rank_name','rank_short_name','rank_department','display_rank_priority']

class RankDeleteView(PermissionRequiredMixin, DeleteView):
      '''
       Delete a Rank, Warning will delete all crew associated with the rank.
       Should fix or check this.
      '''      
      permission_required='crew.delete_rank'
      model=Rank
      template_name='crew/deleteview.html'
      context_object_name='rank'       
      success_url=reverse_lazy('crew:rank_type_list')


#Rank Views end------  

#Department Views start-----

class DepartmentsIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_departments'
      template_name='crew/tables.html'
      model=Departments
      table_class=DepartmentsTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Departments Type'
          return context


class DepartmentsCreateView(PermissionRequiredMixin,CreateView):
      permission_required='crew.add_departments'
      model=Departments
      template_name='crew/modelform.html'
      context_object_name='departments'  
      fields=['department_type','department_email'] 


class DepartmentsUpdateView(PermissionRequiredMixin, UpdateView):
      permission_required='crew.change_departments'
      model=Departments
      template_name='crew/modelform.html'
      context_object_name='departments'
      fields=['department_type','department_email']      

class DepartmentsDeleteView(PermissionRequiredMixin, DeleteView):
      permission_required='crew.delete_departments'
      model=Departments
      template_name='crew/deleteview.html'
      context_object_name='departments'
      success_url=reverse_lazy('crew:department_type_list')

#Department views end---


#vessel type views start ---
class VesselTypeIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_vesseltype'
      template_name='crew/tables.html'
      model=VesselType
      table_class=VesselTypeTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Vessel Types'
          return context

class VesselTypeCreateView(PermissionRequiredMixin ,CreateView):
      '''
      Add Vessel Types
      '''
      permission_required='crew.add_vesseltype'
      model=VesselType
      template_name='crew/modelform.html'
      context_object_name='vessel_type'
      fields=['vessel_type']
      success_url=reverse_lazy('crew:vessel_type_list')


class VesselTypeUpdateView(PermissionRequiredMixin ,UpdateView):
      '''
      Update Vessel Types
      '''
      permission_required='crew.change_vesseltype'
      model=VesselType
      template_name='crew/modelform.html'
      context_object_name='vessel_type'
      fields=['vessel_type']
      success_url=reverse_lazy('crew:vessel_type_list') 

class VesselTypeDeleteView(PermissionRequiredMixin ,DeleteView):
      '''
      Delete Vessel Types
      '''
      permission_required='crew.delete_vesseltype'
      model=VesselType
      template_name='crew/modelform.html'
      template_name='crew/deleteview.html'
      success_url=reverse_lazy('crew:vessel_type_list')           

#Vessel type views end-------

#crew management company views start---

class CrewManagementCompanyIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_crewmanagementcompany'
      template_name='crew/tables.html'
      model=CrewManagementCompany
      table_class=CrewManagementCompanyTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Crew Management Companies'
          return context


class CrewManagementCompanyCreateView(PermissionRequiredMixin ,CreateView):
      '''
      Add a Crew Management Company
      '''
      permission_required='crew.add_crewmanagementcompany'
      model=CrewManagementCompany
      template_name='crew/modelform.html'
      context_object_name='crew_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:crew_management_company_list')


class CrewManagementCompanyUpdateView(PermissionRequiredMixin ,UpdateView):
      '''
      Update a Crew Management Company
      '''
      permission_required='crew.change_crewmanagementcompany'
      model=CrewManagementCompany
      template_name='crew/modelform.html'
      context_object_name='crew_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:crew_management_company_list')      

class CrewManagementCompanyDeleteView(PermissionRequiredMixin ,DeleteView):
      '''
      Delete a Crew Management Company
      '''
      permission_required='crew.change_crewmanagementcompany'
      model=CrewManagementCompany
      template_name='crew/deleteview.html'
      context_object_name='crew_management_company'
      success_url=reverse_lazy('crew:crew_management_company_list') 

#crew management company views end----

#Technical management company views start--
class TechnicalManagementCompanyIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_technicalmanagementcompany'
      template_name='crew/tables.html'
      model=TechnicalManagementCompany 
      table_class=TechnicalManagementCompanyTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Technical Management Companies'
          return context


class TechnicalManagementCompanyCreateView(PermissionRequiredMixin ,CreateView):
      '''
      Add a Technical Management Company
      '''
      permission_required='crew.add_technicalmanagementcompany'
      model=TechnicalManagementCompany      
      template_name='crew/modelform.html'
      context_object_name='technical_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:technical_management_list')

class TechnicalManagementCompanyUpdateView(PermissionRequiredMixin ,UpdateView):
      '''
      Update a Technical Management Company
      '''
      permission_required='crew.change_technicalmanagementcompany'
      model=TechnicalManagementCompany      
      template_name='crew/modelform.html'
      context_object_name='technical_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:technical_management_list')


class TechnicalManagementCompanyDeleteView(PermissionRequiredMixin ,DeleteView):
      '''
      Delete a Technical Management Company
      '''
      permission_required='crew.delete_technicalmanagementcompany'
      model=TechnicalManagementCompany      
      template_name='crew/deleteview.html'
      context_object_name='technical_management_company'
      success_url=reverse_lazy('crew:technical_management_list')


#technical management company views end--

#Operations Management Company views start -

class OperationsManagementCompanyIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_operationsmanagementcompany'
      template_name='crew/tables.html'
      model=OperationsManagementCompany 
      table_class=OperationsManagementCompanyTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Operations Management Companies'
          return context


class OperationsManagementCompanyCreateView(PermissionRequiredMixin ,CreateView):
      '''
      Add a Operations Management Company
      '''
      permission_required='crew.add_operationsmanagementcompany'
      model=OperationsManagementCompany
      template_name='crew/modelform.html'
      context_object_name='operations_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:operations_management_list')

class OperationsManagementCompanyUpdateView(PermissionRequiredMixin ,UpdateView):
      '''
      Update a Operations Management Company
      '''
      permission_required='crew.change_operationsmanagementcompany'
      model=OperationsManagementCompany
      template_name='crew/modelform.html'
      context_object_name='operations_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:operations_management_list')

class OperationsManagementCompanyDeleteView(PermissionRequiredMixin ,DeleteView):
      '''
      Delete a Operations Management Company
      '''
      permission_required='crew.delete_operationsmanagementcompany'
      model=OperationsManagementCompany
      template_name='crew/modelform.html'
      template_name='crew/deleteview.html'
      success_url=reverse_lazy('crew:operations_management_list')      


#Operations management company views end --
#Safety management company views start --

class SafetyManagementCompanyIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_safetymanagementcompany'
      template_name='crew/tables.html'
      model=SafetyManagementCompany
      table_class=SafetyManagementCompanyTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Safety Management Companies'
          return context


class SafetyManagementCompanyCreateView(PermissionRequiredMixin ,CreateView):
      '''
      Add A Safety Management Company
      '''
      permission_required='crew.add_safetymanagementcompany'
      model=SafetyManagementCompany
      template_name='crew/modelform.html'
      context_object_name='safety_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:safety_management_list')  

class SafetyManagementCompanyUpdateView(PermissionRequiredMixin ,UpdateView):
      '''
      Update A Safety Management Company
      '''
      permission_required='crew.change_safetymanagementcompany'
      model=SafetyManagementCompany
      template_name='crew/modelform.html'
      context_object_name='safety_management_company'
      fields=['name','email','phone','department_type','address',]
      success_url=reverse_lazy('crew:safety_management_list')  

class SafetyManagementCompanyDeleteView(PermissionRequiredMixin ,DeleteView):
      '''
      Delete A Safety Management Company
      '''
      permission_required='crew.delete_safetymanagementcompany'
      model=SafetyManagementCompany
      template_name='crew/deleteview.html'
      context_object_name='safety_management_company'
      success_url=reverse_lazy('crew:safety_management_list')

#Safety management company views end --
#vessel onwer views start

class OwnerIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_owner'
      template_name='crew/tables.html'
      model=Owner
      table_class=OwnerTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Vessel Owners List'
          return context


class OwnerCreateView(PermissionRequiredMixin,CreateView):
      '''
      Add a Ship Owner
      '''
      permission_required='crew.add_owner'
      model=Owner
      template_name='crew/modelform.html'
      context_object_name='owner'
      fields=['name','imo_no','email','address',]
      success_url=reverse_lazy('crew:owner_list') 


class OwnerUpdateView(PermissionRequiredMixin,UpdateView):
      '''
      Update a Ship Owner
      '''
      permission_required='crew.change_owner'
      model=Owner
      template_name='crew/modelform.html'
      context_object_name='owner'
      fields=['name','imo_no','email','address',]
      success_url=reverse_lazy('crew:owner_list') 

class OwnerDeleteView(PermissionRequiredMixin,DeleteView):
      '''
      Delete a Ship Owner
      '''
      permission_required='crew.delete_owner'
      model=Owner
      template_name='crew/deleteview.html'
      context_object_name='owner'
      success_url=reverse_lazy('crew:owner_list') 


#owner views end      

#vessel views start 

class VesselIndexView(PermissionRequiredMixin, SingleTableView):
      permission_required='crew.change_vessels'
      template_name='crew/tables.html'
      model=Vessels
      table_class=VesselsTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Vessels  List'
          return context

class ManagedVesselIndexView(LoginRequiredMixin, SingleTableView):
      template_name='crew/tables.html'
      model=Vessels
      table_class=ManagedVesselsTable
      table_pagination={'per_page':10 }

      def get_context_data(self,**kwargs):
          context=super().get_context_data(**kwargs)
          context['viewname']='Managed Vessels List'
          return context


class VesselCreateView(PermissionRequiredMixin,CreateView):
      '''
      Add a vessel to the list of vessels.
      '''
      permission_required='crew.add_vessels'
      model=Vessels
      template_name='crew/modelform.html'
      context_object_name='vessel'
      success_url=reverse_lazy('crew:index')
      fields=['vessel_type','name','flag','port_of_registery','imo_no','official_no','email','kwh','bhp',
             'rpm','deadweight','net_tonnage','gross_tonnage','owner','crew_management','operations_management',
             'safety_management','technical_management','managed',
             ]
      success_url=reverse_lazy('crew:vessel_list')

class VesselUpdateView(PermissionRequiredMixin,UpdateView):
      '''
      Update a vessel to the list of vessels.
      '''
      permission_required='crew.change_vessels'
      model=Vessels
      template_name='crew/modelform.html'
      context_object_name='vessel'
      success_url=reverse_lazy('crew:index')
      fields=['vessel_type','name','flag','port_of_registery','imo_no','official_no','email','kwh','bhp',
             'rpm','deadweight','net_tonnage','gross_tonnage','owner','crew_management','operations_management',
             'safety_management','technical_management','managed',
             ]
      success_url=reverse_lazy('crew:vessel_list')      


class VesselDeleteView(PermissionRequiredMixin,DeleteView):
      '''
      Delete a vessel to the list of vessels.
      '''
      permission_required='crew.delete_vessels'
      model=Vessels
      template_name='crew/deleteview.html'
      context_object_name='vessel'
      success_url=reverse_lazy('crew:vessel_list')


    
#vessel views end
  

class WageScaleCreateView(PermissionRequiredMixin ,CreateView):
      '''
      Add Wage Scale 
      '''
      permission_required='crew.add_wagescale'
      model=WageScale
      template_name='crew/modelform.html'
      context_object_name='wage_scale'
      fields=['rank','level']
      success_url=reverse_lazy('crew:index') 



'''def personcreate(request):
    """
    Creates a Person using Model form PersonForm 
    Bug: Does not check if the person already exists in the database with same key no.
    """
    #action_url=reverse('crew:personcreate')
    if request.method=="POST":
        form=PersonForm(request.POST,request.FILES)

        if form.is_valid():
            p=form.save()
            return  HttpResponseRedirect(reverse('crew:index'))    
    else:   
        form=PersonForm()
    return   render(request,'crew/modelform.html',{'form':form, })'''             

            

       
def crewlist(request,vessel_id):
    """
    Gives a list containing a dict of a person object,a seatime object, a certificate object filtered
    to passport, List is ordered by rank display priority.
    Checks if a passport is entered. If not, it prints no passport entered.
    Need to add Date, Arrival Port, Last Port, through a form. And items passed to context.
    Should make header into a generic template to save work.
    """
    template_name='crew/crewlist.html'
    try:
        v=Vessels.objects.get(id=int(vessel_id)) # Gets all objects of a particular vessel.
    except Vessels.DoesNotExist:
        raise Http404("Vessel Does not exist")

           
    s=v.seatime_set.all().filter(date_signed_off__isnull=True).order_by('rank__display_rank_priority') # Filters all persons on board who
    # have not signed off
    person_list=[] # Creats a list to store all persons on board  
    for p in s:
        person_list.append(p.person_id)

       
    crew_list=[]
    for person_id in person_list:
        crew_details={'seatime_obj':'st','passport_obj':'','person_obj':''}
        person=Person.objects.get(id=person_id)
        crew_details['person_obj']=person
        st=Seatime.objects.filter(person=person.id).filter(vessel_name=vessel_id).filter(date_signed_off__isnull=True)
        st=st[0]
        crew_details['seatime_obj']=st
        pcr=person.crewcertificates_set.all().filter(certificate__certificate_name__icontains='passport')
        try:
            pcr=pcr[0]
        except:
            pcr={'certificate_no':'No Passport Entered'}    
        crew_details['passport_obj']=pcr
        crew_list.append(crew_details)
    try :    # If no crew are entered crew_list[0] will raise a IndexError
        context={'crew_list':crew_list,'vessel_id':vessel_id,'vessel':v,'master':crew_list[0]}
    except:  # Remove crew_list[0] from context   
        context={'crew_list':crew_list,'vessel_id':vessel_id,'vessel':v,}
    return render(request,template_name,context)   

  

'''
Deprecated and kept for learning reference.
Used earlier to enter a single persons Seatime. Now Form set below is used to bulk enter seatime
def sea_time_create_view(request):
    if request.method=="POST":
        form=SeatimeForm(request.POST)
        if form.is_valid():
            date_signed_on=form.cleaned_data['date_signed_on']
            date_signed_off=form.cleaned_data['date_signed_off']
            vessel_name=form.cleaned_data['vessel_name']
            person=form.cleaned_data['person']
            rank=form.cleaned_data['rank']
            st=Seatime()
            st.date_signed_on=date_signed_on
            st.date_signed_off=date_signed_off
            st.vessel_name=vessel_name
            st.person=person
            st.rank=rank
            st.save()

            return HttpResponseRedirect(reverse('crew:index'))
    else:
        form=SeatimeForm()
    return render(request,'crew/modelform.html',{'form':form})   '''    

'''def sea_time_create_view(request):
    """
    Used to Insert multiple instances of Sea time.
    Checks if date signed off is equal to or lesser than date signed on.
    Checks if same person has the same date signed on or date signed off on two different entries.
    Bug: Does not check if same sign on and same sign off date is already entered. 
    """
    if request.method=="POST":
        formset=SeatimeFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if len(form.cleaned_data)!=0 and form.has_changed() is not False:
                    # Above line filters out the empty form. As the empty form passes through the formset.is_valid() loop.
                    date_signed_on=form.cleaned_data['date_signed_on']
                    date_signed_off=form.cleaned_data['date_signed_off']
                    vessel_name=form.cleaned_data['vessel_name']
                    person=form.cleaned_data['person']
                    rank=form.cleaned_data['rank']
                    st=Seatime()
                    st.date_signed_on=date_signed_on
                    st.date_signed_off=date_signed_off
                    st.vessel_name=vessel_name
                    st.person=person
                    st.rank=rank
                    st.save()
            return HttpResponseRedirect(reverse('crew:index'))             
    else :
          formset=SeatimeFormSet()             
    return render(request,'crew/formset.html',{'formset':formset})   '''    

'''def sea_time_edit_view(request,person_id):
    """
    Used to view the first sea time entry for a person. Have to further include bulk sea time edit.
    """

    if request.method=="POST":
        form=SeatimeForm(request.POST)
        if form.is_valid():
            date_signed_on=form.cleaned_data['date_signed_on']
            date_signed_off=form.cleaned_data['date_signed_off']
            vessel_name=form.cleaned_data['vessel_name']
            person=form.cleaned_data['person']
            rank=form.cleaned_data['rank'] 
            st=get_list_or_404(Seatime,person_id=person_id)   
            st=st[0]
            st.date_signed_on=date_signed_on
            st.date_signed_off=date_signed_off
            st.vessel_name=vessel_name
            st.person=person
            st.rank=rank
            st.save()
            return  HttpResponseRedirect(reverse('crew:index'))   
    else:
        st=Seatime.objects.all().filter(person=person_id)
        try :
            st=st[0]
            form=SeatimeForm({'date_signed_on':st.date_signed_on,'date_signed_off':st.date_signed_off,'vessel_name':st.vessel_name.id,'person':st.person.id,'rank':st.rank.id})
        except :
            raise Http404('No Seatime Entered for Person')
    return   render(request,'crew/modelform.html',{'form':form, })  '''

'''def sea_time_edit_view(request,person_id):
    """
    Used to view/edit the  sea time entry for a person. 
    Bug: If From delete is selected on a empty from. The form passes 'len(form.cleaned_data)!=0 
    and form.has_changed() is not False: validation' and KeyError is raised for date_signed_on
    'len(form.cleaned_data)!=0 and form.has_changed() is not False: validation' is meant to eliminate empty forms.
    as even empty forms pass is_valid() validation.
    """
    if request.method=="POST":
        formset=SeatimeFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if len(form.cleaned_data)!=0 and form.has_changed() is not False:
                    # Above line filters out the empty form. As the empty form passes through the formset.is_valid() loop.
                    date_signed_on=form.cleaned_data['date_signed_on']
                    date_signed_off=form.cleaned_data['date_signed_off']
                    vessel_name=form.cleaned_data['vessel_name']
                    person=form.cleaned_data['person']
                    rank=form.cleaned_data['rank']
                    id=form.cleaned_data['id']
                    seatimeobject=Seatime.objects.all()
                    # st.date_signed_on=date_signed_on
                    # st.date_signed_off=date_signed_off
                    # st.vessel_name=vessel_name
                    # st.person=person
                    # st.rank=rank
                    # st.id=id
                    seatimeobject.update_or_create(id=id,defaults={'date_signed_on':date_signed_on,'date_signed_off':date_signed_off,
                        'person':person,'rank':rank,'vessel_name':vessel_name})
            for form in formset.deleted_forms:
                    id=form.cleaned_data['id']
                    seatimeobject=get_object_or_404(Seatime,pk=id)
                    seatimeobject.delete()

            return HttpResponseRedirect(reverse('crew:index'))      
                
    else:
        st=Seatime.objects.all().filter(person=person_id)
        try :
            data=[]
            for item in st.values():
                date_signed_on=item.get('date_signed_on')
                date_signed_off=item.get('date_signed_off')
                vessel_name=item.get('vessel_name_id')
                person=item.get('person_id')
                rank=item.get('rank_id')   
                id=item.get('id')
                data.append({'id':id,'rank':rank,'person':person,'vessel_name':vessel_name,'date_signed_on':date_signed_on,'date_signed_off':date_signed_off})
                
            formset=SeatimeFormSet(initial=data)
        except :
            raise Http404('No Seatime Entered for Person')
    return   render(request,'crew/formset.html',{'formset':formset, }) '''     



