from django.db import models
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.contrib.auth.models import User, Permission
from django.db.models import Max
from crew.nritime import FinancialYear, NriTime, SeaTime, join_nri_list, print_nri




# Create your models here.

YESNO_CHOICES=(('Y','YES'),('N','NO'))

class Departments(models.Model):
     department_type=models.CharField(max_length=200)
     department_email=models.EmailField(blank=True,null=True)

     def __str__(self):
        return self.department_type
     def get_absolute_url(self):
        return reverse('crew:department_type_list')   

class CrewManagementCompany(models.Model): 
    name=models.CharField(max_length=200)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=200,blank=True)
    department_type=models.ManyToManyField(Departments, help_text="Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple")
    address=models.TextField(blank=True)

    def __str__(self):
        return self.name

class TechnicalManagementCompany(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=200,blank=True)
    department_type=models.ManyToManyField(Departments,  help_text="Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple")
    address=models.TextField(blank=True)

    def __str__(self):
        return self.name

class OperationsManagementCompany(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=200,blank=True)
    department_type=models.ManyToManyField(Departments, help_text="Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple")
    address=models.TextField(blank=True)

    def __str__(self):
        return self.name

class SafetyManagementCompany(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=200,blank=True)
    department_type=models.ManyToManyField(Departments, help_text="Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple")
    address=models.TextField(blank=True)

    def __str__(self):
        return self.name        

class Owner(models.Model):
    name=models.CharField(max_length=200)
    imo_no=models.IntegerField(null=True,blank=True)
    email=models.EmailField(blank=True)
    address=models.TextField(blank=True)

    def __str__(self):
        return self.name

class VesselType(models.Model):
    vessel_type=models.CharField(max_length=200)

    def __str__(self):
        return self.vessel_type
    
    

class Vessels(models.Model):
    MANAGED_CHOICES=(('Y','YES'),('N','NO'))
    vessel_type=models.ForeignKey(VesselType)
    name=models.CharField(max_length=200,unique=True)
    flag=models.CharField(max_length=200)
    port_of_registery=models.CharField(max_length=200)
    imo_no=models.IntegerField(unique=True)
    official_no=models.IntegerField(null=True,blank=True,unique=True)
    email=models.EmailField(blank=True)
    kwh=models.CharField(max_length=100,blank=True)
    bhp=models.IntegerField(blank=True,null=True)
    rpm=models.IntegerField(null=True,blank=True)
    deadweight=models.CharField(max_length=100,blank=True)
    net_tonnage=models.IntegerField(null=True)
    gross_tonnage=models.IntegerField(null=True)
    owner=models.ForeignKey(Owner,blank=True,null=True)
    crew_management=models.ForeignKey(CrewManagementCompany,blank=True,null=True)
    operations_management=models.ForeignKey(OperationsManagementCompany,blank=True,null=True)
    safety_management=models.ForeignKey(SafetyManagementCompany,blank=True,null=True)
    technical_management=models.ForeignKey(TechnicalManagementCompany,blank=True,null=True)
    managed=models.CharField(max_length=10,choices=MANAGED_CHOICES)
    
    
    def crewlist(self):
         return 'crew list'

    def contract_status(self):
         return 'contract status'

    def __str__(self):
        return self.name


     
class Rank(models.Model):
      rank_name=models.CharField(max_length=100,unique=True)
      rank_short_name=models.CharField(max_length=200,blank=True,unique=True)
      rank_department=models.ForeignKey(Departments)
      display_rank_priority=models.IntegerField(unique=True)

      def __str__(self):
        return self.rank_name
      
      def get_absolute_url(self):
        return reverse('crew:rank_type_list')      

class WageScale(models.Model):
      rank=models.ForeignKey(Rank)
      level=models.IntegerField(unique=True)

      def __str__(self):
         return 'Rank %s Level %d' % (self.rank,self.level)
        

