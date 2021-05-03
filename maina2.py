from flask import Flask, render_template, session, request, redirect, url_for
import boto3
from boto3.dynamodb.conditions import Key,Attr


app = Flask(__name__)
app.secret_key = 'mykey'


@app.route('/login',methods = ['GET','POST'])
def login():
    error = None
    if request.method =='POST':
        email = request.form['id']
        password = request.form['password']
        session["email"] = email
        
        print('d' + email)
        user = fetch_email(email)
        print(user) 
        if user:
            print("usr present")
            for data in user:
                email = data['email']
                userpassword = data['password']
                print(userpassword)
                session['username']= data['user_name']
                session['msgid'] = 1
                if userpassword == password:
                    return redirect(url_for('mainpage'))
                else:
                    error =" ID or password is invalid"
                    print("a error", error)
                    return render_template('login.html',error=error)
        else:
            error =" ID or password is invalid"
            print("b error", error)
            return render_template('login.html', error=error)
            
    return render_template('login.html', error=error)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    error_message = None
    if request.method == 'POST':
        email = request.form['id']
        username= request.form['username']
        password=request.form['password']
        
        print (username)
        user = fetch_email(email)
        
        print(user)
        

        if user:
            error = "TheEmail ID already exists"
            return render_template('register.html',error = error)
            print(user)
        else:
            print ("else")
            response = update(email, username, password)
            print (response)
            return redirect(url_for('login'))
            #return render_template('login.html',error = error_message)
    
    return render_template('register.html',error = error)
 
@app.route('/mainpage',methods = ['GET','POST'])
def mainpage():
    error = None
    fetchresult= " "
    
    username = session['username']
    
    url = "https://storagea2.s3.amazonaws.com/"
    
    subremove = fetchrem(username)
    
    if request.method == 'POST' and 'query' in request.form:
        title = request.form['title']
        artist = request.form['artist']
        year = request.form['year']
        
        if title and artist and year:
            fetchresult = fetchtitarye(title,artist,year)
        
        if title and artist:
            fetchresult = fetchtitar(title,artist)
        
        if title and year:
            fetchresult = fetchtitye(title,year)
        
        if artist and year:
            fetchresult= fetcharye(artist,year)
        
        if title:
            fetchresult = fetchtit(title)
        
        if artist:
            fetchresult = fetchart(artist)
        
        if year:
            fetchresult = fetchyear(year)
        
        print(fetchresult)
        
        if fetchresult:
            error = None
        else:
            error = "No result is retrieved. Please query again" 
        
        
    if request.method == 'POST' and 'subscribe' in request.form:
        print(request.form)
        title = request.form['title']
        artist = request.form['artist']
        year = request.form['year']
        username = session['username']
        
        print("title", title)
        print("year", year)
        print("artist", artist)
        print("username", username)
        
        result = updating(title,year,artist,username)
        print (result)
        return redirect(url_for('mainpage'))
        
    if request.method == 'POST' and 'remove' in request.form:
        title = request.form['title']
        username = session['username']
        
        result = remove_sub(title, username)
        return redirect(url_for('mainpage'))
        
    print(url)   
    
    return render_template('mainpage.html',fetchresult = fetchresult,url = url, error = error, subremove = subremove)

def fetchrem(username, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('subscribed')
    response = table.scan(FilterExpression = Attr('username').eq(username) )
    
    return response['Items']


def updating(title,year,artist,username,dynamodb = None):
    
    if not dynamodb:

        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')

    table = dynamodb.Table('subscribed')

    response = table.put_item(

        Item={


            'username':username,
            
            'title': title,

            'year': year,

            'artist': artist
            
            

        }

    )

    return response
    
def update(email, username, password,dynamodb=None):

    if not dynamodb:

        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')

    table = dynamodb.Table('login')

    response = table.put_item(

        Item={

            'email': email,

            'user_name': username,

            'password': password

        }

    )

    return response
    
    
def remove_sub(title, username,dynamodb=None):

    if not dynamodb:

        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')

    table = dynamodb.Table('subscribed')

    response = table.delete_item(

        Key={

            'username': username,
            'title': title

        }

    )

    return response
    
    
    
def fetchtitarye(title,artist,year,dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('music')
    response = table.scan(FilterExpression = Attr('title').eq(title) & Attr('artist').eq(artist) & Attr('year').eq(year))
    
    return response['Items']
    
def fetchtitar(title,artist,dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('music')
    response = table.scan(FilterExpression = Attr('title').eq(title) & Attr('artist').eq(artist) )
    
    return response['Items']
    
def fetchtitye(title,year,dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('music')
    response = table.scan(FilterExpression = Attr('title').eq(title)& Attr('year').eq(year))
    
    return response['Items']
    
def fetcharye(artist,year,dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('music')
    response = table.scan(FilterExpression = Attr('artist').eq(artist) & Attr('year').eq(year))
    
    return response['Items']
    
def fetchtit(title,dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('music')
    response = table.scan(FilterExpression = Attr('title').eq(title) )
    
    return response['Items']
    
def fetchtitart(artist,dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('music')
    response = table.scan(FilterExpression =  Attr('artist').eq(artist) )
    
    return response['Items']
    
def fetchyear(year,dynamodb = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        
    table = dynamodb.Table('music')
    response = table.scan(FilterExpression = Attr('year').eq(year))
    
    return response['Items']
    
def fetch_email(email, dynamodb=None):


    if not dynamodb:

        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')

    table = dynamodb.Table('login')

    response = table.query(

        KeyConditionExpression=Key('email').eq(email)

    )

    return response['Items']
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
   print('in logout')
   #session.pop('loggedin', None)
   session.pop('id', None)
   #session.pop('username', None)
   
   print('url: ' + url_for('login'))
   
   return redirect(url_for('login'))

    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)