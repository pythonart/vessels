from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.views.static import serve



app_name='crew'
urlpatterns=[  
url(r'^$',views.IndexView.as_view(),name='index'),
url(r'^person/create/$',views.PersonCreateView.as_view(),name='person_create'),
url(r'^person/update/(?P<pk>[0-9]+)/$',views.PersonUpdateView.as_view(),name='person_update'),
url(r'^person/detail/(?P<pk>[0-9]+)/$',views.PersonDetailView.as_view(),name='person_detail'),
url(r'^person/delete/(?P<pk>[0-9]+)/$',views.PersonDeleteView.as_view(),name='person_delete'),


url(r'^person/seatime/detail/(?P<person_id>[0-9]+)/$',views.SeaTimePersonDetailView,name='person_seatime_detail'),

url(r'^seatime/create/$',views.SeaTimeBulkCreateView,name='seatime_bulk_create'),
url(r'^seatime/edit/(?P<pk>[0-9]+)/$',views.SeaTimeUpdateView.as_view(),name='seatime_edit'),
url(r'^seatime/delete/(?P<pk>[0-9]+)/$',views.SeaTimeDeleteView.as_view(),name='seatime_delete'),

url(r'^contract/bulk/create/$',views.ContractBulkCreateView,name='contract_bulk_create'),
url(r'^contract/create/$',views.ContractCreateView.as_view(),name='contract_create'),
url(r'^contract/view/$',views.ContractListView.as_view(),name='contract_view'),
url(r'^contract/update/(?P<pk>[0-9]+)/$',views.ContractUpdateView.as_view(),name='contract_update'),
url(r'^contact/delete/(?P<pk>[0-9]+)/$',views.ContractDeleteView.as_view(),name='contract_delete'),
url(r'^person/contract/detail/(?P<person_id>[0-9]+)/$',views.ContractPersonDetailView,name='person_contract_detail'),

url(r'^certificate/create/$',views.CrewCertificateListCreatView.as_view(),name='certificate_create'),
url(r'^certificate/update/(?P<pk>[0-9]+)/$',views.CrewCertificateListUpdateView.as_view(),name='certificate_update'),
url(r'^certificate/delete/(?P<pk>[0-9]+)/$',views.CrewCertificateListDeleteView.as_view(),name='certificate_delete'),
url(r'^certificate/index/$',views.CrewCertificateIndexView.as_view(),name='certificate_index'),


url(r'^person/certificate/create/$',views.CrewCertificatesCreateView.as_view(),name='person_certificate_create'),
url(r'^person/certificate/update/(?P<pk>[0-9]+)/$',views.CrewCertificatesUpdateView.as_view(),name='person_certificate_update'),
url(r'^person/certificate/delete/(?P<pk>[0-9]+)/$',views.CrewCertificatesDeleteView.as_view(),name='person_certificate_delete'),
url(r'^person/certificate/index/$',views.PersonsCertificatesListView.as_view(), name='person_certificate_index'),
url(r'^person/certificate/list/(?P<pk>[0-9]+)/$',views.PersonCertificates.as_view(),name='person_certificates' ),

url(r'^wagescale/create/$',views.WageScaleCreateView.as_view(),name='wagescale_create'),
url(r'^crewlist/(?P<vessel_id>[0-9]+)/$',views.crewlist,name='crewlist'),

   ] 

#Rank urls
urlpatterns +=[
url(r'^ranktypes/list/$',views.RankIndexView.as_view(),name='rank_type_list'),    
url(r'^ranktype/create/$',views.RankCreateView.as_view(),name='rank_type_create'),
url(r'^ranktypes/update/(?P<pk>[0-9]+)/$',views.RankUpdateView.as_view(),name='rank_type_update'),
url(r'^ranktypes/delete/(?P<pk>[0-9]+)/$',views.RankDeleteView.as_view(),name='rank_type_delete'),

]

#Department urls
urlpatterns +=[
url(r'^department/list/$',views.DepartmentsIndexView.as_view(),name='department_type_list'),    
url(r'^department/create/$',views.DepartmentsCreateView.as_view(),name='department_create'),
url(r'^department/update/(?P<pk>[0-9]+)/$',views.DepartmentsUpdateView.as_view(),name='department_update'),
url(r'^department/delete/(?P<pk>[0-9]+)/$',views.DepartmentsDeleteView.as_view(),name='department_delete'),
]


