import os
os.chdir('/Users/keeganpatrao/Desktop/Programming/python/django_new/vessels')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vessels.settings")
import django
django.setup()
from crew.models import *

vessel_id=3

v=Vessels.objects.get(id=int(vessel_id)) # Gets all objects of a particular vessel.
s=v.seatime_set.all().filter(date_signed_off__isnull=True) # Filters all persons on board who
# have not signed off
person_list=[] # Creats a list to store all persons on board  
for p in s:
    person_list.append(p.person_id)

crew_details={'first_name':'','last_name':'','rank':'','date_joined':'','passport_no':'','passport_issued':'','passport_exp':''}   
crew_list=[]
for person_id in person_list:
    print("Start of loop\n")
    print(crew_list)
    print(crew_details)
    print("Populated crew list and crew details \n")
    person=Person.objects.get(id=person_id)
    crew_details['first_name']=person.first_name
    print(crew_details)
    print(crew_list)
    crew_details['last_name']=person.last_name
    print(crew_details)
    print(crew_list)
    crew_details['rank']=person.rank.rank_name
    print(crew_details)
    print(crew_list)
    st=Seatime.objects.filter(person=person.id).filter(vessel_name=vessel_id).filter(date_signed_off__isnull=True)
    st=st[0]
    crew_details['date_joined']=st.date_signed_on
    print(crew_details)
    print(crew_list)
    pcr=person.crewcertificates_set.all().filter(certificate__certificate_name__icontains='passport')
    for item in pcr:
        crew_details['passport_no']=item.certificate_no
        print(crew_details)
        print(crew_list)
        crew_details['passport_issued']=item.date_issued
        print(crew_details)
        print(crew_list)
        crew_details['passport_exp']=item.date_expiry
        print(crew_details)
        print(crew_list)
    crew_list.append(crew_details)
    print(" End of loop \n")
    print(crew_list)
    print(crew_details)
    crew_details={'first_name':'','last_name':'','rank':'','date_joined':'','passport_no':'','passport_issued':'','passport_exp':''}
