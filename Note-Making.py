from tkinter import *
from tkinter import messagebox
import pymysql as pm

root = Tk()
root.geometry('700x700')
root.title('Note Taking App')

#database
try:
    con = pm.connect(host='localhost', database='project', user='root',password='oggy123')
    cursor = con.cursor()
    query1 = 'create table note_making(note_title varchar(40) primary key,notes varchar(1000))'
    cursor.execute(query1)
    

    #functions

    #function for adding new notes
    def add_new_notes():
        top1 = Toplevel()
        top1.title('Adding notes')
        top1.geometry('550x550')
        
        l2 = Label(top1,text = 'NOTES TITLE')
        l2.place(x = 5,y = 5)
        e2 = Entry(top1,width = 30,font = ('calibri',15))
        e2.place(x = 5,y = 25)

        l3 = Label(top1,text = 'NOTES')
        l3.place(x = 5,y = 70)

        s2=Scrollbar(top1)
        s2.place(x = 430,y =90)
        s4 = Scrollbar(top1)
        t2 = Text(top1,height = 20,wrap = NONE,width = 50,xscrollcommand = s4.set,yscrollcommand = s2.set)
        s2.config(command = t2.yview)
        s4.config(command = t2.xview,orient = HORIZONTAL)
        t2.place(x = 5,y = 90)
        s4.place(x = 5,y =425)
        

        
        def add_to_database():
            try:
                if len(e2.get())!=0:
                    if (len(t2.get("1.0", "end-1c"))==0):
                        temp = messagebox.askokcancel("WARNING!","No content is added to %s note"%(e2.get()))
                        if temp:
                            cursor.execute(" INSERT INTO note_making VALUES (%s,%s) ", (e2.get(),t2.get("1.0",END)))
                            con.commit()
                            e2.delete(0,'end')
                            t2.delete("1.0",END)
                            messagebox.showinfo("Congratulations!!","Your Note is added succeessfully")
                            
                        else:
                            sol = messagebox.askyesno("QUESTION!","Do you want to add another?")
                            if sol:
                                add_new_notes()
                            
                    else:
                        cursor.execute(" INSERT INTO note_making VALUES (%s,%s) ", (e2.get(),t2.get("1.0",END)))
                        con.commit()
                        e2.delete(0,'end')
                        t2.delete("1.0",END)
                        l4 = Label(top1,text = 'Data is inserted successfully')
                        l4.place(x = 100,y = 500)
                else:
                    messagebox.showinfo("EMPTY TITLE!!","You have not given any title to your notes.\nNotes without title cannot be added.")
            except Exception as e:
                messagebox.showinfo("DUPLICATE NOTES","Note with this name %s already exists.Try giving a new name. "%(e2.get()))
                        
        b4 = Button(top1,text = 'ADD',bg = 'green',width = 20,command = add_to_database)
        b4.place(x = 200,y = 440)

        b5 = Button(top1,text = 'Exit',bg = 'red',width = 15,command = top1.destroy)
        b5.place(x = 380,y = 440)


    #function to list all notes
    def list_notes():
        query3 = 'select note_title from note_making order by note_title asc'
        rows_count = cursor.execute(query3)
        t1.config(state=NORMAL)
        t4.config(state=NORMAL)
        t1.delete("1.0",END)
        t4.delete("1.0",END)
        
        if rows_count>0:
            t4.insert(END,"ALL NOTES--")
            data1 = cursor.fetchall()
            for row in data1:
                t1.insert(END,row[0]+'\n')
            
        else:
            messagebox.showinfo("Failure","There are no notes present.")
        t1.config(state=DISABLED)   
        
    #function to update notes
    def update_notes():
        top2 = Toplevel()
        top2.title('Updating notes')
        top2.geometry('550x550')
        
        l5 = Label(top2,text = 'NOTES TITLE')
        l5.place(x = 5,y = 5)
        e3 = Entry(top2,width = 30,font = ('calibri',15))
        e3.place(x = 5,y = 25)

        l6 = Label(top2,text = 'NOTES')
        l6.place(x = 5,y = 70)

        s3=Scrollbar(top2)
        s3.place(x = 430,y =90)
        t3 = Text(top2,height = 20,width = 50,yscrollcommand = s3.set)
        s3.config(command = t3.yview)
        t3.place(x = 5,y = 90)


        def update_to_database():
            rows_count = cursor.execute("""UPDATE note_making SET notes=%s WHERE note_title=%s""",(t3.get("1.0",END),e3.get()))
            con.commit()
            
            if rows_count>0:
                l7 = Label(top2,text = 'successfully updated notes',width = 50)
                l7.place(x = 150,y = 480)
            else:
                l7 = Label(top2,text = 'There is no notes found as titled %s'%(e3.get()),width = 50)
                l7.place(x = 150,y = 480)

            t3.delete("1.0",END)
            e3.delete(0,'end')

        b8 = Button(top2,text = 'Save New Changes',bg = 'blue',width = 20,command = update_to_database)
        b8.place(x = 150,y = 440)

        def view_notes():
            rows_count = cursor.execute("select notes from note_making where note_title=%s",(e3.get()))
            if rows_count>0:
                data1 = cursor.fetchall()
                for row in data1:
                    t3.insert(END,row[0])
            else:
                l7 = Label(top2,text = 'There are no existing notes titled %s'%(e3.get()),width = 50)
                l7.place(x = 150,y = 480)
                
        
        b10 = Button(top2,text = 'Change in existing file',command = view_notes)
        b10.place(x = 300,y = 25)


        b9 = Button(top2,text = 'Exit',bg = 'red',width = 15,command = top2.destroy)
        b9.place(x = 380,y = 440)


    #function to delete notes
    def delete_notes():
        top3 = Toplevel()
        top3.geometry('400x150')
        l8 = Label(top3,text = "Which note you want to delete?")
        l8.place(x = 5,y = 5)
        e4 = Entry(top3,width = 30,font = ('calibri',15))
        e4.place(x = 5,y = 30)

        def delete_from_database():
            result = messagebox.askokcancel("Delete Notes","Are you sure you want to delete this note?")
            if result:
                rows_count = cursor.execute(""" DELETE from note_making WHERE note_title=%s""",(e4.get()))
                con.commit()
                if rows_count>0:
                    messagebox.showinfo("Success","Notes with title %s are deleted succeessfully"%(e4.get()))
                else:
                    if(len(e4.get())!=0):
                        messagebox.showinfo("Failure","There are no notes having title %s"%(e4.get()))
                    else:
                        messagebox.showinfo("OOPS!!","Nothing to delete.")

                
        def deleteall_from_database():
            result = messagebox.askokcancel("Delete All Notes","Are you sure you want to delete all the available notes ?")
            if result:
                rows_count = cursor.execute(""" DELETE from note_making """)
                con.commit()
                if rows_count>0:
                    messagebox.showinfo("Success","All Notes were deleted succeessfully")
                else:
                    messagebox.showinfo("Failure","There are no notes present.")
        
        b9 = Button(top3,text = 'DELETE',width = 17,command = delete_from_database)
        b9.place(x =20,y=70)

        b11 = Button(top3,text = 'DELETE All',width = 17,bg = 'red',command = deleteall_from_database)
        b11.place(x =180,y=70)


    #function to search notes
    def search_notes():
        if(len(e1.get())==0):
            messagebox.showinfo("OOPS!!","Nothing to search")
        else:
            rows_count = cursor.execute("""SELECT * from note_making WHERE note_title=%s""",(e1.get()))
            t1.config(state=NORMAL)
            t4.config(state=NORMAL)
            t1.delete('1.0',END)
            t4.delete('1.0',END)
            e1.delete(0,'end')
            if rows_count > 0:
                rs = cursor.fetchall()
                for row in rs:
                    t1.insert(END,row[1])
                    if(len(t1.get("1.0", "end-1c"))==1):
                        messagebox.showinfo("EMPTY",row[0]+" is empty.")
                    else:
                        t4.insert(END,"NOTES TITLE: "+row[0])

            else:
                messagebox.showinfo("ERROR",'no results found')
            t1.config(state=DISABLED)
            

    ####MAIN WINDOW WIDGETS####
      

    #button for adding new notes
    b1 = Button(root,text='Add New Note>>',height = 2,width = 30,bg ='orange',foreground='white',font=('calibri', 10, 'bold'))
    b1.config(command = add_new_notes)
    b1.place(anchor='nw', x=20,y=20)

    #button for listing all notes
    b2 = Button(root,text='List All Notes>>',height = 2,width = 30,bg ='orange',foreground='white',font=('calibri', 10, 'bold'),command = list_notes)
    b2.place(x=320,y =20)

    #button for updating notes
    b6 = Button(root,text = 'Update Notes>>',height = 2,width = 30,bg ='orange',foreground='white',font=('calibri', 10, 'bold'),command =update_notes)
    b6.place(x = 20,y = 70)

    #button for deleting notes
    b7 = Button(root,text = 'Delete Notes>>',height = 2,width = 30,bg ='red',foreground='white',font=('times', 10, 'bold'),command =delete_notes)
    b7.place(x = 320,y = 70)
    

    l1 = Label(root,text = 'Search Notes',font = ('calibri',20,'bold'))
    l1.place(x = 20, y = 135)

    #entry box for searching notes
    large_font = ('calibri',15)
    e1 = Entry(root,width = 40,font = large_font)
    e1.place(x = 20,y = 185)

    b3 = Button(root,text='Search',height = 1,width = 15,bg ='orange',foreground='white',font=('calibri', 10, 'bold'))
    b3.config(command = search_notes)
    b3.place(x=430,y =185)

    l2 = Label(root,text = '--Notes--',font = ('calibri',15,'bold'))
    l2.place(x = 250,y = 250)

    #text box to view heading
    t4 = Text(root,height = 2,width = 70,bg = 'green',state=DISABLED)
    t4.place(x = 0,y =280)
    

    #text box to view notes
    s1=Scrollbar(root)
    s1.place(x = 570,y =320)
    s5 = Scrollbar(root,orient = HORIZONTAL)
    t1 = Text(root,wrap = NONE,height = 20,width = 70,bg = 'green',state=DISABLED,yscrollcommand = s1.set,xscrollcommand = s5.set)
    s1.config(command = t1.yview)
    s5.config(command = t1.xview)
    s5.place(x = 0,y = 640)
    t1.place(x = 0,y = 320)

    root.mainloop()

        
    
except pm.DatabaseError as e:
    if con:
        con.rollback()
        print("problem",e)
finally:
   cursor.close()
   con.close()