#Vessel Type urls
urlpatterns +=[
url(r'^vessel/type/list/$',views.VesselTypeIndexView.as_view(),name='vessel_type_list'),    
url(r'^vessel/type/create/$',views.VesselTypeCreateView.as_view(),name='vessel_type_create'),
url(r'^vessel/type/update/(?P<pk>[0-9]+)/$',views.VesselTypeUpdateView.as_view(),name='vessel_type_update'),
url(r'^vessel/type/delete/(?P<pk>[0-9]+)/$',views.VesselTypeDeleteView.as_view(),name='vessel_type_delete'),
]

#crew management urls
urlpatterns +=[
url(r'^crew_management_company/list/$',views.CrewManagementCompanyIndexView.as_view(),name='crew_management_company_list'),     
url(r'^crew_management_company/create/$',views.CrewManagementCompanyCreateView.as_view(),name='crew_management_company_create'),
url(r'^crew_management_company/update/(?P<pk>[0-9]+)/$',views.CrewManagementCompanyUpdateView.as_view(),name='crew_management_company_update'),
url(r'^crew_management_company/delete/(?P<pk>[0-9]+)/$',views.CrewManagementCompanyDeleteView.as_view(),name='crew_management_company_delete'),
]


#Technical management urls
urlpatterns +=[
url(r'^technical_management_company/list/$',views.TechnicalManagementCompanyIndexView.as_view(),name='technical_management_list'),     
url(r'^technical_management_company/create/$',views.TechnicalManagementCompanyCreateView.as_view(),name='technical_management_create'),
url(r'^technical_management_company/update/(?P<pk>[0-9]+)/$',views.TechnicalManagementCompanyUpdateView.as_view(),name='technical_management_update'),
url(r'^technical_management_company/delete/(?P<pk>[0-9]+)/$',views.TechnicalManagementCompanyDeleteView.as_view(),name='technical_management_delete'),
]


#Operations management company urls

urlpatterns +=[
url(r'^operations_management_company/list/$',views.OperationsManagementCompanyIndexView.as_view(),name='operations_management_list'),     
url(r'^operations_management_company/create/$',views.OperationsManagementCompanyCreateView.as_view(),name='operations_management_create'),
url(r'^operations_management_company/update/(?P<pk>[0-9]+)/$',views.OperationsManagementCompanyUpdateView.as_view(),name='operations_management_update'),
url(r'^operations_management_company/delete/(?P<pk>[0-9]+)/$',views.OperationsManagementCompanyDeleteView.as_view(),name='operations_management_delete'),
]

#Safety Management Company urls

urlpatterns +=[
url(r'^safety_management_company/list/$',views.SafetyManagementCompanyIndexView.as_view(),name='safety_management_list'),     
url(r'^safety_management_company/create/$',views.SafetyManagementCompanyCreateView.as_view(),name='safety_management_create'),
url(r'^safety_management_company/update/(?P<pk>[0-9]+)/$',views.SafetyManagementCompanyUpdateView.as_view(),name='safety_management_update'),
url(r'^safety_management_company/delete/(?P<pk>[0-9]+)/$',views.SafetyManagementCompanyDeleteView.as_view(),name='safety_management_delete'),
]

#Vessel Owners urls

urlpatterns +=[
url(r'^owner/list/$',views.OwnerIndexView.as_view(),name='owner_list'),     
url(r'^owner/create/$',views.OwnerCreateView.as_view(),name='owner_create'),
url(r'^owner/update/(?P<pk>[0-9]+)/$',views.OwnerUpdateView.as_view(),name='owner_update'),
url(r'^owner/delete/(?P<pk>[0-9]+)/$',views.OwnerDeleteView.as_view(),name='owner_delete'),
]


#vessel urls
urlpatterns +=[
url(r'^vessel/list/$',views.VesselIndexView.as_view(),name='vessel_list'),
url(r'^vessel/managed/list/$',views.ManagedVesselIndexView.as_view(),name='vessel_managed_list'),      
url(r'^vessel/create/$',views.VesselCreateView.as_view(),name='vessel_create'),
url(r'^vessel/update/(?P<pk>[0-9]+)/$',views.VesselUpdateView.as_view(),name='vessel_update'),
url(r'^vessel/delete/(?P<pk>[0-9]+)/$',views.VesselDeleteView.as_view(),name='vessel_delete'),
]

#NRI urls
urlpatterns +=[
url(r'^person/nri/(?P<pk>[0-9]+)/$',views.personNriDetail,name='person_nri'),
url(r'^person/nri/(?P<pk>[0-9]+)/(?P<finyr>\d{4,4}-\d{4,4})/$',views.personNriShipList,name='person_nri_seatime' ),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^temp/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]   


