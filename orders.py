import requests

import mysql.connector 
import json
import random
import logging

#from Create_customer import customer_name

# Check if a customer exists 

def get_customer_details(cust_id):
    cntr = 0
    LOG_FILENAME = 'orders.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    
    logging.debug('we are getting into customer details')
    print("About to connect")
    cnx = mysql.connector.connect(user='xxxx', password='xxxx',
                              host='<your database host>',
                              database='<your database name>')
    cursor = cnx.cursor()
    #cust_id = input("Enter the id of the Customer your want to Search for ")
    query = ("Select customer_name from customer_details where cust_id = " +cust_id)
    cursor.execute(query)
    for (customer_name) in cursor:
        print("{}".format(customer_name))
        cntr = cntr +1 # reset customer cntr to 1 to indicate customer exsist
        print ("Counter Value " + str(cntr))
        logging.debug('Counter  Value' + str(cntr))

    if cntr == 0: # if the customer does not exist then return null
        print("Customer Does not exist")
        logging.debug('we are getting into customer details')
        return 0
    else:        # if they do exist then return the name of the customer
        return customer_name
    cursor.close()    
    cnx.close()
    # we are returning a customer name
    



# This is to create a new customer, it takes customer name, customer address and customer phone as varaibles
# returns the newly created customer id

def create_customer(customer_name, customer_add, customer_ph):
    customer_name= customer_name
    customer_add = customer_add
    customer_ph = customer_ph
    max_cust_id = 0
    
    cnx2=mysql.connector.connect(user='xxxx', password='xxxx',
                              host='<Your database host name',
                              database='your database name')
    
    cursor2=cnx2.cursor()
    query = ("Select max(cust_id) from customer_details")
    cursor2.execute(query)
    for(cust_id) in cursor2:
        max_cust_id = max(cust_id) +1 
        #print ("Max Customer Id" + str(max_cust_id))
        #print ("Max Customer {}".format(cust_id))
    
    add_customer= ("insert into customer_details"
                   "(cust_id, customer_name, cusotmer_address,customer_phone)"
                   "VALUES(%(cust_id)s, %(customer_name)s, %(cusotmer_address)s, %(customer_phone)s)")
    
    customer_data = {
        'cust_id': max_cust_id,
        'customer_name': customer_name,
        'cusotmer_address': customer_add,
        'customer_phone': customer_ph
        }
    
    cursor2.execute(add_customer,customer_data)
    cnx2.commit()
    cursor2.close()
    cnx2.close()
    return max_cust_id 

# This is takes the customer id and provides details of orders associated with the customer 
# we are just returning the last tupple .... need to fix that but not critical for what we want to do
def get_order_details(cust_id):
    
    order_cntr = 0 # will be used to check to naviagte if order exists
    cnx = mysql.connector.connect(user='xxxx', password='xxxxx',
                              host='<your database host>',
                              database='yourdatabase name')
    cursor = cnx.cursor()
    
    find_order = ("Select order_item, order_value from order_detail where cust_id = " + cust_id)
    cursor.execute(find_order)
    
    #order_json = json.dumps(find_order)
    
    for(order_item, order_value) in cursor:
        print("{},{}".format(order_item, order_value))
        order_cntr = order_cntr +1
        
    #check if any order of that number actually exists,else return 0
    if order_cntr==0:
        return 0,0
    else:
        return order_item, str(order_value)
    cursor.close()
    cnx.close()
    
#creates an order for a customer with a specific item and prince 
#returns 0 if the customer does not exist, else returns the order id created 
def create_order(cust_id, order_item, order_value):
    cnx = mysql.connector.connect(user='xxxx', password='xxxx',
                              host='<your host name>',
                              database='your database name')
    cursor_outer = cnx.cursor()

#We are going to check if the customer we want to create an order for exits 
    query_outer= ("Select customer_name  from customer_details where cust_id=" + str(cust_id))
    print ("My query String " + query_outer)
    customer_exists = "None"
    cursor_outer.execute(query_outer)
    

    
    for (customer_name) in cursor_outer:
        customer_exists = customer_name
    else:
        customer_exists = "None"

    print ("Customer exists: " + customer_exists)
# If the customer does not existm then return 0    
    if customer_exists!= "None": #thsi is not working properly should == None but can't get it to work
        print("The Customer you entered does not exist, Please create customer first")
        cursor_outer.close()
        cnx.close()
        return 0
