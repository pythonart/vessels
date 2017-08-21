from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms import formset_factory
from django.forms import BaseFormSet
from django.forms import modelform_factory
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet
from django.shortcuts import get_object_or_404 , get_list_or_404

from crew.models import *  

class PersonForm(ModelForm):
    class Meta:
        model=Person
        fields=['salutation','first_name','last_name','gender','dob',
        'place_of_birth','country_of_birth','nationality','email','photo','date_joined_company','key_number','rank','address','resume','incompatible_with']
        
        widgets={               'dob' :forms.DateInput(attrs={'class':'datepicker'}) ,
                 'date_joined_company':forms.DateInput(attrs={'class':'datepicker'}),
                 
        
                 } 



class SeaTimeForm(ModelForm):
    class Meta:
        model=Seatime
        fields=['vessel_name','person','rank','date_signed_on','date_signed_off']   
        widgets={ 'date_signed_on' : forms.DateInput(  attrs={'class':'datepicker'}  ) ,
                  'date_signed_off': forms.DateInput(  attrs={'class':'datepicker'}  )
                   }
    def clean(self):
            if any(self.errors):
                return
            try :                 
                date_signed_off=self.cleaned_data['date_signed_off']
            except KeyError:
                return 
            if date_signed_off!=None:
                date_signed_on=self.cleaned_data['date_signed_on']
                if date_signed_off < date_signed_on:
                    raise forms.ValidationError(" Sign off date before Sign on date ")                      
            

class BaseSeaTimeFormSet(BaseModelFormSet): 
        def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.queryset=Seatime.objects.none()

        def clean(self):
            if any(self.errors):
                return
            for form in self.forms:
                try :                 
                    date_signed_off=form.cleaned_data['date_signed_off']
                except KeyError:
                    return 
                if date_signed_off!=None:
                    date_signed_on=form.cleaned_data['date_signed_on']
                    if date_signed_off < date_signed_on:
                        raise forms.ValidationError(" Sign off date before Sign on date ")    
            

SeaTimeModelFormset=modelformset_factory(Seatime,
                                        fields=('vessel_name','person','rank','date_signed_on','date_signed_off'),
                                        formset=BaseSeaTimeFormSet,extra=2,
                                        widgets={ 'date_signed_on' : forms.DateInput(  attrs={'class':'datepicker'}  )
                                                 ,'date_signed_off': forms.DateInput(  attrs={'class':'datepicker'}  )} ,
                                         )                       
class ContractForm(ModelForm):
    class Meta:
        model=Contract
        fields=['vessel','person','rank','date_started','date_expired','wage_scale']
        widgets={ 'date_started' : forms.DateInput(  attrs={'class':'datepicker'}  ),
                  'date_expired' : forms.DateInput(  attrs={'class':'datepicker'}  )
                }
    def clean(self):
        if any(self.errors):
            return

        date_started=self.cleaned_data['date_started']
        date_expired=self.cleaned_data['date_expired']                
        if date_expired < date_started:
            raise forms.ValidationError(" Date Expired before Date Started ") 


class BaseContractFormSet(BaseModelFormSet):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.queryset=Contract.objects.none()

        def clean(self):
            if any(self.errors):
                return
            for form in self.forms:
              try :
                date_started=form.cleaned_data['date_started']
              except KeyError:      
                return 
                if date_started!=None:
                    date_expired=form.cleaned_data['date_expired']
                    if date_expired < date_started:
                        raise forms.ValidationError("Date Expired before Date Started")        
                    

ContractModelFormset=modelformset_factory(Contract,
                                          fields=('vessel','person','rank','date_started','date_expired','wage_scale'),
                                          formset=BaseContractFormSet,extra=5,
                                          widgets={ 'date_started' : forms.DateInput(  attrs={'class':'datepicker'}  )
                                                    ,'date_expired': forms.DateInput(  attrs={'class':'datepicker'}  )} ,
                                             
                                          )



class CrewCertificatesForm(ModelForm):
    class Meta:
        model=CrewCertificates
        fields=['person','certificate','date_issued','date_expiry','institute_name',
                'issued_place','certificate_no','certificate_file']
        widgets={'date_issued':forms.DateInput(  attrs={'class':'datepicker'}  ),
                 'date_expiry':forms.DateInput(  attrs={'class':'datepicker'}  ),   
                  }        



'''class SeatimeForm(forms.Form):
    vq=Vessels.objects.all()
    pq=Person.objects.all()
    rq=Rank.objects.all()
    date_signed_on=forms.DateField(label='Date Signed On')
    date_signed_off=forms.DateField(required=False)
    vessel_name=forms.ModelChoiceField(queryset=vq)
    person=forms.ModelChoiceField(queryset=pq)
    rank=forms.ModelChoiceField(queryset=rq)        
    id=forms.IntegerField(widget=forms.HiddenInput(),required=False)


class BaseSeatimeFormSet(BaseFormSet):
    def clean(self):
        """
        Checks if date signed off is equal to or lesser than date signed on.
         Checks if same person has the same date signed on or date signed off on two different entries.
        Bug: Does not check if same sign on and same sign off date is already entered.
        """
        if any(self.errors):

            return

        list_date_signed_on=[]
        list_date_signed_off=[]    
        for form in self.forms:
            if len(form.cleaned_data)!=0:
                date_signed_on=form.cleaned_data['date_signed_on']
                date_signed_off=form.cleaned_data['date_signed_off']
                person=form.cleaned_data['person']
            
                if date_signed_off < date_signed_on:
                    raise forms.ValidationError(" Date Signed off must be equal to or greater than Date Signed On")

            
                if (person,date_signed_on) in list_date_signed_on:
                    raise forms.ValidationError("Person has the same sign on two events")
                list_date_signed_on.append((person,date_signed_on))

                if (person,date_signed_off) in list_date_signed_off:
                    raise forms.ValidationError("Person has the same sign off on two events")
                list_date_signed_off.append((person,date_signed_off))


SeatimeFormSet=formset_factory(SeatimeForm,formset=BaseSeatimeFormSet ,extra=3)   
'''

