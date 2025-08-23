#For assigning destination folder
import os.path

#Connecting to MYSQL for "Total" calculation
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="assist")
mycursor=mydb.cursor()

import pandas as pd
file = pd.ExcelFile("inventory.xlsx")
df1=file.parse('Sheet1')

#for scanner
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import winsound



#length
lengthd = df1.count()
lengthd = int(lengthd.ID)

#names of commodities
x1=[]
for n in range (lengthd):
    x1.append(df1.iloc[n,1])
c={}
for n in range(len(x1)):
    c[n+1] = x1[n]
    
#price of commodities
y=[]
for n in range (lengthd):
    y.append(df1.iloc[n,2])    
d={}
for n in range(len(y)):
    d[n+1] = y[n]

#Function to read QR code
def read_qr_code():
    cap = cv2.VideoCapture(0)  

    try:
        while True:
            success, frame = cap.read()
            _, frame = cap.read()
            cv2.imshow("Scanner", frame)

            # Decode QR code
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                barcode_data = obj.data.decode("utf-8")
                pts = np.array([obj.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                
                # Check if the scanned data is numeric
                if barcode_data.isnumeric() and int(barcode_data) in range(1,lengthd+1) :
                    print("Scanned Product Code:", barcode_data, ".", c[int(barcode_data)])
                    cv2.polylines(frame, [pts], True, (0, 179, 0), 2)
                    text = f"{c[int(barcode_data)]} MRP: {d[int(barcode_data)]} Rs"
                    pts2 = obj.rect
                    cv2.putText(frame, barcode_data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 179, 0), 2)
                    cv2.putText(frame, text, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 179, 0), 2)
                    
                    cv2.imshow("Scanner", frame)
                    cv2.waitKey(1)
                    winsound.Beep(3700, 400)
                    return int(barcode_data)
                                         
                else:
                    cv2.polylines(frame, [pts], True, (0, 0, 255), 2)
                    pts2 = obj.rect
                    cv2.putText(frame, barcode_data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow("Scanner", frame)

            # Limit frames processed per loop iteration
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Release the video capture when done
        cap.release()
        cv2.destroyAllWindows()



#in case if an error, it will display already used names
mycursor.execute("show databases")
databases=[]
for xyz in mycursor:
    xyz=str(xyz)
    xyz=xyz[2:-3]
    databases.append(xyz)
if "shop" in databases:
    print("_"*80)
    print("Names Used:")
    mycursor.execute("use shop;")
    mycursor.execute("show tables;")
    for v in mycursor:
        v=str(v)
        v=v.replace("zzzreport","_"*80)
        v=v.replace("zzzsale","")
        print(v[2:-3])

mycursor.execute("create database if not exists shop")
mycursor.execute("use shop")
mycursor.execute("create table if not exists zzzReport(S_no int auto_increment primary key,Name varchar(40),Wo_Discount float(9,2),Discount_Per float(6,2),Discount float(9,2),W_Discount float(9,2), UID varchar(15))")
mycursor.execute("use shop")           
mycursor.execute("show tables")
tables=[]
for xyz in mycursor:
    xyz=str(xyz)
    xyz=xyz[2:-3]
    tables.append(xyz)
if "zzzsale" in tables:
    This_is_just_a_filling_statement=1000
else:
    mycursor.execute("create table if not exists zzzSale(S_no integer(5),Name varchar(40),Number integer(10) default 0)")
    for inv_var in range(1,len(c)+1):
        mycursor.execute("insert into zzzSale(S_no,Name) values("+str(inv_var)+",'"+str(c[inv_var])+"')")
        mydb.commit()

#Creating destination folder of Invoices
us="'_'"
mycursor.execute("select concat(dayofmonth(now()),"+us+",monthname(now()),"+us+",year(now()))")
for tdate in mycursor:
    tdate=str(tdate)
    tdate=tdate[2:-3]

import os
from os import path
if path.exists("Invoices"):
    This_is_just_a_filling_statement=1000
else:
    os.mkdir("Invoices")

if path.exists("Invoices\Invoices of "+tdate):
    This_is_just_a_filling_statement=1000
else:
    os.mkdir("Invoices\Invoices of "+tdate)


#UI starts
import sys
if sys.version[0:6] =="3.11.5":
    print("","_"*79)
    print("|\t\t\tNature's Basket Herbal Store\t\t\t\t|")
    print("|\t\t\t111, New Road Ratlam\t\t\t\t\t|")
    print("|\t\t\tContact Number 1212121212\t\t\t\t|")
    print("|","_"*77,"|")    
else:
    print("","_"*79)
    print("|\t\t\t\t\t\tNature's Basket Herbal Store\t\t\t\t\t\t\t|")
    print("|\t\t\t\t\t\t111, New Road Ratlam\t\t\t\t\t\t\t\t\t|")
    print("|\t\t\t\t\t\tContact Number 1212121212\t\t\t\t\t\t\t\t|")
    print("|","_"*77,"|")

operator=input("Operator's Name:")
if operator=="":
    operator="operator1"
fd=input("Fixed Discount for all Buyers?(Y/N):")
if fd in ["y","Y","YES","Yes","yes","1"]:
    disc=float(input("Discount (%):"))

while True:
    cust=input("Customer's Name (Spaces not allowed!):")
    mycursor.execute("select now();")
    for uid in mycursor:
        uid=str(uid)
        uid=uid[19:-3]
    uid=uid.replace(", ","")

    if cust=="":
        cust=uid+"_customer"
    else:
        cust=uid+"_"+cust
    arb=int(input("Number of Unique Products:"))
    print("_"*80) 
    
    if arb<=len(c):
        mycursor.execute("insert into zzzReport (Name) values('"+cust+"');")
        mydb.commit()
        print("="*14,"Inventory:","="*14)
        for x in range (1,len(c)+1):
            print(x,".",c[x])
        print("="*40)
#Code for creating a seperate .txt file of invoice with name of customer and save it in defined folder
        space="' '"
        comma="', '"
        mycursor.execute("select concat(dayofmonth(now()),"+space+",monthname(now()),"+space+",year(now()),"+comma+",dayname(now()),"+comma+",current_time())")
        for dt in mycursor:
            dt=str(dt)
            dt=dt[2:-3]
        my_dir="Invoices\Invoices of "+tdate
        file_name=cust+".txt"
        fname=os.path.join(my_dir,file_name)
        report= open(fname,"w")
        report.write(" "+"_"*79)
        report.write("\n|\t\t\tNature's Basket Herbal Store\t\t\t\t|")
        report.write("\n|\t\t\t111, New Road Ratlam\t\t\t\t\t|")
        report.write("\n|\t\t\tContact Number 1212121212\t\t\t\t|")
        report.write("\n|"+"_"*79+"|")
        report.write("\n|Bill Number: "+uid)
        report.write("\n|"+"_"*79+"|")
        report.write("\n|\tProduct\t\t\t|Price\t\t|Quantity\t|Amount\t\t|")
        report.write("\n|"+"-"*79+"|")
        
        for a in range (1,arb+1):
            
            try:
                print("Product Code:")
                inp=read_qr_code()

            except:
                inp=int(input("Type Product Code:"))
            
            if inp==None:
                inp=int(input("Type Product Code:"))
            
            try:
                n1=int(input("Quantity:"))
            except:
                n1=1
                print(n1)
            print("-"*80)
        
            if inp==1:
                c1=(d[inp]*n1)
                f1=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c1))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c1)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f1" in locals():
                    report.write("\n"+str(f1))
                    report.write("\n|"+"-"*79+"|")
                
            elif inp==2:
                c2=(d[inp]*n1)
                f2=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c2))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c2)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f2" in locals():
                    report.write("\n"+str(f2))
                    report.write("\n|"+"-"*79+"|")
                
            elif inp==3:
                c3=(d[inp]*n1)
                f3=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c3))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c3)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f3" in locals():
                    report.write("\n"+str(f3))
                    report.write("\n|"+"-"*79+"|")
            
            elif inp==4:
                c4=(d[inp]*n1)
                f4=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c4))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c4)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f4" in locals():
                    report.write("\n"+str(f4))
                    report.write("\n|"+"-"*79+"|")
                    
            elif inp==5:
                c5=(d[inp]*n1)
                f5=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c5))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c5)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f5" in locals():
                    report.write("\n"+str(f5))
                    report.write("\n|"+"-"*79+"|")
                    
            elif inp==6:
                c6=(d[inp]*n1)
                f6=("|"+str(a)+". "+c[inp]+"\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c6))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c6)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f6" in locals():
                    report.write("\n"+str(f6))
                    report.write("\n|"+"-"*79+"|")
                    
            elif inp==7:
                c7=(d[inp]*n1)
                f7=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c7))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c7)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f7" in locals():
                    report.write("\n"+str(f7))
                    report.write("\n|"+"-"*79+"|")
                
            elif inp==8:
                c8=(d[inp]*n1)
                f8=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c8))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c8)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f8" in locals():
                    report.write("\n"+str(f8))
                    report.write("\n|"+"-"*79+"|")
                
            elif inp==9:
                c9=(d[inp]*n1)
                f9=("|"+str(a)+". "+c[inp]+"\t\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c9))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c9)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f9" in locals():
                    report.write("\n"+str(f9))
                    report.write("\n|"+"-"*79+"|")
                
            elif inp==10:
                c10=(d[inp]*n1)
                f10=("|"+str(a)+". "+c[inp]+"\t"+str(d[inp])+"\t\t"+str(n1)+"\t\t"+str(c10))
                mycursor.execute("create table if not exists "+cust+"(Product varchar(40),Number int(7),Paid int(7))")
                mycursor.execute("insert into "+cust+" values('"+c[inp]+"',"+str(n1)+","+str(c10)+");")
                mycursor.execute("update zzzSale set Number=Number+"+str(n1)+" where S_no="+str(inp))
                mydb.commit()
                if "f10" in locals():
                    report.write("\n"+str(f10))
                    report.write("\n|"+"-"*79+"|")

            else:
                print("Wrong input!")
                
#Original Total       
        mycursor.execute("select sum(Paid) from "+cust+" ;")        
        for w in mycursor:
            w=str(w)
            w=w[10:-4]
            report.write("\n|"+"Original Total: "+w+" Rupees")
            mycursor.execute("update zzzReport set Wo_Discount="+w+" where Name='"+cust+"';")
            mydb.commit()
#Discount Rate        
        if fd not in ["y","Y","YES","Yes","yes","1"]:     
            try:
                disc=float(input("Discount (%):"))
            except:
                disc=0
            print("-"*80)
        mycursor.execute("update zzzReport set Discount_Per="+str(disc)+" where Name='"+cust+"';")
        mydb.commit()
        dis=100-disc
        report.write("\n|"+"Discount: "+str(disc)+"%")       
        report.write("\n|"+"_"*79+"|")
#Discounted Total
        mycursor.execute("select round(sum(Paid)*"+str(dis)+"/100,2) from "+cust+";")        
        for g in mycursor:
            g=str(g)
            g=g[10:-4]
            report.write("\n|"+"Discounted Total: "+g+" Rupees")
            mycursor.execute("update zzzReport set W_Discount="+g+" where Name='"+cust+"';")
            mydb.commit()
        report.write("\n|"+"_"*79+"|")
#Money Saved        
        mycursor.execute("select round(sum(Paid)*"+str(disc)+"/100,2) from "+cust+" ;")
        for y in mycursor:
            y=str(y)
            y=y[10:-4]
            report.write("\n|"+"Today's Savings: "+y+" Rupees")
            mycursor.execute("update zzzReport set Discount="+y+" where Name='"+cust+"';")
            mydb.commit()
       
        
        mycursor.execute("update zzzReport set UID="+uid+" where Name='"+cust+"';")
        mydb.commit()
        report.write("\n|Date, Time of Purchase: "+dt)
        report.write("\n|"+"~"*79+"|")
        report.write("\n|Thanks "+cust+" for your visit!")
        report.write("\n|Invoice prepared by: "+operator)
        report.write("\n|"+"~"*79+"|")
        report.write("\n|Find Us Open:\t\t\t\t\t\t\t\t\t|")
        report.write("\n|Mon to Sat 11:00 AM to 09:00 PM (Excluding National Holidays)\t\t\t|")
        report.write("\n|"+"_"*79+"|")
        report.write("\n|Terms and Conditions:\t\t\t\t\t\t\t\t|")
        report.write("\n|*No Return\t*No Exchange\t*No Guarantee\t\t\t\t\t|")
        report.write("\n|"+"_"*79+"|")
        
#To show names of all buyers of today
        print("Names Used:")
        mycursor.execute("show tables;")
        for v in mycursor:
            v=str(v)
            v=v.replace("zzzreport","_"*80)
            v=v.replace("zzzsale","")
            print(v[2:-3])
                
            report.close()

        os.startfile("Invoices\\Invoices of "+tdate+"\\"+cust+".txt")

    else:
        mycursor.execute("select sum(Wo_DIscount) from zzzreport;")
        for wodisc in mycursor:
            wodisc=str(wodisc)
            wodisc=wodisc[1:-2]
            print("Total Sale Without Discount: \t\t",wodisc,"₹")
        mycursor.execute("select sum(DIscount) from zzzreport;")
        for tdisc in mycursor:
            tdisc=str(tdisc)
            tdisc=tdisc[1:-2]
            if sys.version[0:6] =="3.11.5":
                print("Discounts Offered Today: \t-\t",tdisc,"₹")
                print("\t\t\t\t\t","_"*(len(wodisc)+2))
            else:
                print("Discounts Offered Today: \t\t-\t",tdisc,"₹")                
                print("\t\t\t\t\t\t\t\t\t","_"*(len(wodisc)+2))
        mycursor.execute("select sum(W_DIscount) from zzzreport;")
        for wdisc in mycursor:
            wdisc=str(wdisc)
            wdisc=wdisc[1:-2]
            if sys.version[0:6] =="3.11.5":
                print("Net Sale of Today: \t\t\t",wdisc,"₹")
            else:
                print("Net Sale of Today: \t\t\t\t\t",wdisc,"₹")
            print("_"*80)
#Code for saving today's sale report               
            yorno=input("Save Today's Sale Report?(Y/N):")
            print("_"*80)
            
            if yorno in ["y","Y","YES","Yes","yes","1"]:
                from os import path
                if path.exists("Reports"):
                    This_is_just_a_filling_statement=1000
                else:
                    os.mkdir("Reports")
                    
                if path.exists("Reports\Report of "+tdate):
                    This_is_just_a_filling_statement=1000
                else:
                    os.mkdir("Reports\Report of "+tdate)
                my_dir="Reports\Report of "+tdate

                mycursor.execute("select concat(dayofmonth(now()),"+us+",monthname(now()),"+us+",year(now()))")
                for tdate in mycursor:
                    tdate=str(tdate)
                    tdate=tdate[2:-3]
                
                file_name=tdate+"'s Sale Report.txt"
                fname=os.path.join(my_dir,file_name)
                
                count=[]
                mycursor.execute("select Number from zzzSale;")
                for cn in mycursor:
                    cn=str(cn)
                    cn=cn[1:-2]
                    cn=int(cn)
                    count.append(cn)
                
                report= open(fname,"w")
                report.write(" "+"_"*79)
                report.write("\n|\t\t\tNature's Basket Herbal Store\t\t\t\t|")
                report.write("\n|\t\t\t111, New Road Ratlam\t\t\t\t\t|")
                report.write("\n|\t\t\tContact Number 1212121212\t\t\t\t|")
                report.write("\n|"+"_"*79+"|")
                report.write("\n|\t\t       Closure Report of "+tdate)
                report.write("\n|"+"_"*79+"|")
                mycursor.execute("select concat(current_time())")
                for rtime in mycursor:
                    rtime=str(rtime)
                    rtime=rtime[2:-3]
                report.write("\n|  Operator: "+operator+" \t\t\tTime of Closure: "+rtime)
                report.write("\n|"+"_"*79+"|")
                mycursor.execute("select count(S_no) from zzzReport;")
                for nbuyers in mycursor:
                    nbuyers=str(nbuyers)
                    nbuyers=nbuyers[1:-2]
                report.write("\n|  Number of Buyers: "+nbuyers)
                report.write("\n|"+"_"*79+"|")
                report.write("\n|  Total Sale Without Discount: \t"+wodisc+" Rs")
                report.write("\n|  Discounts Offered Today:\t_\t"+tdisc+" Rs")
                report.write("\n|\t\t\t\t\t"+"_"*(len(wodisc)+4))
                report.write("\n|  Net Sale of Today: \t\t\t"+wdisc+" Rs")
                report.write("\n|"+"_"*79+"|")
                report.write("\n| \t\t\t\tBuyers' List:\t\t\t\t\t|")
                report.write("\n|"+"_"*79+"|")
                report.write("\n|"+" S_no |      Name of Buyer     |  Gross  |Discount%|  Discount  |  Net Payable "+"|")
                report.write("\n|"+"_"*79+"|")
                mycursor.execute("delete from zzzReport where Wo_Discount is null;")
                mydb.commit()
                blank="     "
                blank=str(blank)
                mycursor.execute("select S_no,'"+blank+"',Name,'"+blank+"',Wo_Discount,'"+blank+"',Discount_Per,'"+blank+"',Discount,'"+blank+"',W_Discount from zzzreport")
                for rtt in mycursor:
                    rtt=str(rtt)
                    rtt=rtt.replace("'","")
                    rtt=rtt.replace(",","")
                    rtt=str(rtt)
                    rtt=rtt[1:-1]
                    report.write("\n| "+rtt)
                    report.write("\n|"+"-"*79+"|")
                report.write("\n|"+"_"*79+"|")
                report.write("\n| \t\t\t\tCommodities Sold:\t\t\t\t|")
                report.write("\n|"+"_"*79+"|")
                report.write("\n| S_no\t|\t\t"+"Commodity\t\t|\t"+"Units Sold\t\t|")
                report.write("\n|"+"_"*79+"|")
            
                for repfea in range(1,len(c)+1):
                    mycursor.execute("select S_no,'"+blank+"',Name,'"+blank+"',Number from zzzSale where S_No="+str(repfea))
                    for mm in mycursor:
                        mm=str(mm)
                        mm=mm.replace("'","")
                        mm=mm.replace(",","")
                        mm=str(mm)
                        mm=mm[1:-1]
                        report.write("\n| "+mm)
                        report.write("\n|"+"-"*79+"|")
                report.write("\n|"+"_"*79+"|")
                report.write("\n|  Units Sold Count: "+str(sum(count)))
                report.write("\n|"+"_"*79+"|")
                report.close()
                
#Code for making Report graph of the day

#names
                mycursor.execute("select Name from zzzReport;")
                names=[]
                for names1 in mycursor:
                    names1=str(names1)
                    names1=names1[2:-3]
                    names.append(names1)
                
#discount%
                mycursor.execute("select Discount_Per from zzzReport;")
                discper=[]
                for discper1 in mycursor:
                    discper1=str(discper1)
                    discper1=discper1[1:-2]
                    discper1=float(discper1)
                    discper.append(discper1)
                
#without discount
                mycursor.execute("select Wo_Discount from zzzReport;")
                wo_disc=[]
                for wo_disc1 in mycursor:
                    wo_disc1=str(wo_disc1)
                    wo_disc1=wo_disc1[1:-2]
                    wo_disc1=float(wo_disc1)
                    wo_disc.append(wo_disc1)
                
#with discount
                mycursor.execute("select W_Discount from zzzReport;")
                w_disc=[]
                for w_disc1 in mycursor:
                    w_disc1=str(w_disc1)
                    w_disc1=w_disc1[1:-2]
                    w_disc1=float(w_disc1)
                    w_disc.append(w_disc1)
                
#discount
                mycursor.execute("select Discount from zzzReport;")
                discou=[]
                for discou1 in mycursor:
                    discou1=str(discou1)
                    discou1=discou1[1:-2]
                    discou1=float(discou1)
                    discou.append(discou1)
                
#Code for drawing graph
                import matplotlib.pyplot as plt
                
                lab=[]
                for n in range(len(c)):
                    lab.append(x1[n]+": "+str(count[n]))
                    
#For drawing pie chart
                plt.pie(count, explode= np.tile(.05,len(c)), labels=lab, autopct= "%2.2f%%", pctdistance= 0.8 )
                plt.text(0., 0., "Total:\n"+str(sum(count)), verticalalignment= "center", horizontalalignment= "center")
                centre_circle=plt.Circle((0,0),0.5, fc="white")
                fig= plt.gcf()
                fig.gca().add_artist(centre_circle)
                plt.title("Sale Share of "+tdate+":\n")
                plt.axis("equal")
                
#For saving the pie chart
                my_path=os.path.abspath("Reports\Report of "+tdate)
                my_file=tdate+"'s Sale Share.pdf"
                plt.savefig(os.path.join(my_path,my_file), bbox_inches="tight", pad_inches=0.5)
                
                fig,ax=plt.subplots()
                plt.plot(w_disc,color="#0077b3", linestyle="dotted",label="Net Paid", marker="o",markersize=5)
                plot=plt.bar(names,wo_disc, edgecolor="#ff9900",color="#fff5e6",hatch="xxx",label="Before Discount",width=0.5)
                for value in plot:
                    height=value.get_height()
                    plt.text(value.get_x()+value.get_width()/2.,1.002*height,'%d'%int(height),ha='left',va='bottom',color='#cc7a00',size=5)
                plot1=plt.bar(names,w_disc, color="#eeffe6",edgecolor="#44cc00",hatch="///",label="After Discount",width=0.5)
                for value in plot1:
                    height=value.get_height()
                    plt.text(value.get_x()+value.get_width()/2.,1.002*height,'%d'%int(height),ha='right',va='top',size=5)
                plot2=plt.bar(names,discou, color="#fff2e6",edgecolor="red",hatch="\\\\\\",label="Discount",width=0.5)
                for value in plot2:
                    height=value.get_height()
                    plt.text(value.get_x()+value.get_width()/2.,1.002*height,'%d'%int(height),ha='left',va='top',color='#990000',size=5)
                leg=ax.legend()
                plt.xlabel("Buyers")
                plt.xticks(rotation=90)
                plt.ylabel("Purchases Made")
                plt.title("Data of "+tdate+":")
                
#For saving the Graph of the Report
                my_path=os.path.abspath("Reports\Report of "+tdate)
                my_file=tdate+"'s Buyers.pdf"
                plt.savefig(os.path.join(my_path,my_file),bbox_inches="tight")
                
                print("Report Created by Name: Report of",tdate)
                print("_"*80)
            else:
                This_is_just_a_filling_statement=1000
                
        print("Closure for today!")
        print("_"*80)
        input("                Press Enter to delete Today's data from SQL")
        mycursor.execute("drop database if exists shop")
        print("                        Database (Shop) Deleted.")
        print("_"*80) 
        break
#After creating all invoices for the day, the SQL database is deleted