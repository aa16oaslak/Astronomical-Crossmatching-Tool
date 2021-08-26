import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd

from tkinter import *
from tkinter import ttk
import sqlite3
import os 
import csv
import sqlite3 as sql
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog

window=Tk()
label=Label(window,text="Tool For Positional Cross-matching of two Astronomical Catalogs",font=('arial',18,'bold'),bg='red',fg='white')
label.pack(side=TOP,fill=X)
label=Label(window,text="© This GUI tool is developed by Ashesh AK",font=('arial',10,'bold'),bg='red',fg='white')
label.pack(side=BOTTOM,fill=X)

label=Label(window,text='Please enter the file directory for both the catalogs (Format e.g. D:/catlog.csv). Note: This tool will only work for csv files.',font=('arial',12,'italic'),fg='black')
label.place(x=0,y=40)
label=Label(window,text='Enter the file directory for catalog 1:',font=('arial',12,'bold'),bg='white',fg='black')
label.place(x=0,y=90)
label=Label(window,text='Enter the file directory for catalog 2:',font=('arial',12,'bold'),bg='white',fg='black')
label.place(x=0,y=140)

cat1_entry=StringVar()
cat1_entry=ttk.Entry(window,textvariable=cat1_entry)
cat1_entry.place(x=280,y=90,width=600)
cat1_entry.focus()
cat2_entry=StringVar()
cat2_entry=ttk.Entry(window,textvariable=cat2_entry)
cat2_entry.place(x=280,y=140,width=600)

