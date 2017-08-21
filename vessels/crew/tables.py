import django_tables2 as tables
from django_tables2.utils import A
import itertools
from django.utils.html import format_html
from django.urls import reverse
from crew.models import *
from crew.urls import *


class RankListTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    rank_name=tables.LinkColumn('crew:rank_type_update',args=[A('pk')])
    class Meta:
        model=Rank
        attrs={'class':'paleblue table table-bodered'}


    def __init__(self,*args,**kwargs):   
        super(RankListTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:rank_type_update', args=[(record.pk)])
        button2=reverse('crew:rank_type_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 )


class DepartmentsTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    department_type=tables.LinkColumn('crew:department_update',args=[A('pk')])
    class Meta:
        model=Departments
        attrs={'class':'paleblue table table-bodered'}


    def __init__(self,*args,**kwargs):   
        super(DepartmentsTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:department_update', args=[(record.pk)])
        button2=reverse('crew:department_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 ) 



class VesselTypeTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    vessel_type=tables.LinkColumn('crew:vessel_type_update',args=[A('pk')])
    class Meta:
        model=VesselType
        attrs={'class':'paleblue table table-bodered'}

    def __init__(self,*args,**kwargs):   
        super(VesselTypeTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:vessel_type_update', args=[(record.pk)])
        button2=reverse('crew:vessel_type_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 )               


class CrewManagementCompanyTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    name=tables.LinkColumn('crew:crew_management_company_update',args=[A('pk')])
    class Meta:
        model=CrewManagementCompany
        attrs={'class':'paleblue table table-bodered'}

    def __init__(self,*args,**kwargs):   
        super(CrewManagementCompanyTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:crew_management_company_update', args=[(record.pk)])
        button2=reverse('crew:crew_management_company_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 )         

class TechnicalManagementCompanyTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    name=tables.LinkColumn('crew:technical_management_update',args=[A('pk')])
    class Meta:
        model=TechnicalManagementCompany
        attrs={'class':'paleblue table table-bodered'}

    def __init__(self,*args,**kwargs):   
        super(TechnicalManagementCompanyTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:technical_management_update', args=[(record.pk)])
        button2=reverse('crew:technical_management_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 )         

class OperationsManagementCompanyTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    name=tables.LinkColumn('crew:operations_management_update',args=[A('pk')])
    class Meta:
        model=OperationsManagementCompany
        attrs={'class':'paleblue table table-bodered'}

    def __init__(self,*args,**kwargs):   
        super(OperationsManagementCompanyTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:operations_management_update', args=[(record.pk)])
        button2=reverse('crew:operations_management_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 )         

class SafetyManagementCompanyTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    name=tables.LinkColumn('crew:safety_management_update',args=[A('pk')])
    class Meta:
        model=SafetyManagementCompany
        attrs={'class':'paleblue table table-bodered'}

    def __init__(self,*args,**kwargs):   
        super(SafetyManagementCompanyTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:safety_management_update', args=[(record.pk)])
        button2=reverse('crew:safety_management_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 )  


class OwnerTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    name=tables.LinkColumn('crew:owner_update',args=[A('pk')])
    class Meta:
        model=Owner
        attrs={'class':'paleblue table table-bodered'}

    def __init__(self,*args,**kwargs):   
        super(OwnerTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:owner_update', args=[(record.pk)])
        button2=reverse('crew:owner_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 ) 


class VesselsTable(tables.Table):
    action=tables.Column(empty_values=(), orderable=False)
    name=tables.LinkColumn('crew:vessel_update',args=[A('pk')])
    owner=tables.LinkColumn('crew:owner_list')
    crew_management=tables.LinkColumn('crew:crew_management_company_list')
    operations_management=tables.LinkColumn('crew:operations_management_list')
    safety_management=tables.LinkColumn('crew:safety_management_list')
    technical_management=tables.LinkColumn('crew:technical_management_list')


    class Meta:
        model=Vessels
        attrs={'class':'paleblue table table-bodered'}

    def __init__(self,*args,**kwargs):   
        super(VesselsTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count()

    def render_action(self,record):
        button_update_html="<a href='{}' ><Button>Update</Button></a>"
        button_delete_html="<a href='{}' ><Button>Delete</Button></a>"
        button1=reverse('crew:vessel_update', args=[(record.pk)])
        button2=reverse('crew:vessel_delete', args=[(record.pk)])
        buttons=[button_update_html, button_delete_html]
        return format_html( ' '.join(buttons),  button1, button2 ) 



class ManagedVesselsTable(tables.Table):
    no=tables.Column(empty_values=())

    def __init__(self,*args,**kwargs):
        super(ManagedVesselsTable,self).__init__(*args,**kwargs)
        self.counter=itertools.count(start=1) 

    def render_no(self):
        return '%d' % next(self.counter)

    class Meta:
        model=Vessels
        attrs={'class':'paleblue table table-bodered'}
        fields={'name','flag','port_of_registery','vessel_type' }
        sequence=('no','name','flag','port_of_registery','vessel_type',)                                       