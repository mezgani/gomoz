import sqlite3


class Gomozdblite:
    def __init__(self, scan, menu):
        self.scan=scan
        self.menu=menu
        self.connexion=''
        self.cur=''

    def Connectdb(self, db):
        self.con = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cur = self.con.cursor()


    def Createdb(self):
        self.cur.execute("create table scan(request integer primary key, url varchar(255), exploit varchar(500), date timestamp, status varchar(50))")
        self.cur.execute("create table menu(url varchar(255), include varchar(255), proxy varchar(150), exploit varchar(500))")
     

    def Insertdb(self):
       
        for i in self.scan:     
            #server info 'iis|apache|others'
            self.cur.execute("insert into scan values(?,?,?,?,?)",(int(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4])))
        self.cur.execute("insert into menu values(?,?,?,?)",(str(self.menu[0]),str(self.menu[1]),str(self.menu[2]),str(self.menu[3])))
        self.con.commit()


    def Selectdb(self):
        self.cur.execute("select request, url, exploit, date, status from scan")
        scans = self.cur.fetchall()
        
        self.cur.execute("select  url, include, proxy, exploit from menu")
        menus = self.cur.fetchall()
        return (scans, menus)


    def Selectsdb(self):
        self.cur.execute("select request, url, exploit, date, status from scan")
        while (1):
            row = self.cur.fetchone()
            print "request", "=>", row[0], type(row[0])
            print "url", "=>", row[1], type(row[1])
            print "exploit", "=>", row[2], type(row[2])
            print "date", "=>", row[3], type(row[3])
            print "status", "=>", row[4], type(row[4])
            if row is None: break

    def Affichdb(self, rows):
        
        for row in rows:
            print "request", "=>", row[0], type(row[0])
            print "url", "=>", row[1], type(row[1])
            print "exploit", "=>", row[2], type(row[2])
            print "date", "=>", row[3], type(row[3])
            print "status", "=>", row[4], type(row[4])


    def Closedb(self):
        self.cur.close()
        self.con.close()
