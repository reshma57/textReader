import MySQLdb
import time;
from mod_python import Session
from config_path import data
import student
ff=5
Rollno=0

def addr_split(nn):
               cnt=0
               cntt=0
          
               nn=list(nn)
               for i in range(0,len(nn)):
                   if nn[i]==',':
                        nn[i]='</br>';
                        cntt=1
                   elif nn[i]==' ':
                       cntt+=1;
                       if cntt%3==0:
                           nn[i]='</br>';


               return nn;
def index(req):
         session = Session.Session(req);
         global Rollno
         Rollno=session['rno']
         session.save()
         session.cleanup()
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess" )
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         #req.content_type="text/html"
         #req.write(str(studAct))

         ss=""" select rollNumber from internationalStudentInformationDomain;"""
         cursor.execute(ss)
         rnoarray=cursor.fetchall()
         rno=map(lambda x:x[0],rnoarray)
         if str(Rollno)in rno:
            fp=open(data.path+"/project_data/NewAppInter.html","r")
            ap=fp.read()
            return ap
         else:
            fp=open(data.path+"/project_data/Newapplication.html","r")
            ap=fp.read()
            return ap;

def for_bonafied(req):
         global ff
         ff=0
         flg=0
         info=req.form
         pur=info['purp']
         session = Session.Session(req);
         global Rollno
         Rollno=session['rno']
         ip=session['ipaddr']
         session.save()
         session.cleanup()
         #return pur
         doc='';
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase")
         info1=req.form
         
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         
         ss="""select applicationPurpose from applicationProcess.applicationForm where appId="APBN" and rollnumber=%s;"""%(Rollno)
         cursor.execute(ss)
         val=cursor.fetchall()
         p=val
         pur=info1['purp']
         
         if(len(p)!=0):
            
            ss= """update applicationProcess.applicationForm set applicationPurpose=%s where appId="APBN" and rollnumber=%s;"""
            cursor.execute(ss,(pur,Rollno)) 
            db.commit()
         else:
            ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,"applicationForm",%s,"APBN,"%s);"""
            cursor.execute(ss,(Rollno,ip,pur))
       	    db.commit();

               
           
         q4 = """select "%s" in (select rollNumber from applicationProcess.auxApplicationForm where appId='APBN');"""%(Rollno)
         cursor.execute(q4)
         res = cursor.fetchall()
         
         if res[0][0]!=0:
	     q5="""select msg from userInputDatabase.outputErrorMsgs where requestId in(select requestId from applicationProcess.applicationForm where rollNumber in(select rollNumber from applicationProcess.auxApplicationForm where rollNumber=%s and appId="APBN"));""" %(Rollno)      
	     cursor.execute(q5)
             msg = cursor.fetchall()[0][0]
             return """</form><html><b>%s</b><form value="form" action="../st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(msg)

         
         
       	 tabid="ApplicationRequests"
         
         ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
         cursor.execute(ss,(Rollno,'APBN'+'%'))
         val=cursor.fetchall()
         
         states=('','')      
         if len(val)==0:
             flg=1
             ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,start,ApplicationInitiated,Bonafide Certificate,apply for Bonafide Certificate");"""

             cursor.execute(ss,(Rollno,tabid,ip))
             db.commit();

         else:
           states=val[len(val)-1]
       
           
	 db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess" )
         # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         
         if states==('start','ApplicationInitiated') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,ApplicationInitiated,ApplicationFormPartiallyFilled,Bonafide Certificate,apply for Bonafide Certificate");"""
 
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();

         if states==('ApplicationInitiated','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,ApplicationInitiated,ApplicationFormFilled,Bonafide Certificate,apply for Bonafide Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
         


         fp=open(data.path+"/project_data/bonafied.html","r")
         fp=(fp.read())
         
 
         if states==('ApplicationInitiated','ApplicationFormFilled') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,ApplicationFormPartiallyFilled,ApplicationFormPartiallyFilled,Bonafide Certificate,apply for Bonafide Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();

         if states==('ApplicationFormPartiallyFilled','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,ApplicationFormPartiallyFilled,ApplicationFormFilled,Bonafide Certificate,apply for Bonafide Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();

         
         if states==('ApplicationFormPartiallyFilled','ApplicationFormFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,ApplicationFormFilled,ApplicationFormPartiallyFilled,Bonafide Certificate,apply for Bonafide Certificate");""" 

           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
         
        
         
         
         
	 ss="""select * from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()
         
         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
             hh="his"
         else:
             gen='Miss.'
             hh="her"

         y="""select year from courseSemesterDomain where courseId = (select courseId from studentDetailsDomain where rollNumber=%s) and semId = (select semId from studentDetailsDomain where rollNumber=%s);"""
         cursor.execute(y,(Rollno,Rollno))
         val1=cursor.fetchall()
         yy= map(lambda x:x[0],val1)
         d=time.strftime("%d/%m/%Y")
         year=int(d.split('/')[2])
         p="""select applicationPurpose from applicationForm where appId='APBN' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)
         val2=cursor.fetchall()
         purpose= map(lambda x:x[0],val2)
         
         dt="""select  dateOfBirth from studentDetailsDomain where rollNumber=%s;"""%(Rollno)
         cursor.execute(dt)
         valdt=cursor.fetchall()    
         bdt= map(lambda x:x[0],valdt)
         dt=str(bdt[0]).split('-')
         dt.reverse()
         dt='-'.join(dt)              
    	 
         doc+="""<h1> Bonafied Certificate:<br><br><br> <h1></html>"""    
         #doc+=fp%(val[0][4]+" "+val[0][5]+" "+val[0][6],int(val[0][0]),val[0][1],yy,year,year+1,purpose,val[0][10],val[0][11],val[0][12],val[0][8]);
         doc+=fp%(gen,val[0][4]+" "+val[0][5]+" "+val[0][6],int(val[0][0]),val[0][1],yy[0],year,year+1,hh,purpose[0],val[0][12],val[0][13],val[0][14],dt);
    
         if(pur==""):
             doc+="""</form><head><body><form value="form" action="print_Application" method="post"><input type=\"submit\" value=\"Final Submit\"><span style="margin-left:0.5em;"></span><input type=hidden name=\"ff\" value=\"0\"></form><form value="form" action="../read_pur.py" method="post"><input type=\"submit\" value=\"Save For Later\"><span style="margin-left:0.5em;"></span></form><form value="form" action="../st_loh.py" method="post"><input type=\"submit\" value=\"Cancel\"></form><form value="form" action="../delete.py" method="post"><input type=\"submit\" value=\"Delete\"><input type="hidden" name="appid" value="APBN"></form></body></head></html>"""
             return doc
             
         if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APBN,ApplicationFormFilled,ApplicationFormFilled,Bonafide Certificate,apply for Bonafide Certificate");"""

           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();         
  
     
         doc+="""</form><head><body><form value="form" action="print_Application" method="post"><input type=\"submit\" value=\"Final Submit\"><span style="margin-left:0.5em;"></span><input type=hidden name=\"ff\" value=\"0\"></form><form value="form" action="../read_pur.py" method="post"><input type=\"submit\" value=\"Save For Later\"><span style="margin-left:0.5em;"></span></form><form value="form" action="../st_loh.py" method="post"><input type=\"submit\" value=\"Cancel\"><span style="margin-left:0.5em;"></span></form><form value="form" action="../delete.py" method="post"><input type=\"submit\" value=\"Delete\"><input type="hidden" name="appid" value="APBN"></form></body></head></html>"""
         return doc

def for_nodues(req):
         global ff
         ff=1
         flg=0
         doc='';
         session = Session.Session(req);
         global Rollno
         Rollno=session['rno']
         ip=session['ipaddr']
         session.save()
         session.cleanup()
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase" )
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         
         ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,"applicationForm",%s,"APND");"""
      
         cursor.execute(ss,(Rollno,ip))
       	 db.commit();
  

         q4 = """select "%s" in (select rollNumber from applicationProcess.auxApplicationForm where appId='APND');"""%(Rollno)
         cursor.execute(q4)
         res = cursor.fetchall()
         
         if res[0][0]!=0:
	     q5="""select msg from userInputDatabase.outputErrorMsgs where requestId in(select requestId from applicationProcess.applicationForm where rollNumber in(select rollNumber from applicationProcess.auxApplicationForm where rollNumber=%s and appId="APND"));""" %(Rollno)      
	     cursor.execute(q5)
             msg = cursor.fetchall()[0][0]
             return """</form><html><b>%s</b> <form value="form" action="../st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(msg)



       	 tabid="ApplicationRequests"

         ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
         cursor.execute(ss,(Rollno,'APND'+'%'))
         val=cursor.fetchall()
         states=('','')      
         if len(val)==0:
             flg=1
             ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params)    values (NOW(),"insert",%s,%s,%s,"APND,start,ApplicationInitiated,No Dues Certificate,apply for No Dues Certificate");"""

             cursor.execute(ss,(Rollno,tabid,ip))
             db.commit();

         else:
           states=val[len(val)-1]


         
	 db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess" )
         # prepare a cursor object using cursor() method
    	 cursor = db.cursor()

         if states==('start','ApplicationInitiated') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APND,ApplicationInitiated,ApplicationFormPartiallyFilled,No Dues Certificate,apply for No Dues Certificate");"""
 
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();




         if states==('ApplicationInitiated','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APND,ApplicationInitiated,ApplicationFormFilled,No Dues Certificate,apply for No Dues Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();

         #disconnect from server
    	 #db.close()


         fp=open(data.path+"/project_data/no_dues.html","r")
         fp=(fp.read());


         if states==('ApplicationInitiated','ApplicationFormFilled') or flg==1:
	   flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APND,ApplicationFormPartiallyFilled,ApplicationFormPartiallyFilled,No Dues Certificate,apply for No Dues Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();


         if states==('ApplicationFormPartiallyFilled','ApplicationFormPartiallyFilled') or flg==1:
	   flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APND,ApplicationFormPartiallyFilled,ApplicationFormFilled,No Dues Certificate,apply for No Dues Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();


         if states==('ApplicationFormPartiallyFilled','ApplicationFormFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APND,ApplicationFormFilled,ApplicationFormPartiallyFilled,No Dues Certificate,apply for No Dues Certificate");""" 

           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();




         if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APND,ApplicationFormFilled,ApplicationFormFilled,No Dues Certificate,apply for No Dues Certificate");"""

           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
         
	 ss="""select * from  studentDetailsDomain where rollNumber=%s;;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()
         
       

    	
         ss="""select rollnumber from applicationProcess.studentApplicationQueue where rollnumber=%s and appId=%s;"""
         cursor.execute(ss,(Rollno,'APND'))
         val2=cursor.fetchall()
         rn= map(lambda x:x[0],val2)
         if len(rn)!=0:
             ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params)    values (NOW(),"insert",%s,%s,%s,"APND,start,ApplicationInitiated,No Dues Certificate,apply for No Dues Certificate");"""

             cursor.execute(ss,(Rollno,tabid,ip))
             db.commit();
             q4 = """select msg from userInputDatabase.outputErrorMsgs where requestId = (select requestId from userInputDatabase.inputRequests where userId=%s  order by requestId desc limit 1);"""
             cursor.execute(q4,(Rollno,))
             res = cursor.fetchall()
          
             
             return """</form><html>%s <form value="form" action="../st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(res[0])
         doc+="""<h1> NoDues Certificate:<br><br><br> <h1>"""
         

         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
             hh="his"
             on_print_gender="him"
         else:
             gen='Miss.'
             hh="her"
	     on_print_gender="her"



      
	 #year=int(str(val[0][10]).split('-')[0])
         doc+=fp%(gen,val[0][4]+" "+val[0][5]+" "+val[0][6]+" ",int(val[0][0]),val[0][1],on_print_gender,hh);
         doc+="""</form><head><body><form value="form" action="print_Application" method="post"><input type=\"submit\" value=\"Final Submit\"><span style="margin-left:0.5em;"></span><input type=hidden name=\"ff\" value=\"1\"></form><form value="form" action="../st_loh.py" method="post"><input type=\"submit\" value=\"Cancel\"></form><form value="form" action="../delete.py" method="post"><input type=\"submit\" value=\"Delete\"><input type="hidden" name="appid" value="APND"></form></body></head></html>"""
	 return doc

def for_feesstructure(req):
         global ff
         ff=2
         flg=0
         doc='';
         session = Session.Session(req);
         global Rollno
         Rollno=session['rno']
         ip=session['ipaddr']
         session.save()
         session.cleanup()
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase" )
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         info1=req.form
         addbank=info1['bname']
         add=info1['addr'];
         add=addbank+","+add;
         
         ss="""select applicationPurpose from applicationProcess.applicationForm where appId="APFS" and rollnumber=%s;"""%(Rollno)
         cursor.execute(ss)
         val=cursor.fetchall()
         p=val
        
         if(len(p)!=0):
            
            ss= """update applicationProcess.applicationForm set applicationPurpose=%s where appId="APFS" and rollnumber=%s;"""
            cursor.execute(ss,(add,Rollno)) 
            db.commit()
         else:
            
            ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,"applicationForm",%s,"APFS,"%s);"""
            cursor.execute(ss,(Rollno,ip,add))
       	    db.commit();   

         q4 = """select "%s" in (select rollNumber from applicationProcess.auxApplicationForm where appId='APFS');"""%(Rollno)
         cursor.execute(q4)
         res = cursor.fetchall()
         
         if res[0][0]!=0:
	     q5="""select msg from userInputDatabase.outputErrorMsgs where requestId in(select requestId from applicationProcess.applicationForm where rollNumber in(select rollNumber from applicationProcess.auxApplicationForm where rollNumber=%s and appId="APFS"));""" %(Rollno)      
	     cursor.execute(q5)
             msg = cursor.fetchall()[0][0]
             return """</form><html><b>%s</b><form value="form" action="../st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(msg)
         
        
       	 tabid="ApplicationRequests"
          
         ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
         cursor.execute(ss,(Rollno,'APFS'+'%'))
         val=cursor.fetchall()
         states=('','')      
         if len(val)==0:
             flg=1
             ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params)    values (NOW(),"insert",%s,%s,%s,"APFS,start,ApplicationInitiated,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank");"""
         
             cursor.execute(ss,(Rollno,tabid,ip))
             db.commit();
             
         else:
           states=val[len(val)-1]

              
 
	 db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess" )
         # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         
         if states==('start','ApplicationInitiated') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APFS,ApplicationInitiated,ApplicationFormPartiallyFilled,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank");"""
 
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
        


         
         if states==('ApplicationInitiated','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APFS,ApplicationInitiated,ApplicationFormFilled,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
           
         
         #disconnect from server
    	 #db.close()


         fp=open(data.path+"/project_data/fees_structure.html","r")
         fp1=open(data.path+"/project_data/feestructureformca.html","r")
         fp1=fp1.read()
         fp=(fp.read());



         if states==('ApplicationInitiated','ApplicationFormFilled') or flg==1:
	   flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APFS,ApplicationFormPartiallyFilled,ApplicationFormPartiallyFilled,Fee Structure Certificate For Bank,apply for Feees Structure Application");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
           
          
         if states==('ApplicationFormPartiallyFilled','ApplicationFormPartiallyFilled') or flg==1:
	   flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APFS,ApplicationFormPartiallyFilled,ApplicationFormFilled,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();


         if states==('ApplicationFormPartiallyFilled','ApplicationFormFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APFS,ApplicationFormFilled,ApplicationFormPartiallyFilled,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank");""" 

           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();


         

        
	 ss="""select * from applicationProcess.feesStructureForm where rollNumber=%s ;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()
         p="""select applicationPurpose from applicationForm where appId='APFS' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)
         val2=cursor.fetchall()
         addr= map(lambda x:x[0],val2)
         addr=''.join(addr_split(addr[0]))
         
    	 
         doc+="""<h1> FeesStructure Certificate:<br><br><br> <h1>"""       
	 #year=int(str(val[0][10]).split('-')[0])

         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
         else:
             gen='Miss.'


         if val[0][4]=='MCA':  
           doc+=fp1%(addr,gen,val[0][1]+" "+val[0][2]+" "+val[0][3],val[0][4],val[0][6],val[1][6],val[2][6],val[3][6],val[4][6],val[5][6],val[0][7],val[1][7],val[2][7],val[3][7],val[4][7],val[5][7],val[0][8],val[1][8],val[2][8],val[3][8],val[4][8],val[5][8],val[0][9],val[1][9],val[2][9],val[3][9],val[4][9],val[5][9])
         else:
		doc+=fp%(addr,gen,val[0][1]+" "+val[0][2]+" "+val[0][3],val[0][4],val[0][6],val[1][6],val[2][6],val[3][6],val[0][7],val[1][7],val[2][7],val[3][7],val[0][8],val[1][8],val[2][8],val[3][8],val[0][9],val[1][9],val[2][9],val[3][9])


         if(add==""):
             
             return doc
             
         if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APFS,ApplicationFormFilled,ApplicationFormFilled,Fee Structure Certificate For Bank,apply for FeesStructure Application");"""
           
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();  
           

         doc+="""</form><head><body><form value="form" action="print_Application" method="post"><input type=\"submit\" value=\"Final Submit\"><span style="margin-left:0.5em;"></span><input type=hidden name=\"ff\" value=\"2\"></form><form value="form" action="../read_bank.py" method="post"><input type=\"submit\" value=\"Save For Later\"><span style="margin-left:0.5em;"></span></form><form value="form" action="../st_loh.py" method="post"><input type=\"submit\" value=\"Cancel\"></form><form value="form" action="../delete.py" method="post"><input type=\"submit\" value=\"Delete\"><input type="hidden" name="appid" value="APFS"></form></body></head></html>"""
         return doc


def for_inter_bonafied(req):
         global ff
         ff=3
         flg=0
         doc='';
         session = Session.Session(req);
         global Rollno
         Rollno=session['rno']
         ip=session['ipaddr']
         session.save()
         session.cleanup()
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase" )
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
                  
         ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,"applicationForm",%s,"APIB");""" 

         cursor.execute(ss,(Rollno,ip))
       	 db.commit();

         q4 = """select "%s" in (select rollNumber from applicationProcess.auxApplicationForm where appId='APIB');"""%(Rollno)
         cursor.execute(q4)
         res = cursor.fetchall()
         
         if res[0][0]!=0:
	     q5="""select msg from userInputDatabase.outputErrorMsgs where requestId in(select requestId from applicationProcess.applicationForm where rollNumber in(select rollNumber from applicationProcess.auxApplicationForm where rollNumber=%s and appId="APIB"));""" %(Rollno)      
	     cursor.execute(q5)
             msg = cursor.fetchall()[0][0]
             return """</form><html><b>%s</b><form value="form" action="../st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(msg)
  
   
       	 tabid="ApplicationRequests"
          
         ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
         cursor.execute(ss,(Rollno,'APIB'+'%'))
         val=cursor.fetchall()
         states=('','')      
         if len(val)==0:
             flg=1
             ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params)    values (NOW(),"insert",%s,%s,%s,"APIB,start,ApplicationInitiated,International Bonafide Certificate,apply for International Bonafide Certificate");"""
         
             cursor.execute(ss,(Rollno,tabid,ip))
             db.commit();
             
         else:
           states=val[len(val)-1]

         q4 = """select msg from userInputDatabase.outputErrorMsgs where requestId = (select requestId from userInputDatabase.inputRequests where userId=%s  order by requestId desc limit 1);"""
         cursor.execute(q4,(Rollno,))
         res = cursor.fetchall()
         if len(res)!=0:
                return """</form><html>%s <form value="form" action="../st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%("res")
         
	 db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess" )
         # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         
         if states==('start','ApplicationInitiated') or flg==1:
           flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APIB,ApplicationInitiated,ApplicationFormPartiallyFilled,International Bonafide Certificate,apply for International Bonafide Certificate");"""
 
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
        


         
         if states==('ApplicationInitiated','ApplicationFormPartiallyFilled') or flg==1:
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APIB,ApplicationInitiated,ApplicationFormFilled,International Bonafide Certificate,apply for International Bonafide Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
           flg=1
           
         
         
         
         fp=open(data.path+"/project_data/international_stud_bonafied.html","r")
         fp=(fp.read());


         if states==('ApplicationInitiated','ApplicationFormFilled') or flg==1:
	   flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APIB,ApplicationFormPartiallyFilled,ApplicationFormPartiallyFilled,International Bonafide Certificate,apply for International Bonafide Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
           
          
         if states==('ApplicationFormPartiallyFilled','ApplicationFormPartiallyFilled') or flg==1:
	   flg=1
           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APIB,ApplicationFormPartiallyFilled,ApplicationFormFilled,International Bonafide Certificate,apply for International Bonafide Certificate");"""
           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();


         if states==('ApplicationFormPartiallyFilled','ApplicationFormFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APIB,ApplicationFormFilled,ApplicationFormPartiallyFilled,International Bonafide Certificate,apply for International Bonafide Certificate");""" 

           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();


         

         if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled') or flg==1:
           flg=1
	   ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,"APIB,ApplicationFormFilled,ApplicationFormFilled,International Bonafide Certificate,apply for International Bonafide Certificate");"""

           cursor.execute(ss,(Rollno,tabid,ip))
       	   db.commit();
         
	 ss = """select * from applicationProcess.studentDetailsDomain where rollNumber=%s ;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()

         ss1 = """select * from applicationProcess.internationalStudentInformationDomain where rollNumber=%s ;"""%(Rollno)
    	 cursor.execute(ss1)
       	 val1=cursor.fetchall()
         
                   
	 

    	 '''if flg==0 and states==('ApplicationFormFilled','ApplicationSubmitted'):
            return """<html>Allready applied..! <input type=\"button\" onclick=(window.history.go(-2)) value=\"OK\"></html>"""
         '''

         ss="""select rollnumber from applicationProcess.studentApplicationQueue where rollnumber=%s and appId=%s;"""
         cursor.execute(ss,(Rollno,'APIB'))
         val2=cursor.fetchall()
         rn= map(lambda x:x[0],val2)
         if len(rn)!=0:
               ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params)    values (NOW(),"insert",%s,%s,%s,"APIB,start,ApplicationInitiated,International Bonafide Certificate,apply for International Bonafide Certificate");"""
         
               cursor.execute(ss,(Rollno,tabid,ip))
               db.commit();

 	       q4 = """select msg from userInputDatabase.outputErrorMsgs where requestId = (select requestId from userInputDatabase.inputRequests where userId=%s  order by requestId desc limit 1);"""
               cursor.execute(q4,(Rollno,))
               res = cursor.fetchall()
          
             
               return """</form><html>%s <form value="form" action="../st_loh.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(res[0])








         doc+="""<h1>International Bonafied Certificate:<br><br><br> <h1>"""       
	 
         d=time.strftime("%d/%m/%Y")

         
         doc+=fp%(val[0][4]+" "+val[0][5]+" "+val[0][6],val[0][4]+" "+val[0][5]+" "+val[0][6],val1[0][1],val1[0][2],int(val[0][9]),int(val1[0][4]),int(val1[0][7]),val1[0][5],val1[0][8],val1[0][6],val1[0][9],val1[0][10],val1[0][3],val[0][1],val[0][1],d);
         doc+="""</form><head><body><form value="form" action="print_Application" method="post"><input type=\"submit\" value=\"Final Submit\"><span style="margin-left:0.5em;"></span><input type=hidden name=\"ff\" value=\"3\"></form><form value="form" action="../st_loh.py" method="post"><input type=\"submit\" value=\"Cancel\"></form><form value="form" action="../delete.py" method="post"><input type=\"submit\" value=\"Delete\"><input type="hidden" name="appid" value="APIB"></form></body></head></html>"""
	 return doc



