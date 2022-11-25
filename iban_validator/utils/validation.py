import re
from abc import ABC, abstractmethod
from ..models import IBANFormat, IBANCountry, IBANAlgorithm, IBANCountryChar


class IBANValidationStatus:
    code: int
    message: str
    
    def __init__(self, code:int, message:str):
        self.code = code
        self.message = message
        
    def __str__(self):
        return f'{self.code}: {self.message}'


class ValidatorStrategy(ABC):
    
    @abstractmethod
    def validate_iban(self, iban: str):
        """ Validate IBAN """  


class IBAN:
    raw_iban:       int
    country_code:   str
    
    algorithm:      ValidatorStrategy
    country:        IBANCountry
    format:         IBANFormat
    chars:          dict
    
    def __init__(self, iban: str):
        self.raw_iban = iban[2:]
        self.country_code = iban[0:2]
    
    def general_validation(self) -> IBANValidationStatus:
        """ Validate the IBAN format """     
        
        # Check if country code contains only characters
        if bool(re.search(r'\d', self.country_code)):
            status = IBANValidationStatus(
                400, 'Error Bad Request: Country code should not contain digits'
            )
            return status
        
        # Check if country code exist
        country = IBANCountry.query.filter_by(code=self.country_code.upper()).all()
        if not country:
            status = IBANValidationStatus(
                404, 'Error Not Found: IBANCountry not Found in database'
            )
            return status
        self.country = country[0]
        
        # Check if country chars exist in DB
        country_chars = IBANCountryChar.query.filter(
            IBANCountryChar.char.in_([char.upper() for char in self.country_code])
        ).all()
        if len(country_chars) != 2: # should make check <2> more generic
            status = IBANValidationStatus(
                404, 'Error Not Found: IBANCountryChar not Found in database'
            )
            return status
        self.chars = {
            country.char: 
                country.value for country in country_chars
        }
        
        # Check if IBAN format for country exist
        ibanformat_obj = IBANFormat.query.filter_by(country=self.country.id).all()
        if not ibanformat_obj:
            status = IBANValidationStatus(
                404, 
                f'''Error Not Found: IBANFormat not 
                Found for country: {self.country.name} in database'''
            )
            return status
        self.format = ibanformat_obj[0]
        
        # Check if IBAN algorithm exist
        algorithm_obj = IBANAlgorithm.query.filter_by(
            id=self.format.iban_algorithm
        ).all()
        if not algorithm_obj:
            status = IBANValidationStatus(
                404, 'Error Not Found: IBANCountry not Found in database'
            )
            return status
        self.algorithm = iban_conf[algorithm_obj[0].name]
        
        # Check if IBAN length is valid
        if len(self.raw_iban) + len(self.country_code) != self.format.total_len:
            status = IBANValidationStatus(
                400, 
                f'''Error Bad Request: Length of characters is 
                invalid for country: {self.country.name}'''
            )
            return status
         
        status = IBANValidationStatus(200, 'OK')
        return status
    
    
class ISOMOD97Validator(ValidatorStrategy):       
        
    @staticmethod
    def validate_iban(iban: IBAN) -> bool:
        
        # Check if account part contains only digits
        if iban.raw_iban.isdigit():
            
            iban_validate_number =  int(''.join(
                [
                    iban.raw_iban[iban.format.len_check_digits:],
                    str(iban.chars[iban.country_code[0]]), 
                    str(iban.chars[iban.country_code[1]]), 
                    iban.raw_iban[0:iban.format.len_check_digits]
                ]
            ))
            
            # Compute ISO 7064 MOD-97-10
            if iban_validate_number % 97 == 1:
                return True
        return False
        
        
iban_conf = {
    'ISO 7064 MOD-97-10': ISOMOD97Validator
}
