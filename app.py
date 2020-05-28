import sqlite3
import flask

app = flask.Flask(__name__)

def get_db():
    db = sqlite3.connect('PairWorkDBMS.db')
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/additem')
def additem():
    return flask.render_template('additem.html')

@app.route('/added', methods=['POST']) ##new entry
def added(): 
	s = flask.request.form['service']
	p = flask.request.form['price']
	db = get_db()
	db.execute('INSERT into TypeOfService (service,price) VALUES (?,?)',(s,p))
	db.commit()
	db.close()
	return flask.render_template('itemadded.html',n=n)
    
@app.route('/deleteitem')
def deleteitem():
    return flask.render_template('deleteitem.html')
    #extend to retrieve names from DB and display list in form

@app.route('/delete_entry', methods=['POST']) #default is GET
def delete_entry():
    d = flask.request.form['']
    db = get_db()
    db.execute('DELETE from TypeOfService where services = ?', [flask.request.form['services']])
    db.commit()
    return flask.render_template('viewinventory.html')

#delete with archive
#or inaction attribute in Inventory
#User ID for accountability

@app.route('/buyitem')
def buyitem():
    return flask.render_template('buyitem.html') #buyitem.html not coded yet

@app.route('/buy', methods=['GET']) #default is GET
def buy():
    service_code = ['cutS','cutM','cutL','colour','high1','high2','perm','rebond','treat']
    service = ['Cut(short length)','Cut(medium length)','Cut(long length)','Colour','Highlight(half head)','Highlight(full head)','Perm','Rebonding','Treatment']
    n = flask.request.form['name']
    d = flask.request.form['Date']
    m = flask.request.form['memberID']
    t = flask.request.form.getlist('services')
    total = 0.0
    db = get_db()
    db.commit()
    i = db.execute("SELECT seq FROM sqlite_sequence WHERE name = 'Transaction'").fetchall()
    i = i[0][0]
    for items in t:
        services = service_code.index(items)
        db.execute('INSERT INTO Transaction('+
               'invoiceID, type) VALUES (?,?)',(i,service[services]))
        db.commit()
        print("THIS IS SERVICE:",service[services])
        c = db.execute("SELECT price FROM Service WHERE type = (?)",(service[services],)).fetchall()
        c = c[0][0]
        total += c
    
    membership = db.execute("SELECT name FROM Member WHERE memberID = (?)",(m,)).fetchall()
    if membership[0][0] == n:
        discount = 0.9
    else:
        discount = 1.0
    payable = total * discount
    db.execute('INSERT INTO Transaction('+
               'Date,name,memberID,TotalPayable) VALUES (?,?,?,?)',(d,n,m,payable))
    db.commit()
    db.close()
    return flask.render_template('added.html',n=n)
    

@app.route('/viewinventory')
def viewinventory():
    db = get_db()
    rows = get_db().execute('SELECT * FROM TypeOfService').fetchall()
    db.close()
    return flask.render_template('viewinventory.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)