def Next_Win():
    a = cat1_entry.get()
    b = cat2_entry.get()
    if a != '' and b != '':
        window.destroy()
        window2=Tk()
        window2.title('User requirements')
        window2.geometry("1000x600+420+170")
        label=Label(window2,text="User requirements",font=('arial',18,'bold'),bg='gold2',fg='white')
        label.pack(side=TOP,fill=X)
        label=Label(window2,text="© This GUI tool is developed by Ashesh AK",font=('arial',10,'bold'),bg='gold2',fg='white')
        label.pack(side=BOTTOM,fill=X)
        
        label=Label(window2,text='Required details for Catalog 2',font=('arial',18,'bold'),bg='gold2',fg='white')
        label.place(x=300,y=40)
        label=Label(window2,text='Enter the column number for Right Acension:',font=('arial',10,'bold'))
        label.place(x=50,y=100)
        label=Label(window2,text='Enter the column number for Declination:',font=('arial',10,'bold'))
        label.place(x=50,y=140)
        label=Label(window2,text='Enter the attributes you want from catalog 1 in the final csv file (Format: attr1,attr2,attr3):',font=('arial',10,'bold'))
        label.place(x=50,y=180)
        
        label=Label(window2,text='Required details for Catalog 2',font=('arial',18,'bold'),bg='gold2',fg='white')
        label.place(x=300,y=240)
        label=Label(window2,text='Enter the column number for Right Acension:',font=('arial',10,'bold'))
        label.place(x=50,y=280)
        label=Label(window2,text='Enter the column number for Declination:',font=('arial',10,'bold'))
        label.place(x=50,y=320)
        label=Label(window2,text='Enter the attributes you want from catalog 2 in the final csv file (Format: attr1,attr2,attr3):',font=('arial',10,'bold'))
        label.place(x=50,y=360)
        
        label=Label(window2,text='Crossmatching criteria',font=('arial',18,'bold'),bg='gold2',fg='white')
        label.place(x=300,y=400)
        label=Label(window2,text='Please enter the threshold distance(in arcsec):',font=('arial',10,'bold'))
        label.place(x=50,y=460)

        

        entry1 = IntVar()
        entry1 = ttk.Entry(window2,textvariable=entry1)
        entry1.place(x=350,y=100,width=60)
        
        entry2 = IntVar()
        entry2 = ttk.Entry(window2,textvariable=entry2)
        entry2.place(x=350,y=140,width=60)
        
        entry3 = StringVar()
        entry3 = ttk.Entry(window2,textvariable=entry3)
        entry3.place(x=620,y=180,width=200)
        
        entry4 = IntVar()
        entry4 = ttk.Entry(window2,textvariable=entry4)
        entry4.place(x=350,y=280,width=60)
        
        entry5 = IntVar()
        entry5 =ttk.Entry(window2,textvariable=entry5)
        entry5.place(x=350,y=320,width=60)
        
        entry6 = StringVar()
        entry6 =ttk.Entry(window2,textvariable=entry6)
        entry6.place(x=620,y=360, width=200)
        
        entry7 = IntVar()
        entry7 =ttk.Entry(window2,textvariable=entry7)
        entry7.place(x=350,y=460,width=60)
        
            
        def import_cat():
            ra1 = int(entry1.get())
            dec1 = int(entry2.get())
            data1 = np.loadtxt(a, delimiter=',', skiprows=1, usecols=[ra1,dec1])
            res1 = []
            for row1 in data1:
                res1.append((row1[0], row1[1]))
            
            ra2 = int(entry4.get())
            dec2 = int(entry5.get())
            data2 = np.loadtxt(b, delimiter=',', skiprows=1, usecols=[ra2,dec2])
            res2 = []
            for row2 in data2:
                res2.append((row2[0], row2[1]))
            return res1,res2
            

        def crossmatch(coords1, coords2, max_radius):
            matches = []
            no_matches = []
            
            # Converting to astropy coordinates objects
            coords1_sc = SkyCoord(coords1*u.degree, frame='icrs')
            coords2_sc = SkyCoord(coords2*u.degree, frame='icrs')
            
            # Performing crossmatching
            closest_ids, closest_dists, _ = coords1_sc.match_to_catalog_sky(coords2_sc)
            
            for id1, (closest_id2, dist) in enumerate(zip(closest_ids, closest_dists)):
                closest_dist = dist.value
                # Ignore the match if it's outside the maximum radius
                if closest_dist > max_radius:
                    no_matches.append(id1)
                else:
                    matches.append([id1, closest_id2, closest_dist])
            return matches, no_matches
        
        def crossmatch_call():
            cat1,cat2 = import_cat()
            arr1 = np.asarray(cat1)
            arr2 = np.asarray(cat2)
            # max-radius in which we wanna do our positional cross-matching
            dist = int(entry7.get())
            max_dist = dist/3600   # Unit of max_dist is in degrees
            matches, no_matches = crossmatch(arr1, arr2, max_dist)
            
            #Filtering and creating the master catalog according to users requirement
            id_matched_cat1 = [row[0] for row in matches]
            id_matched_cat2 = [row[1] for row in matches]
            closest_dist = [row[2] for row in matches]
            
            col_names_cat1 = entry3.get()
            col_names_cat1 = col_names_cat1.split(',')
            col_names_cat2 = entry6.get()
            col_names_cat2 = col_names_cat2.split(',')
            
            df = pd.read_csv(a)
            df.drop(no_matches,0,inplace=True)
            df.reset_index(inplace = True, drop = True)
            col_names_cat1
            
            df1 = pd.read_csv(b)
            df1= df1.iloc[id_matched_cat1, :]
            df1.reset_index(inplace = True, drop = True)
            
            #attributes required by the user
            df= df.loc[: , col_names_cat1]
            df1= df1.loc[: , col_names_cat2]
            
            #joining the two catalogs
            df2= pd.concat([df, df1], axis=1)
            df2.to_csv('DBMS.csv', index= False)
            
            messagebox.showinfo("Success!", "The catalogs has been successfully cross-matched. Please Check your file directory for the final resulting catalog.")
            window2.destroy()
            
            
        btn2=ttk.Button(window2,text='Click here to Start the Cross-matching Procedure',command = crossmatch_call)
        btn2.place(x=270,y=520,width=400,height=40)

    else:
        messagebox.showerror('Error','Please Enter the catalog directories')

btn=ttk.Button(window,text='Next',command=Next_Win)
btn.place(x=270,y=180,width=120,height=40)


window.title("Postitional Cross-matching Tool")
window.geometry("1000x400+420+170")
window.mainloop()
