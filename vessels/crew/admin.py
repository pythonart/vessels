from django.contrib import admin

# Register your models here.

from .models import Departments,CrewManagementCompany,TechnicalManagementCompany,OperationsManagementCompany
from .models import Owner,VesselType,Vessels,Rank,WageScale,Person,Contract,Seatime,SafetyManagementCompany,WageScale
from .models import CrewCertificates,CrewCertificateList, GeneralSettings

class ContractInline(admin.TabularInline):
    model=Contract
    extra=0

class SeaTimeInline(admin.TabularInline):
    model=Seatime
    extra=0
   
class PersonAdminlist(admin.TabularInline):
    model=Person
    extra=0

class CrewCertificatesAdminInline(admin.TabularInline):
    model=CrewCertificates
    list_display=('certificate','date_issued','date_expiry')
    extra=0


class PersonAdmin(admin.ModelAdmin):
    list_display=('id','key_number','rank','first_name','last_name','gender','dob',)
    list_filter=('first_name','rank','last_name','gender','dob','email','key_number')
    search_fields=('first_name','last_name','gender','dob','email','photo','key_number','rank')
    ordering=('rank__display_rank_priority',)
    inlines=[ContractInline,SeaTimeInline,CrewCertificatesAdminInline]

class VesselsAdmin(admin.ModelAdmin):
    list_display=('name','vessel_type','owner','managed','email')
    list_filter=('name','vessel_type','flag','managed','owner','crew_management','operations_management','safety_management','technical_management')
    search_fields=('name','flag',)
    inlines=[ContractInline,SeaTimeInline]

class RankAdmin(admin.ModelAdmin):
    list_display=('rank_name','rank_department','display_rank_priority')
    list_filter=('rank_name','rank_department')
    search_fields=('rank_name','rank_department')
    ordering=('display_rank_priority',)
    inlines=[PersonAdminlist]


class CrewCertificatesAdmin(admin.ModelAdmin):
    list_display=('person','certificate','date_issued','date_expiry','certificate_no','institute_name')    
    list_filter=('person','certificate','date_issued','date_expiry','certificate_no','institute_name')
    search_fields=('person','certificate','date_issued','date_expiry','certificate_no','institute_name')

#class VesselsAdmin(admin.ModelAdmin):
   #  list_display=('id','name','type','company','email','imo_no','kwh','deadweight')   
   #  list_filter=('id','name','type','company','email','imo_no','kwh','deadweight')
   #  search_fields=('id','name','type','company','email','imo_no','kwh','deadweight')


admin.site.register(Departments)
admin.site.register(CrewManagementCompany)
admin.site.register(TechnicalManagementCompany)
admin.site.register(OperationsManagementCompany)
admin.site.register(Owner)
admin.site.register(VesselType)
admin.site.register(Vessels,VesselsAdmin)
admin.site.register(Rank,RankAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(SafetyManagementCompany)
admin.site.register(WageScale)
admin.site.register(CrewCertificates,CrewCertificatesAdmin)
admin.site.register(CrewCertificateList)
admin.site.register(GeneralSettings)


#admin.site.register(Seatime)
#admin.site.register(Contracts)


