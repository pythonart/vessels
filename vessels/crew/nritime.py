from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date

class FinancialYear:
    '''
    Financial Year Class Instance,
    finYrStart is a datetime object for the start of the finanacial year e.g 01-04-2017
    finYrEnd is a datetime object for the end of the financial year e.g 31-03-2018
    finYrName is the Name of the financial yr representend as a string.
    '''
    finYrStart=None
    finYrEnd=None
    finYrName=None
    
    def __init__(self,start=datetime(2017,4,1),end=datetime(2018,3,31)):
        self.finYrStart=start
        self.finYrEnd=end
        self.finYrName=self.getName()

    def getFinancialYear(self,inpdate,yrStartDate=1,yrStartMonth=4,yrEndDate=31,yrEndMonth=3):
        '''
        getFinancialYear returns are financial year object for a input date
        inpdate is a datetime object
        yrStartDate is the date the financial year started
        yrStartMonth is the Month the financial year starts
        '''
        if inpdate !=None and inpdate.month >=4:
            self.finYrStart=datetime(inpdate.year,yrStartMonth,yrStartDate)
            self.finYrEnd=datetime(inpdate.year+1,yrEndMonth,yrEndDate)
            self.finYrName=self.getName()
        else:
            self.finYrStart=datetime(inpdate.year-1,yrStartMonth,yrStartDate)
            self.finYrEnd=datetime(inpdate.year,yrEndMonth,yrEndDate)
            self.finYrName=self.getName()
        return self        

    def getName(self):
        return str(self.finYrStart.year)+'-'+str(self.finYrEnd.year)

    def nextFinYr(self):
        '''
        Returns the next consecutive financial year for the present financial year instance.
        Can be used for Iteration.
        '''
        next_start_year=self.finYrStart.year+1
        next_end_year=self.finYrEnd.year+1
        start_date=datetime(next_start_year,self.finYrStart.month,self.finYrStart.day)
        end_date=datetime(next_end_year,self.finYrEnd.month,self.finYrEnd.day)
        next_fin_yr=FinancialYear(start_date,end_date)
        return next_fin_yr
    

    def __eq__(self,other):
        '''
        Check if two financial years are the same.
        '''
        a=self.__dict__
        b=other.__dict__
        if a==b:
            return True
        else:
            return False

    def __lt__(self,other):
        return self.finYrStart < other.finYrStart     

    def __gt__(self,other):
        return self.finYrStart > other.finYrStart           

    def __str__(self):
         return self.getName()
        
        
class NriTime:
    '''
    NriTime Class has two properties. nriDays (which is the number of days a person has spent abroad, qualifying for Non Resident Indian time)
    and yr. Which is a FinancialYear class instance for which the person spent time abroad.
    '''
    nriDays=None
    yr=None

    def __init__(self,nridays,finYr=FinancialYear()):
        self.nriDays= nridays
        self.yr     = finYr
        

    def add_days(self,nriobj):
        nriobj=nriobj
        if self.finYrStart==nriobj.finYrStart and self.finYrEnd==nriobj.finYrEnd:
            self.nriDays=self.nriDays+nriobj.nriDays
        return self

    
    def daysToCompleteNri(self,requiredDays=relativedelta(days=183)):
        requiredDays=requiredDays
        dtc=requiredDays-self.nriDays
        #convert object to days only. As when NRI is complete when subtracting
        #relativedelta objcts relativedelta(days=183) - relativedelta(month=6 days=40)
        #returns relativedelta( months=-6 , days 143) which is of no use to us.
        dtcn=dtc.years*365+dtc.months*30+dtc.days
        if dtcn < 0:
            return None
        else:
            return relativedelta(days=dtcn)
       
    def departByForNRI(self):
        if self.daysToCompleteNri() == None:
             return None
        else:
            return self.yr.finYrEnd - self.daysToCompleteNri() 

    def current(self):
        a=FinancialYear()
        a.getFinancialYear(datetime.today())
        if self.yr==a:
            return True
        else :
            return False 
               
class SeaTime:
    '''
    SeaTime class takes date signed onto a vessel and date signed off and calculates a nriList property for the period sailed.
    calcNriTime populates nriList property which contains a list of nriTime instances for the Seatime.
    '''
    son=None
    soff=None
    nriList=[]

    def __init__(self,date_on,date_off):
        self.son=date_on
        if date_off is None:
            self.soff=date.today()
        else :
            self.soff=date_off 
        fson=FinancialYear()
        self.fson=fson.getFinancialYear(self.son)
        fsoff=FinancialYear()
        self.fsoff=fsoff.getFinancialYear(self.soff)
        self.nrilist=self.calcNriTime()

    def calcNriTime(self):
        self.nriList=[]
        if self.fson == self.fsoff:
            days=relativedelta(self.soff,self.son)
            nri=NriTime(days,finYr=self.fsoff)
            self.nriList.append(nri)
            return self.nriList
        else:
            sondays=relativedelta(self.fson.finYrEnd,self.son)
            nri=NriTime(sondays,finYr=self.fson)
            self.nriList.append(nri)
            soffdays=relativedelta(self.soff, self.fsoff.finYrStart)
            nri=NriTime(soffdays,finYr=self.fsoff)
            self.nriList.append(nri)
            next=self.fson.nextFinYr()
            while next !=self.fsoff:
                days=relativedelta(next.finYrEnd,next.finYrStart)
                nri=NriTime(days,next)
                self.nriList.append(nri)
                next=next.nextFinYr()            
            return self.nriList
    
    def __eq__(self,other):
        a=self.__dict__
        b=other.__dict__
        if a==b:
            return True
        else:
            return False

def print_nri(new_nri_list):
    new_nri_list=new_nri_list
    print("I am in Print Nri\n")
    for nriitem in new_nri_list:
        print(nriitem.nriDays)
        print(nriitem.yr.finYrName)

        
def join_nri_list(nriList1,nriList2):
    #Bug- Need to change join_nri to accept NRI Object lists instead of seatime objects.
    new_nri_list=[]
    for item in nriList1:
        equal=False
        print( "In nriList1 List\n")
        print("Item here is",item.yr.finYrName,"\n")
        for obj in nriList2:
            print("In nriList2 \n")
            if item.yr==obj.yr:
                print( item.yr.finYrName,"in nriList1 found Equal to  ",obj.yr.finYrName,"\n")
                days=item.nriDays+obj.nriDays
                new_nri_list.append(NriTime(days,item.yr))
                nriList2.pop(nriList2.index(obj))
                print_nri(new_nri_list)
                equal=True
                continue
            else :
                print(item.yr.finYrName,"in nriList1  Found NOT Equal to ",obj.yr.finYrName,"\n")
        if equal==True:
            pass
        else :
            print(item.yr.finYrName," Does not match any item nriList2 \n")
            days=item.nriDays
            new_nri_list.append(NriTime(days,item.yr))
            print_nri(new_nri_list)
            
    print("Completed Check, Now appending remaining objects from nriList2 to nriList1 \n")
    new_nri_list=new_nri_list+nriList2
    print_nri(new_nri_list)
    return new_nri_list


    
    
            
            
        
    
    
    