#if the customer exists then create order and return order id
    else:
        cursor = cnx.cursor()
        max_order_id = 0
        query = ("Select max(order_id) from order_detail")
        cursor.execute(query)
        for(order_id) in cursor:
            max_order_id = max(order_id)
            print ("Max Order Id" + str(max_order_id))
        
        cursor.close()
        
        add_order= ("insert into order_detail"
                       "(order_id, cust_id, order_item, order_value)"
                       "VALUES(%(order_id)s, %(cust_id)s, %(order_item)s, %(order_value)s)")
        
        order_data = {
            'order_id': max_order_id + 1,
            'cust_id': cust_id,
            'order_item': order_item,
            'order_value': order_value
            }
        cursor = cnx.cursor()
        cursor.execute(add_order,order_data)
        cnx.commit()
        cursor.close()
        cursor_outer.close()
        cnx.close()
        return max_order_id+1

#creates a shipment based on an order number and shipper 
#returns shipment_id created and -- tbd 0 if order does not exist in the system
def create_shipment(order_id, shipper_nm):
    
    max_ship_id = 0 # variable used for manipulating next ship id 
    cnx = mysql.connector.connect(user='xxxx', password='xxxx',
                              host='<your database host>',
                              database='your database name')
    cursor = cnx.cursor()
    cursor_outer = cnx.cursor() # this cursor is just to check if the order exists
    query_outer = ("Select order_item from order_detail where order_id=" + str(order_id))
    cursor_outer.execute(query_outer)
    
    order_exists = "None" # variable to check if order exists
    
    for (order_item) in cursor_outer: # set order exists to 1 if the order exists
        order_exists = order_item
        print("order Item" + str(order_item))
        print ("Order Exists" + str(order_exists))
        
    if order_exists == "None": # if the order does not exist return 0 
        print("This order Id Does not exist")
        return 0
    else:                 # else create shipment and return the ship id that was created 
        rand_tracking_num = random.randint(1,1000)*4 # create a generic tracking number based on randon numbers
        #max_ship_id = 0 moved to a variable more global in nature 
        query = ("Select max(ship_id) from shipment_details")
        cursor.execute(query)
        for(ship_id) in cursor:
            max_ship_id = max(ship_id) +1 
            #print ("Max Order Id" + str(max_order_id))
        
        cursor.close() # close out the cursor
        add_ship= ("insert into shipment_details"
                       "(ship_id, order_id, shipper, tracking_number)"
                       "VALUES(%(ship_id)s, %(order_id)s, %(shipper)s, %(tracking_number)s)")
        
        ship_data = {
            'ship_id': max_ship_id,
            'order_id': order_id,
            'shipper': shipper_nm,
            'tracking_number': rand_tracking_num
            }
        cursor = cnx.cursor() #create a new cursor 
        cursor.execute(add_ship,ship_data)
        cnx.commit()
        cursor.close()
    cursor_outer.close() # close out the outer cursor as well 
    cnx.close()
    return max_ship_id

# This used to be the main function for the monlith that privided the required navigation. Is depreciated because all the functions have now been converted to APIs
#This is still used to test the code out 
def main_function(): 
    
    choice = input("Enter What you want to do (1: Get Customer Details, 2: Create New Customer, 3: Get Order Deails, 4: Create New Order, 5: To create a New Shipment")
    
    if choice == '1':
        cust_id = input("Enter the id of the customer you want to look up")
        get_customer_details(cust_id)
    
    elif choice == '2':
        customer_name= input("Provide Customer Name: ")
        customer_add = input ("Enter Customer Address")
        customer_ph = input ("Enter Customer Phone")
        create_customer(customer_name, customer_add, customer_ph)
        
    elif choice == '3':
        cust_id = input("Enter Customer Id for the customer you want to find orderse for: ")
        order_details = get_order_details(cust_id)
        print(order_details)
        
    elif choice == '4':    
        create_new_order = input("Do you want to create a new Order (Y/N): ")
        if create_new_order == 'Y':
            order_cust_id = input ("Enter the customer id for who you want to create an order ")
            order_item = input("Enter the Item you want to order :")
            order_value = input ("Price of the Item: ")
            created_order_id = create_order(order_cust_id,order_item, order_value)
            print("Order was created with Id " + str(created_order_id))
        else:
            print("Looks like you don't want to create a new order. Bye! ")
    
    elif choice == '5':
        create_new_shipment = input("Do you want to create a new Shipment")
        if create_new_shipment == 'Y':
            ship_order_id = input('Enter the order id for which you want to create a shipment')
            shipper = input("Enter the shipper of your choice")
            ship_id_created = create_shipment(ship_order_id, shipper)
            print("Shipment was created with the id" + str(ship_id_created))
        else:
            print("Looks like you dont want to create a shipment. Bye!")
    else:
        print("Please Enter a valid choice")
    
    
    #print("Thanks for using my monolith")

#print("Starting the Main function")
#main_function()
#print("I am done with the program")

#create_shipment(1005, 'USPS')
    
