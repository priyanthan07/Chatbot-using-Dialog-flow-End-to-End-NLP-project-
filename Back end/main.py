from fastapi import Request
from fastapi import FastAPI
import db_handler
from fastapi.responses import JSONResponse
import generic_helper

app = FastAPI()

"""@app.get("/")
async def root():
    return {"message": "mmm nice vro"}"""

inprogress_orders = {}


@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    query_text = payload['queryResult']['queryText']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    intent_handler_dict = {
        'new.order': new_order,
        'order.add- context: ongoing order': add_to_order,
        'order.remove - context: ongoing order': remove_from_order,
        'order.complete - context: ongoing order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }
    return intent_handler_dict[intent](parameters, session_id, query_text)


def new_order(parameters: dict, session_id: str, query_text: str):
    if session_id in inprogress_orders:
        print("***********************you are here")
        del inprogress_orders[session_id]

    else:
        pass


def add_to_order(parameters: dict, session_id: str, query_text: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    # if query_text.find("new order") != -1:
    #     del inprogress_orders[session_id]
    #     print("deleted the ID")

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. can you please specify food items and quantities clearly."
    else:
        new_food_dict = dict(zip(food_items, quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"so far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id: str, query_text: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. sorry! can you place a new order"
        })
    else:
        current_order = inprogress_orders[session_id]
        food_items = [parameters["food-item"]]

        removed_items = []
        no_such_items = []

        for item in food_items:
            if item not in current_order:
                no_such_items.append(item)
            else:
                removed_items.append(item)
                del current_order[item]

        if len(removed_items) > 0:
            fulfillment_text = f"Removed {','.join(removed_items)} from your order"
        if len(no_such_items) > 0:
            fulfillment_text = f"your current order does not have {','.join(no_such_items)}"
        if len(current_order.keys()) == 0:
            fulfillment_text += "Your order is empty"
        else:
            order_str = generic_helper.get_str_from_food_dict(current_order)
            fulfillment_text += f" Here is what is left in your order: {order_str}"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def complete_order(parameters: dict, session_id: str, query_text: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order.Sorry! Can you place a new order"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Sorry,I couldn't process your order due to a backend error. " \
                               "please place a new order again"

        else:
            order_total = db_handler.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order. " \
                               f"Here is your order id # {order_id}. " \
                               f"Your order total is {order_total}, which can pay at the time of delivery"

        del inprogress_orders[session_id]
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order: dict):
    # order ={"Pizza": 2 , "chole":1}
    next_order_id = db_handler.next_order_id()

    for food_item, quantity in order.items():
        rcode = db_handler.insert_order_item(food_item, quantity, next_order_id)
        if rcode == -1:
            return -1
    db_handler.insert_order_tracking(next_order_id, "In progress")

    return next_order_id


def track_order(parameters: dict, session_id: str, query_text: str):
    order_id = int(parameters["number"])
    """if order_id == 40 or order_id == 41:
        order_status = "finished"
    else:
        order_status= None"""

    order_status = db_handler.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order stat us for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



