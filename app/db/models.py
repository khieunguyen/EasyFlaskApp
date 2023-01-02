# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

from flask_login import UserMixin

class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(BIGINT(20), primary_key=True)
    email = Column(String(128))
    password = Column(String(128))
    name = Column(String(45))
    status = Column(String(45), server_default=text("'pending'"), comment='Active: Active user\\nPending: Pending user waiting for activate\\nDeleted: Deleted user that no longer available for login')
    otp_secret = Column(String(45))
    otp_status = Column(String(45), server_default=text("'disable'"), comment='Disable: do not use 2FA verification, \\nEnable: 2FA verification enabled, \\nPending: waiting for setting up 2FA verification')
    created_at = Column(TIMESTAMP)
    created_by = Column(String(45), server_default=text("'System'"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
