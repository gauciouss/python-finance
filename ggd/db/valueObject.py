from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column,String, Float, Date, Integer


Base = declarative_base()
class StkCompInfo(Base):
    __tablename__ = "stk_comp_info"
    stk_id = Column(String(10), primary_key=True)
    comp_name = Column(String(100))
    isin_code = Column(String(30))
    marketing_date = Column(Date)
    industry_class = Column(Integer)
    market = Column(Integer)