def print_Application(req):
           
           session = Session.Session(req);
           Rollno=session['rno']
           
           ip=session['ipaddr']
           session.save()
           session.cleanup()
           tabid="ApplicationRequests"
           db = MySQLdb.connect(
    	   host="localhost",
    	   user=data.mysql_user,
    	   passwd=data.mysql_pswd,
    	
           db="userInputDatabase" )
   	   #prepare a cursor object using cursor() method
    	   cursor = db.cursor()
           info=req.form
           ff=int(info['ff'])



           
           arrayid=["APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,apply for Bonafide Certificate","APND,ApplicationFormFilled,ApplicationSubmitted,No Dues Certificate,apply for No Dues Certificate"
,"APFS,ApplicationFormFilled,ApplicationSubmitted,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","APIB,ApplicationFormFilled,ApplicationSubmitted,International Bonafide Certificate,apply for International Bonafide Certificate","APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,apply for Bonafide Certificate"]
          
           psid=arrayid[ff]
           appid=psid.split(',')[0]
           aplydc=psid.split(',');
           aplydc=aplydc[3:]
          	
           ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
           cursor.execute(ss,(Rollno,appid+'%'))
           val=cursor.fetchall()
           
           states=val[len(val)-1]
                    

           if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled'):
           	 flg=1
	  	 ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,%s);"""

                 cursor.execute(ss,(Rollno,tabid,ip,appid+",ApplicationFormFilled,ApplicationFormFilled,"+aplydc[0]))
         	 db.commit();




           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,%s);"""
           cursor.execute(ss,(Rollno,tabid,ip,psid))
       	   db.commit();
           
           
           fp=open(data.path+"/project_data/autoclick4.html")
           fp=fp.read()   
           return fp


def print_data(req):
     session = Session.Session(req);
     Rollno=session['rno']
     ip=session['ipaddr']
     flag=1
     return for_nodues()

