# -*- coding: utf-8 -*-
import os
from os.path import join, dirname

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ['SQLALCHEMY_URI'], pool_recycle=3600)

db_session = scoped_session(
        sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=engine)
        )


#==================================================================

# ssl_args = {
#     "ssl":{
#         "ca": os.path.join(os.environ['SSL_PATH'], os.environ['SSL_CA']), 
#         "cert": os.path.join(os.environ['SSL_PATH'], os.environ['SSL_CERT']), 
#         "key": os.path.join(os.environ['SSL_PATH'], os.environ['SSL_KEY']) , 
#         "check_hostname": False
#         }
#     }

#print(os.environ['SQLALCHEMY_SSL_URI'])
#print(ssl_args)
#engine_ssl = create_engine(os.environ['SQLALCHEMY_SSL_URI'], connect_args=ssl_args, pool_recycle=3600)
#db_session = scoped_session(
#        sessionmaker(
#            autocommit=False, 
#            autoflush=False, 
#            bind=engine_ssl)
#        )