class Person(models.Model):
    GENDER_CHOICES=(('Male','Male'),('Female','Female'),('Others','Others'))
    key_number=models.CharField("Unique Company No",max_length=100,unique=True)  
    rank=models.ForeignKey(Rank) 
    salutation=models.CharField("Salutation",max_length=10)
    first_name=models.CharField("First Name",max_length=200)
    last_name=models.CharField("Last Name",max_length=200)
    gender=models.CharField("Gender",max_length=200,choices=GENDER_CHOICES)
    dob=models.DateField("Date Of Birth",help_text="yyy-mm-dd")
    place_of_birth=models.CharField("Place of Birth",max_length=200)
    country_of_birth=models.CharField("Country Of Birth",max_length=200)
    nationality=models.CharField("Nationality",max_length=200)
    email=models.EmailField("Email",unique=True)
    photo=models.ImageField("Profile Photo",upload_to='crew_photos',null=True,blank=True)
    address=models.TextField("Residence Address",blank=True)
    resume=models.FileField("Resume",upload_to='crew_resume',null=True,blank=True)
    date_joined_company=models.DateField("Date Join Organisation",null=True,blank=True,help_text="yyy-mm-dd")
    user=models.ForeignKey(User,blank=True)
    incompatible_with=models.ManyToManyField('self',blank=True, help_text="""<p class="help">Hold down Control, or Command on a Mac, 
                                                to select more than one. Hold down "Control", or "Command" on a Mac, to select more than one.</p>""")
    

    class Meta:
        unique_together=(('first_name','last_name'),)  
       
                       
    def __str__(self):
        return '%s %s' % (self.first_name,self.last_name)

    def get_absolute_url(self):
        return reverse('crew:person_detail', args=[self.id]) 
    
    @property
    def total_seatime(self):
        item=relativedelta()
        st=self.seatime_set.all()
        for obj in st:
                item+=obj.seatime()
        return item
    
    @property
    def seatime_present_rank(self):
        item=relativedelta()
        st=self.seatime_set.all().filter(rank=self.rank)
        for obj in st:
            item+=obj.seatime()
        return item

    @property
    def seatime_tankers(self):
        item=relativedelta()
        st=self.seatime_set.all().filter(vessel_name__vessel_type__vessel_type__contains='tanker')
        for obj in st:
            item+=obj.seatime()
        return item
    
    @property
    def time_with_operator(self):
        today=datetime.today()
        return relativedelta(today,self.date_joined_company)   
    
    @property    
    def vacation(self):
        value=True
        seatimes=self.seatime_set.all()
        if seatimes.count() == 0:
            value=True
            return value
        else :    
            for seatime in seatimes:
                if seatime.date_signed_off is None :
                    value=False
        return value        
     
    @property
    def vacation_since(self):
        '''
        If person is on vacation returns the last sign off date, provided sea
        time is entered.
        If No seatime is entered and person is on vacation, returns the date the person joined the company
        else if no date joined company is entered, returns  datetime.min i.e. datetime.datetime(1, 1, 1, 0, 0)
        '''
        if self.vacation is True:  #checks if person is on vacation
            seatimes=self.seatime_set.all()  #if person is on vacation checks the seatime entered
            if seatimes.count() > 0:         # if person has any seatime 
                 obj=seatimes.aggregate(Max('date_signed_off'))  # find the latest date signed off
                 return obj['date_signed_off__max']         # return the latest date signed off
            else :  
                if self.date_joined_company is not None:    #if person is a new seafarer and has not yet joined a vessel, but is on vacation
                    return self.date_joined_company         # returns the date joined company, if entered
                else : 
                    return datetime.min                     # if no date of joining is entered returns the min value of datetime obj.
        else :
            return None                                     # if person is not on vacation return None.
    
    @property 
    def vacation_time(self):
        '''
        Gives the time elapsed since the last sign off date or date joined company for new joiners, or since datetime.min and today 
        in years months and days.
        '''
        if self.vacation is True:
            today=datetime.today()
            return relativedelta(today,self.vacation_since)
                

    #calculate vacation time 

    #calculate time required for promotion

    #check for superior certificate

    #check time to complete nri

 

