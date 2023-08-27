import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='pandeyji_eatery'
)

def get_order_status(order_id: int):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f'SELECT status FROM order_tracking WHERE order_id = %s'
    cursor.execute(query, (order_id,))

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result is not None:
        return result[0]
    else:
        return None

def insert_order_item(food_item, quantity, next_order_id):
    try:
        cursor = cnx.cursor()

        # calling thestored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, next_order_id))

        # committing the changes
        cnx.commit()

        #closing the cursor
        cursor.close()

        print("Order item inserted successfully!")
        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item:{err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occured:{e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

def next_order_id():
    cursor = cnx.cursor()

    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]

    cursor.close()

    # return next available order_id
    if result is None:
        return 1
    else:
        return result+1

def get_total_order_price(order_id):
    cursor = cnx.cursor()

    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()

    return result

def insert_order_tracking (order_id, status):
    cursor = cnx.cursor()

    query = "INSERT INTO order_tracking(order_id, status) VALUES (%s, %s)"
    cursor.execute(query, (order_id, status))
    cnx.commit()

    cursor.close()