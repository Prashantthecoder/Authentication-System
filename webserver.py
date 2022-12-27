import ctypes
from dataclasses import fields
from http import server
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi, os
import cgitb; cgitb.enable()
import mysql.connector
import base64
from pathlib import Path
import os 
import urllib
import webbrowser

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@2912Yadav",
    database="EmployeeTable"
)

cursor = mydb.cursor()
# tasklist = []





def write_file(filename,data):
    with open(filename, 'wb') as file:
        file.write(data)


p = []
tbl = '<thead><tr><th>File Name</th><th>Files</th></tr></thead>'
p.append(tbl)

ab = []
# ac = []



# print(s)
class requestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        files = ' '.join(p)

        if self.path.endswith('/'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            # ab = webbrowser.open('/home/eigen/Desktop/practice/pythonserver/files/pan.jpeg')
            
            output = """<html>
                            <body>
                                <h1>Account</h1>
                                <h3><a href="/new">Login</a></h3>
                                <h4><a href="/registration">Registration</a></h3>
                            </body>
                       </html>"""
            self.wfile.write(output.encode())
            

        elif self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<h1>Account Login</h1>'
                output += '<form method="POST" enctype="multipart/form-data" action="/new">'
                output += '<input name="task" type="text" placeholder="Username">'
                output += '<input name="pwd" type="password" placeholder="Password">'
                output += "<input type='submit' value='submit'>"
                output += '</form>'
                output += '</body></html>'
                self.wfile.write(output.encode())
    
        if self.path.endswith('/login'):
            global var1
            var1 = ab[0]
            global var2
            var2 = ab[1]
            cursor.execute('SELECT * FROM home_userpassword WHERE username={!r} AND password={!r}'.format(str(var1),str(var2)))
            account = cursor.fetchone()
            
            if account == None:
                print("Loginfailed")
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/loginfailed')
                self.end_headers()
            else:
                self.send_response(202)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<h1>Please Upload Your File Here</h1>'
                output += '<form method="POST" enctype="multipart/form-data" action="/login">'
                output += '<label for="fileid">File ID </label>'
                output += '<input name="fileid" type="number" required><br><br>'
                output += '<label for="filename">File Name </label>'
                output += '<input name="filename" type="text" required><br><br>'
                output += '<label for="uploadfile">Select Your File Here </label>'
                output += '<input name="uploadfile" type="file" required><br><br>'
                output += '<input type="submit" value= "Upload">'
                output += '</form>'

                # output += '<form method="POST" enctype="multipart/form-data" action="/upload">'
                # output += '<input type="submit" value= "View">'
                # output += '</form>'
                output += '</body></html>'
                self.wfile.write(output.encode())

            

        if self.path.endswith('/registration'):
            self.send_response(201)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'
            output += '<h1>Add User</h1>'
            output += '<form method="POST" enctype="multipart/form-data" action="/registration">'
            output += '<input name="user" type="text" placeholder="Enter Your Username">'
            output += '<input name="pass" type="password" placeholder="Password">'
            output += "<input type='submit' value='submit'>"
            output += '</form>'
            output += '</body></html>'
            self.wfile.write(output.encode())


        if self.path.endswith('/upload'):
            cursor.execute('SELECT * FROM home_userpassword WHERE username={!r} AND password={!r}'.format(str(var1),str(var2)))
            account = cursor.fetchone()
            
            if account == None:
                print("Loginfailed")
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/loginfailed')
                self.end_headers()
            else:
                self.send_response(203)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = """<html>
                            <body>
                            <h1>Your Files Here </h1>
                                <form method="POST" enctype="multipart/form-data" action="/upload">
                                    <table>
                                        <tbody>
                                            %s    
                                        </tbody>
                                    </table> 
                                </form>                                                      
                            </body>
                            </html>"""%(files)
        
                self.wfile.write(output.encode())
                

        # if self.path.endswith('/showtable'):
        #     self.send_response(202)
        #     self.send_header('content-type', 'text/html')
        #     self.end_headers()
        #     output = """<html>
        #                 <body>
        #                 <h1>Data retrieved</h1>
        #                         %s    
        #                 </body>
        #                 </html>"""%(s)
        #     self.wfile.write(output.encode())
        

        if self.path.endswith('/loginfailed'):
            self.send_response(202)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            output = """<html>
                        <body>
                        <h1>Login failed</h1>   
                        </body>
                        </html>"""
            self.wfile.write(output.encode())

        

    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                global new_task
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task')
                global a
                a = ' '.join(new_task)
                print(a)
                # ab.append(a)
            

                new_task1 = fields.get('pwd')
                global b
                b = ' '.join(new_task1)
                print(b)
                # ac.append(b)

                cursor.execute('SELECT * FROM home_userpassword WHERE username=%s AND password=%s',(a,b))
                account = cursor.fetchone()
            
                if account == None:
                    print("False")
                    # tasklist.append('False')

                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/loginfailed')
                    self.end_headers()
                else:
                    print('True')
                    for items in account:
                        ab.append(items)
                    print("Login Successfull...")
                    # print(account)
                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/login')
                    self.end_headers()

        if self.path.endswith('/login'):
                        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                        content_len = int(self.headers.get('Content-length'))
                        pdict['CONTENT-LENGTH'] = content_len

                        if ctype == 'multipart/form-data':
                            fields = cgi.parse_multipart(self.rfile, pdict)
                            fileid = fields.get('fileid')
                            filename = fields.get('filename')
                            uploadfile = fields.get('uploadfile')

         
                            serialno = ' '.join(fileid)
                            name = ' '.join(filename)
                            file = b' '.join(uploadfile)
                            
                            try:
                                sql_insert = "INSERT INTO uploads (file, username, id ,name) VALUES(%s,%s,%s,%s)"
                                insert_values = (file, a, serialno, name)

                                result = cursor.execute(sql_insert, insert_values)
                                mydb.commit()
                                print("File Inserted in database Successfully....", result)
                                try:
                                    sql_fetch = """SELECT file FROM uploads WHERE id = %s"""
                                    cursor.execute(sql_fetch, fileid)
                                    result = cursor.fetchall()
                                    
                                
                                    storefilepath = "/home/eigen/Desktop/practice/pythonserver/files/{0}".format(str(name))
                                    for row in result:
                                        image = row[0]
                                        write_file(storefilepath, image )
                                        print("File move in folder successfully")
                                    try:
                                        sql_insert1 = """INSERT INTO storage ( filename, filepath, username ) VALUES(%s,%s,%s)"""
                                        insert_sql_values = (name, storefilepath, a)
                                        result1 = cursor.execute(sql_insert1, insert_sql_values)
                                        mydb.commit()
                                        print("File path are stored successfull...", result1)

                                        try:
                                            select_data = """SELECT filename, filepath FROM storage where username = %s"""
                                            # select_data = """SELECT filepath FROM storage where username = %s"""
                                            values_data = (new_task)
                                            cursor.execute(select_data, values_data)
                                            result = cursor.fetchall()
                                            
                                            for row in result:
                                                ist = ' '.join("%s")%row[0]
                                                td = "<tr><td>{0}</td>".format(str(ist))
                                                p.append(td)

                                                a = ' '.join("%s")%row[1]
                                                print(a)

                                                with open(a, 'rb') as file:
                                                    data = file.read()
                                                data1 = base64.b64encode(data)
                                                data2 = data1.decode("UTF-8")
                                                iind = "<td><img src='data:image/jpeg;base64,{0}' height=200 width=400/></td></tr>".format(str(data2))
                                                p.append(iind)
                                            # p.append(tbl)

                                                # iind = "<td><a href=  name=""links"">Click Here </a></td></tr>"

                                            # for row in result:
                                            #     ist = "<tr><td>%s</td>"%row[0]
                                            #     p.append(ist)
                                            
                                            #     iind = "<td><a href= ""%s"" name=""links"">Click Here </a></td></tr>"%row[1]
                                            #     p.append(iind)
                                            
                                            # p.append(tbl)

                                        except mysql.connector.Error as error:
                                            print(" Failed Fetch files from server {}".format(error))


                                    except mysql.connector.Error as error:
                                        print(" Failed path stored in Table {}".format(error))



                                except mysql.connector.Error as error:
                                    print(" Failed insert data in folder {}".format(error))


                            except mysql.connector.Error as error:
                                print("Failed Inserting data to mysql table {}".format(error))

                        self.send_response(303)
                        self.send_header('content-type', 'text/html')
                        self.send_header('Location', '/login/upload')
                        self.end_headers() 
                    
                    # if ctype == 'multipart/form-data':
                    #     fields = cgi.parse_multipart(self.rfile, pdict)
        if self.path.endswith('/upload'):
                    ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                    content_len = int(self.headers.get('Content-length'))
                    pdict['CONTENT-LENGTH'] = content_len

                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)

                    self.send_response(303)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/upload')
                    self.end_headers()



        if self.path.endswith('/upload'):
                    ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                    content_len = int(self.headers.get('Content-length'))
                    pdict['CONTENT-LENGTH'] = content_len

                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        file1 = fields.get('geti')
                        file2 = fields.get('links')
                        # pra = fields.get('get1')
                        print(file1)
                        print(file2)
                        # s.append(file1)
                        # s.append(file2)

                    self.send_response(303)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/showtable')
                    self.end_headers()

        if self.path.endswith('/registration'):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_task2 = fields.get('user')
                    x =' '.join(new_task2)
                    print(x)
                    

                    new_task3 = fields.get('pass')
                    y = ' '.join(new_task3)
                    print(y)

                    sql ='INSERT INTO home_userpassword(username, password) VALUES (%s ,%s)'
                    val = (x, y)
                    cursor.execute(sql, val)
                    print(cursor.rowcount, "User add Successfully....")

                    mydb.commit()
                    
                self.send_response(302)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/')
                self.end_headers()
# http://localhost:8000/home/eigen/Desktop/practice/pythonserver/files/pan.jpeg

# file:///home/eigen/Desktop/practice/pythonserver/files/pan.jpeg

def main():
    PORT = 8000
    server_address = ('', PORT)
    server = HTTPServer(server_address, requestHandler)
    print("Server Running on port %s" % PORT)
    server.serve_forever()

if __name__=='__main__':
    main()
