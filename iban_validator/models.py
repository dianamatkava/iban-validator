from extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, event


class IBANCountryChar(db.Model):
    __tablename__ = 'iban_country_char'
    id = Column(Integer(), primary_key=True)
    char = Column(String(1), nullable=False)
    value = Column(Integer(), nullable=False)

    def __repr__(self):
        return self.char
    
    
class IBANCountry(db.Model):
    __tablename__ = 'iban_country'
    id = Column(Integer(), primary_key=True)
    name = Column(String(225), nullable=False)
    code = Column(String(2), nullable=False)

    def __repr__(self):
        return self.name


class IBANAlgorithm(db.Model):
    __tablename__ = 'iban_algorithm'
    id = Column(Integer(), primary_key=True)
    name = Column(String(225), nullable=False)
    description = Column(String(1500), nullable=True)
    
    def __repr__(self):
        return self.name


class IBANFormat(db.Model):
    __tablename__ = 'iban_format'
    id = Column(Integer(), primary_key=True)
    country = Column(Integer(), ForeignKey(
        'iban_country.id'), nullable=False, unique=True
    )
    total_len = Column(Integer(), nullable=False)
    iban_algorithm = Column(
        Integer(), ForeignKey('iban_algorithm.id'), nullable=False
    )
    len_check_digits = Column(Integer(), nullable=False)
    len_national_bank_code = Column(Integer(), nullable=False)
    len_account_number = Column(Integer(), nullable=False)
    account_type = Column(String(1), nullable=True)
    branch_code = Column(Integer(), nullable=True)
    len_national_check_digit = Column(Integer(), nullable=True)
    
    def __repr__(self):
        return f'{self.country} {self.iban_algorithm}'

    
# Create Inital DB

@event.listens_for(IBANCountryChar.__table__, 'after_create')
def create_iban_country(*args, **kwargs):
    db.session.add(IBANCountryChar(char='M', value='22'))
    db.session.add(IBANCountryChar(char='E', value='14'))
    db.session.commit()


@event.listens_for(IBANCountry.__table__, 'after_create')
def create_iban_country(*args, **kwargs):
    db.session.add(IBANCountry(name='Montenegro', code='ME'))
    db.session.commit()
    
    
@event.listens_for(IBANAlgorithm.__table__, 'after_create')
def create_iban_country(*args, **kwargs):
    db.session.add(IBANAlgorithm(name='ISO 7064 MOD-97-10'))
    db.session.commit()
    

@event.listens_for(IBANFormat.__table__, 'after_create')
def create_iban_country(*args, **kwargs):
    db.session.add(IBANFormat(
        country=IBANCountry.query.filter_by(name='Montenegro')[0].id,
        iban_algorithm=IBANAlgorithm.query.filter_by(name='ISO 7064 MOD-97-10')[0].id,
        total_len=22,
        len_check_digits=2,
        len_national_bank_code=3,
        len_account_number=13,
        len_national_check_digit=2
    ))
    db.session.commit()
