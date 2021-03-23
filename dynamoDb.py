import boto3
from boto3.dynamodb.conditions import Key
import json

dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIAJXXXXXXXXXXXXXX2RKIDRA" , aws_secret_access_key="eYiNe8rjd4s0XXXXXXXXXXXXXticxZMK", region_name="us-east-1")
def get_price_with_name(item_name, iten_type):
    table = dynamodb.Table('allitems')

    response = table.query(
        KeyConditionExpression=Key("item_type").eq(iten_type)
    )
    results = response['Items']
    items = [x for x in results if x["item_name"] == item_name]  # list
    if len(items) > 0:
        return (items[0]["item_name"], items[0]["price"], items[0]["preview_image"])
    return "0"

def get_price_with_barcode(barcode_number, iten_type):
    table = dynamodb.Table('allitems')

    response = table.query(
        KeyConditionExpression=Key("item_type").eq(iten_type)
    )
    results = response['Items']
    items = [x for x in results if x["barcode_number"] == barcode_number]  # list
    if len(items) > 0:
        return (items[0]["item_name"], items[0]["price"], items[0]["preview_image"])
    return "0"

def get_existing_record(id, cart_number):
    table = dynamodb.Table('usercarts')

    response = table.query(
        KeyConditionExpression=Key("cart_number").eq(cart_number)
    )
    results = response['Items']
    items = [x for x in results if x["item_name"] == id]  # list
    if len(items) > 0:
        return items[0]
    return None 

def put_user_cart(id, cart_number, item_type):
    price = 0
    image = ""
    item_name = ""
    if item_type == "FruitsAndVegitables":
        item_name,price,image = get_price_with_name(id, item_type)
    else:
        item_name,price,image = get_price_with_barcode(id, item_type)

    if float(price) <= 0:
        return
    existing = get_existing_record(item_name, cart_number)
    table = dynamodb.Table('usercarts')
    if existing is not None:
        response = table.update_item(
            Key={
                'item_name': existing["item_name"],
                'cart_number': cart_number,
            },
            UpdateExpression="set quantity = :q",
            ExpressionAttributeValues={
                ':q': existing["quantity"] + 1,
            },
            ReturnValues="UPDATED_NEW"
        )
    else:
        response = table.put_item(
        Item={
                'item_name': item_name,
                'cart_number': cart_number,
                "quantity": 1,
                "preview_image": image,
                "price":price
            }
        )
    return response
