# Building a chatbot | End-to-End-NLP-project
This project is creating a chatbot using the Dialog Flow platform.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## requirements:</br>
              Dialog Flow 
              MySQL Workbench
              fastapi[all]  => (Backend) 
              mysql-connector-python
              ngrok  ==>  (to create a secure connection) 
              HTML and CSS (Web page implementation)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Introduction : </br>
The main focus of this project is to build a chatbot for a company called "Food Truck". Food Truck is an online food delivery company.
In this case, the chatbot helps customers place an order and track an order.
   #### Key Features: </br>
         Natural language understanding
         Order placement and Tracking
         Menu Exploration
         Order history and reordering
         Calculation of the total amount
## Technologies and Tools
### 1) Dialogflow  : 
      Dialogflow is a natural language processing platform developed by Google. 
      It helps to create intelligent and interactive conversational interfaces.
         
#### Intents      :   
    Intents are used to understand the user's intention or request. 
    
          - Default Welcome Intent
          - Default Fallback Intent
          - new.order
          - order.add- context: ongoing order
          - order.remove - context: ongoing order
          - order.complete - context: ongoing order
          - track.order
          - track.order - context: ongoing-tracking
           

#### Entities     : 
     Entities are used to extract specific information from user input.
     - food-item
     - number (food quantity)

#### Contexts     :
     Contexts in Dialogflow help to maintain the conversation's context over multiple interactions.
     - ongoing order
     - ongoing tracking

#### Fulfillment  :
    The capabilities of the Dialogflow chatbot can be extended using the fulfillment option by integrating 
    it with external services and APIs. For that, the webhook mechanism is used. That allows Dialogflow to '
    send a request to a designated URL, whenever a specific intent is matched. This URL should be in HTTPS 
    format to make a secure connection. 
 
#### Webhook      :
     Dialogflow can be connected to external APIs through webhooks. This option enables chatbots to fetch 
     real-time information and perform actions beyond the built-in capabilities. 
     
     Here I enabled the webhook option for some intents:
      - new.order
      - order.add- context: ongoing order
      - order.remove - context: ongoing order
      - order.complete - context: ongoing order
      - track.order - context: ongoing-tracking

#### Integration    :
  Dialogflow can be integrated with various platforms, including websites. 
  messaging apps, and voice platforms. In this project, I integrated it with the website.


### 2) Backend       :
     I implemented the backend code using the Python FastAPI in PyCharm. 
     I implemented it in three files.  
   
         - Main             ==>  Handle the request and extract the required details from the payload. 
                                 functions for different intents(add, remove, complete, track order).
                                 
                                 libraries:  from fastapi import Request
                                             from fastapi.responses import JSONResponse
                             
         - db_handler       ==>  This handles the database. 
                                - Inserting order item
                                - get_order_status
                                - get next_order_id
                                - get_total_order_price
                                - insert_order_tracking
                                
                                  libraries: import mysql.connector
                                             global cnx
          
         - generic_helper   ==> This is used to extract some of the required data from 
                                the payload (.JSON file). Also used to transform some of the data.

                                libraries: import re              

### 3) Database setup: 

    The completed order and status of the order are stored in MySQL. 
             Tables            ==> - Food items
                                   - Order tracking
                                   - Orders
             Stored procedures ==>   Insert_order_item

             Functions         ==> - get_price_for_item
                                   - get_total_order_price
 
### 4) Frontend      :

The website is created using HTML and CSS. The attachment code can be obtained from the 
web demo in the integration section. This code will integrate the chatbot with the website. 
So I attached that code to the HTML file and did some alternations as well. By default,
the chatbot doesn't have a minimization and maximization facility.
I created a toggle button to minimize and maximize the chatbot.

## Architecture and Flow : </br>


            when the user says starting phrases. (e.g.: hi, hey ) 
            The chatbot will ask if you want to order something or track your order.
            
            IF reply is new order ===> Add order from Menu ====> Remove anything if wanted
            ===> complete order ===> order will be stored in the database.
            
            If the reply is track order ==> chatbot will ask for order ID ==>  backend  
            ===> database ==> status of the order ==> backend 
            ===> shows the status of the order in the chatbot.

            If the user input is a new order while ordering something the system needs to erase
            past order and need to create a new list.

## Implementation Details


           => Create a new agent in the Dialogflow. 
           => Add intents  and entities.
           => Enable webhook for required intents.
           => Implement backend code using fastapi.
           => convert the URL HTTP --> HTTPS format using ngrok.exe. (aware of active time of ngrok
              that can only provide service for nearly 2 hours).
           => Paste that URL in the fulfillment section of DialogFlow.
           => Create a database in the MySQL workbench.
           => Connect the database to Python.
           => Check the operation of the chatbot.
           => Create a web interface.
           => Integrate the chatbot with the website.
           
              
            









              
              
              
              
                
