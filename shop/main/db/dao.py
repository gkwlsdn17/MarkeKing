from django.db import connection
import traceback
from .dto import *

class Dao():
    def __init__(self):
        pass

    def getGoodsList(self):
        c = connection.cursor()
        items = []
        try:
                    
            query = f'''
            SELECT main_goods.id, main_goods.NAME, main_goods.PRICE, main_goodstype.NAME
            FROM main_goods join main_goodstype
            ON main_goods.TYPE_id = main_goodstype.id
            ORDER BY main_goods.id DESC LIMIT 10
            '''
            
            res = c.execute(query)
            items = c.fetchall()
        except Exception as e:
            traceback.print_exc()
        finally:
            c.close()
        
        return items

    def getCustomerId(self, userId):
        cursor = connection.cursor()
        cid = ''
        try:

            query = f"SELECT id FROM main_customer WHERE CUSTOMER_ID = '{userId}'"
            cursor.execute(query)
            res = cursor.fetchone()
            cid = res[0]

        except Exception as e:
            traceback.print_exc()
        finally:
            cursor.close()
        
        return cid
    
    def getCustomer(self, userId):
        cursor = connection.cursor()
        customer = None
        try:

            query = f'''SELECT id, CUSTOMER_ID, CUSTOMER_PW, CUSTOMER_NAME, CUSTOMER_BIRTH, CUSTOMER_PHONE, CUSTOMER_EMAIL, CUSTOMER_ZIPCODE, CUSTOMER_ADDR, 
            FIRST_VISIT, LAST_VISIT, VISIT_CNT, CUSTOMER_RATING_id, CUSTOMER_SEX, CRTIME, DISCARD
            FROM main_customer WHERE CUSTOMER_ID = "{userId}" AND DISCARD != 1;'''
            cursor.execute(query)
            res = cursor.fetchone()
            if res:
                customer = Customer(*res)

        except Exception as e:
            traceback.print_exc()
        finally:
            cursor.close()
        
        return customer

    def insertOrder(self, cid, orderDate, amount):
        c = connection.cursor()
        result = False
        try:
            query = f'''INSERT INTO main_order(CUSTOMER_NO_id, ORDER_DATE, TOTAL_AMOUNT, MEMO, CRTIME, DISCARD) 
            VALUES({cid}, '{orderDate}', {amount}, '', datetime('now','localtime'), false);
            '''
            c.execute(query)
            result = True
        except Exception as e:
            traceback.print_exc()
        finally:
            c.close()

        return result
    
    def getOrderId(self, cid, orderDate):
        c = connection.cursor()
        oid = None
        try:
            query = f"SELECT id FROM main_order WHERE CUSTOMER_NO_id = {cid} AND ORDER_DATE = '{orderDate}'"
            c.execute(query)
            res = c.fetchone()
            oid = res[0]
        except Exception as e:
            traceback.print_exc()
        finally:
            c.close()

        return oid
    
    def insertItem(self, oid, gid, gname, count, price, amount):
        c = connection.cursor()
        result = False
        try:
            query = f'''
            INSERT INTO main_item(ORDER_NO_id, GOODS_NO_id, GOODS_NAME, GOODS_COUNT, PRICE, TOTAL_AMOUNT)
            VALUES ({oid}, {gid}, '{gname}', {count}, {price}, {amount});
            '''

            res = c.execute(query)
            connection.commit()
            print('item save ok')
            result = True

        except:
            traceback.print_exc()
        finally:
            c.close()
        
        return result
    
    def insertDelivery(self, oid, cid, dname, daddr, dphone):
        c = connection.cursor()
        result = False
        try:
            query = f'''
            INSERT INTO main_delivery(ORDER_NO_id, CUSTOMER_NO_id, DELIVERY_NAME, DELIVERY_ADDR, DELIVERY_PHONE, CRTIME, DISCARD)
            VALUES ({oid}, {cid}, '{dname}', '{daddr}', '{dphone}', datetime('now','localtime'), false);
            '''
            res = c.execute(query)
            connection.commit()
            print('delivery save ok')
            result = True

        except:
            traceback.print_exc()
        finally:
            c.close()
        
        return result
    
    def getCustomerIdCount(self, id):
        c = connection.cursor()
        count = -1
        try:
            query = f"SELECT COUNT(*) FROM main_customer WHERE CUSTOMER_ID = '{id}'"
            res = c.execute(query)
            rows = res.fetchone()
            count = rows[0]

        except:
            traceback.print_exc()
        finally:
            c.close()
        
        return count
    
    def insertCustomer(self, id, pw, name, birth, phone, email, zipcode, addr, sex):
        c = connection.cursor()
        result = False
        try:
            query = f'''
            INSERT INTO main_customer(CUSTOMER_ID, CUSTOMER_PW, CUSTOMER_NAME, CUSTOMER_BIRTH, CUSTOMER_PHONE, CUSTOMER_EMAIL, CUSTOMER_ZIPCODE, CUSTOMER_ADDR, CUSTOMER_SEX)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, {sex});
            '''
            res = c.execute(query, (id, pw, name, birth, phone, email, zipcode, addr))
            connection.commit()
            print('save ok')
            result = True

        except:
            traceback.print_exc()
        finally:
            c.close()
        
        return result