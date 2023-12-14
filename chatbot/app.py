import os

from .famutils import getCDB
from .famutils import current_time
from datetime import datetime
from .chatengine import queryAI
from .chatengine import getReference
from .chatengine import OPENAI_API_KEY

from langchain.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import Chroma 
from langchain.schema import Document
from langchain.llms import OpenAI
from os.path import exists
from langchain.chains import RetrievalQA
from venv import create

from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import Forbidden, HTTPException, NotFound, RequestTimeout, Unauthorized
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsauce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

APPROOT =os.path.dirname(os.path.abspath(__file__))
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cuda"}
hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

def create_app():

    conductor={}   

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from . import models
    print ("creating Database")
    with app.app_context():
        db.create_all()
    print ("Database created")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    print (f"{current_time()}  Getting and extracting CDB files")

    print(f"{app.instance_path}")
    if ("mnt" in APPROOT):
        PDROOT = os.path.join(APPROOT ,"fvdb","fam.faiss")   
    else:
        PDROOT = "/faiss/"
    
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY 
    embeddings = OpenAIEmbeddings()  
    i=0
    persist_dir=os.path.join(PDROOT) 
    print(f"{current_time()}  Loading Vector Database from persisted directory {persist_dir}") 
    vectordb=FAISS.load_local(PDROOT,hf)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="refine", retriever=vectordb.as_retriever())

    #Web routing Procedures
    # /query
    # /summary
    # /getsections
    # / 
    # errorhandlers
    #
    @app.route("/query",methods=['POST'])
    def queryFAM():
  
        print(f"\n{current_time()}  Processing query")
        data = request.get_json()
        sfam =data.get('fam', '')
        squery = data.get('query', '')
        useremail=data.get('email','')
        qae = qa
        s=datetime.now()  
        answer= queryAI(squery,qae)
        e=datetime.now()  
        qseconds=(e-s).seconds
        s=datetime.now()    
        ref=getReference(answer,qae)
        e=datetime.now()
        rseconds=(e-s).seconds
        tduration=qseconds+rseconds  
        response={"FAM":sfam,"Query":squery,"TotalDuration":tduration,"QueryDuration":qseconds,"ReferenceDuration":rseconds,"Reference":ref,"Answer":answer}
         # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_query = models.Query(email=useremail, query=squery,response=answer, duration=tduration, reference=ref)

        # add the new user to the database
        db.session.add(new_query)
        db.session.commit()

        return response

    @app.route("/summary/<sfam>")
    def getSummary(sfam):     
        fsummary="<h1 align='center'>"+conductor[sfam]["Title"]+"</h1><p>"+conductor[sfam]["Summary"]+"</p><br /><a href='"+conductor[sfam]["Baselink"]+"' target='_blank'>"+conductor[sfam]["Title"]+"</a>"
        return fsummary


    @app.route('/')
    def home():  
        return render_template('chatbox.html')

    @app.errorhandler(NotFound)
    def page_not_found_handler(e: HTTPException):
        return render_template('error.html'), 404

    @app.errorhandler(Unauthorized)
    def unauthorized_handler(e: HTTPException):
        return render_template('error.html'), 401


    @app.errorhandler(Forbidden)
    def forbidden_handler(e: HTTPException):
        return render_template('error.html'), 403


    @app.errorhandler(RequestTimeout)
    def request_timeout_handler(e: HTTPException):
        return render_template('error.html'), 408 
 
    return app


create_app()