class Contract(models.Model):
      date_started=models.DateField("Date Contract Started",help_text="yyy-mm-dd")
      date_expired=models.DateField("Date Contract Ends",help_text="yyy-mm-dd")
      vessel=models.ForeignKey(Vessels)
      person=models.ForeignKey(Person)
      rank=models.ForeignKey(Rank)
      wage_scale=models.ForeignKey(WageScale)

      class Meta:
         unique_together=(('date_started','date_expired','person'),('date_started','person'),('date_expired','person')) 

      def __str__(self):
         return '%d - %s - %s' % (self.id ,self.vessel,self.person)

      def contract_duration(self):
         return relativedelta(self.date_expired,self.date_started)

       

class Seatime(models.Model):
      date_signed_on=models.DateField("Date Signed On",help_text="yyy-mm-dd")
      date_signed_off=models.DateField("Date Signed Off",blank=True,null=True,help_text="yyy-mm-dd")
      vessel_name=models.ForeignKey(Vessels)
      person=models.ForeignKey(Person)
      rank=models.ForeignKey(Rank)

      def __str__(self):
        return 'Signed on %s - Signed off %s - Person %s - Vessel %s ' % (self.date_signed_on,self.date_signed_off,self.person,self.vessel_name)

      def seatime(self):
        today=datetime.today()
        if self.date_signed_off :
            return relativedelta(self.date_signed_off,self.date_signed_on)
        else :    
            return relativedelta(today,self.date_signed_on)
          
       
      def nrt(self):
           return SeaTime(self.date_signed_on, self.date_signed_off)


      class Meta:
         unique_together=(('date_signed_on','date_signed_off','person') ,('date_signed_on','person'),('date_signed_off','person'), )

class CrewCertificateList(models.Model):
      CERT_PAYMENT_CHOICES=(('CREW','CREW'),('COMPANY','COMPANY'))
      certificate_name=models.CharField("Certificate Name",max_length=200,unique=True)
      national_cert=models.CharField("Govt Issued",max_length=100,choices=YESNO_CHOICES)
      flag_cert=models.CharField("Flag Issued",max_length=100,choices=YESNO_CHOICES)
      company_required=models.CharField("Company Course",max_length=100,choices=YESNO_CHOICES)
      renewal_required=models.CharField("Renewal Required",max_length=100,choices=YESNO_CHOICES)
      required_for_ranks=models.ManyToManyField(Rank,help_text="Hold down Control, or Command on a Mac, to select more than one.")
      paid_for_by=models.CharField("Paid By",max_length=200,choices=CERT_PAYMENT_CHOICES)
      reminder_required=models.CharField("Reminder Required",max_length=10,choices=YESNO_CHOICES)
             
      def __str__(self):
        return " %s " % (self.certificate_name) 


class CrewCertificates(models.Model):
      person=models.ForeignKey(Person)
      certificate=models.ForeignKey(CrewCertificateList)
      date_issued=models.DateField(help_text="yyy-mm-dd")
      date_expiry=models.DateField(null=True,blank=True,help_text="yyy-mm-dd")
      institute_name=models.CharField(max_length=200,blank=True)
      issued_place=models.CharField(max_length=200,blank=True)
      certificate_no=models.CharField(max_length=200,blank=True)
      certificate_file=models.FileField(upload_to='crew_certificates',null=True,blank=True)


      def __str__(self):
        return " %s " % (self.certificate.certificate_name)

      def  expired(self):
          if self.date_expiry <  self.date_expiry.today() :
              return True
          else :
              return False      
    #add unique_together    

class GeneralSettings(models.Model):
      financial_year_start=models.DateField(help_text='Date financial year starts yyy-mm-dd')
      financial_year_ends=models.DateField(help_text='Date financial year ends yyy-mm-dd')

      def __str__(self):
        return " %s " % 'general settings'





     
    











     
