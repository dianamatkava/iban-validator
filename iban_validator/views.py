import json

from flask import Blueprint, render_template
from flask.json import jsonify
from .utils.validation import IBAN


ibanb = Blueprint('', __name__, url_prefix='/')


@ibanb.route('/', methods=['GET'])
def main():
    return render_template('iban-validation.html')


@ibanb.route('/validate-iban/<client_iban>', methods=['GET'])
def validateIBAN(client_iban:str) -> json:
    
    if client_iban and len(client_iban) > 2:
        # Instantiate IBAN instance
        iban = IBAN(client_iban)
        
        # Make a pre-validation of IBAN format
        status = iban.general_validation()
        print(f'IBAN Pre Validation status: {status}')
        
        if status.code == 200:
            # Instantiate Validator instance
            validator = iban.algorithm()
            
            # Validatin IBAN
            validation_status = validator.validate_iban(iban)
            print(f'IBAN Validation status: {validation_status}')
            
            return jsonify(**{
                    'status': status.code, 
                    'iban': client_iban,
                    'message': validation_status
                })

        return jsonify(**{
            'status': 400, 
            'iban': client_iban, 
            'message': status.message
        })

    return jsonify(**{'status': 404, 'message': 'Please provide a valid IBAN'})

# - - - - - -  TEST - - - - - - -#

# IBAN_CONF = {
#     "COUNTRY_NAME": "Montenegro", 
#     "COUNTRY_CODE": {
#         "ME": 2214,
#     },
#     "CHECK_DIGITS": 2,
#     "BANK_CODE": 3,
#     "ACCOUNT_NUMBER": 13,
#     "NATIONAL_CHECK_DIGITS": 2,
#     "TOTAL_LENGTH": 22
# } 


# def validateIBAN(iban:str='me75533213213429672753') -> bool:
    
#     # Check if length is valid
#     if len(iban) == IBAN_CONF['TOTAL_LENGTH']:
#         country_code = iban[0:2].upper()
        
#         # Check if country code valid and exist
#         if not country_code.isdigit() \
#             and IBAN_CONF['COUNTRY_CODE'].get(country_code.upper(), False):
                    
#             # Check if account part contains only digits
#             if iban[2:].isdigit():
#                 account_number =  iban[4:] + str(IBAN_CONF['COUNTRY_CODE'][country_code]) + str(iban[2:4])
                
#                 # Compute ISO 7064 MOD-97-10
#                 if int(account_number) % 97 == 1:
#                     return True
    
#     return False

# print(validateIBAN())


