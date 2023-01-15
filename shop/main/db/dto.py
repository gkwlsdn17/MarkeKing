from dataclasses import dataclass
from datetime import *

@dataclass
class Customer():
    id : int
    CUSTOMER_ID : str
    CUSTOMER_PW : str
    CUSTOMER_NAME : str
    CUSTOMER_BIRTH : str
    CUSTOMER_PHONE : str
    CUSTOMER_EMAIL : str
    CUSTOMER_ZIPCODE : str
    CUSTOMER_ADDR : str
    FIRST_VISIT : date
    LAST_VISIT : date
    VISIT_CNT : int
    CUSTOMER_RATING : int
    CUSTOMER_SEX : int
    CRTIME : date
    DISCARD : bool
    
@dataclass
class Rating():
    id : str
    NAME : str
    ORDER : int
    DISCARD : bool