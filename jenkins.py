'''
Created on May 20, 2018

@author: LONGBRIDGE
'''

import jenkins
import requests
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session
import datetime
from pymysql.constants.ER import REQUIRES_PRIMARY_KEY
from pip._vendor.distlib.compat import raw_input
from pip._vendor.requests.sessions import session
from http import server
from jenkins import JOBS_QUERY, VIEW_JOBS


Base = declarative_base()

def connectToJenkins(url, username,password):
    server = jenkins.Jenkins(url,
     username = username, password = password)
    return server

def  initiateDb():
    #create an engine that stores data in a local directory
    #sqlalachemy Kay.db file
    engine = create_engine('sqlite:///Kay.db')
    session = sessionmaker (bind=engine)()
    #This is equivalent to creating  craeting a table
    Base.metadata.create_all(engine)
    return session

def addjob(session,jlist):
    for j in jlist :
        session.add(j)
        session.commit()
        
    class Jobs(Base):
        _tablename_ = 'Jobs'
        id = column(Integer,primary_key = True)
        jen_id = Column(Integer)
        name = Column(String)
        timeStamp = Column(DateTime)
        result = Column(String)
        building = Column(String)
        estimatedDuration = Column(String)
    
    
def getjobLastId(session,name):
    job = session.query(Jobs).filter_by(name=name).order_by(Jobs.jen_id.desc()).first()
    if(job != None):
        return job.jen_id
    else:
        return None
    
   
        
        
def createJobList(start,lastnumber,jobname): 
    jlist = []
    for i in range(start + 1, lastnumber + 1) :
        current = server.get_build_info(jobname,i)
        current_as_jobs= Jobs()
        current_as_jobs.jen_id = current['id']
        current_as_jobs.building= current['building']
        current_as_jobs.estimatedDuration= current['estimatedDuration']
        current_as_jobs.result= current['result']
        current_as_jobs.name= jobname
        current_as_jobs.timeStamp= datetime.datetime.fromtimestamp(long(current['timestamp'])*0.001)
        jlist.append(current_as_jobs)
        
    return jlist 

 url = 'http://localhost:8080'
 username = raw_input('Enter username :')
 password = raw_input('Enter password : ')
 server = connectToJenkins(url, username,password)
 
 authenticated = False
 try:
     server.get_whoami()
     authenticated = True
except jenkins.jenkinsException as e:
    print ('Authentication error')
    authenticated = False
    
if authenticated :
    session = initiateDb()
    
    #get list o all jobs
     jobs = server.get_all_jobs()
     for j in jobs 
     jobname = j['name']
     lastJobId = getLastJobid(session,jobname)
     lastBuildNumber = server.get_job_info(jobname)['lastBuild']['number']
     
     if lastJobId == None:
       start = 0
       else:
           start = lastJobId
           
           Jlist = createJobList(start,lastnumber,jobname)
           addJob(session,Jlist)
    
 
 
        
        
        
        
        
    
    
