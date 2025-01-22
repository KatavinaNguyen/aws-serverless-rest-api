import boto3
import json
import logging
from custom_encoder import CustomEncoder

# Set up logging for the Lambda function
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the DynamoDB resource and specify the table
dynamodbTableName = 'product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

# HTTP Methods and API Paths
getMethod = 'GET'
postMethod = "POST"
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthPath = '/health'  # Endpoint to check API health (200=good/API is alive, 500=internal server error/API is down)
productPath = '/product'  # Endpoint for individual product operations
productsPath = '/products'  # Endpoint to fetch all products

def lambda_handler(event, context):
    """
    Main Lambda function handler. Routes incoming HTTP requests to the appropriate function
    based on the HTTP method and request path.
    """
    logger.info(event)  # Log the incoming event for debugging
    httpMethod = event.get('httpMethod')
    path = event.get('path')

    # Lambda function test to confirm that it's correctly handling requests to the root / path
    if path == "/":
        return buildResponse(200, {"message": "API is working!"})

    # Match the HTTP method and path to the corresponding operation
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == productPath:
        response = getProduct(event['queryStringParameters']['productPath'])
    elif httpMethod == getMethod and path == productsPath:
        response = getProducts()
    elif httpMethod == postMethod and path == productPath:
        response = saveProduct(json.loads(event['body']))
    elif httpMethod == patchMethod and path == productPath:
        requestBody = json.loads(event['body'])
        response = modifyProduct(requestBody['productID'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == productPath:
        requestBody = json.loads(event['body'])
        response = deleteProduct(requestBody['productID'])
    else:
        # Handle unmatched paths or methods with a 404 error
        response = buildResponse(404, 'Not Found')
    return response

def getProduct(productID):
    """
    Fetches a product by its ID from the DynamoDB table.
    """
    try:
        response = table.get_item(
            Key={
                'productID': productID
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'ProductID: %s not found' % productID})
    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        return buildResponse(500, {'error': 'Unable to fetch product'})

def getProducts():
    """
    Fetches all products from the DynamoDB table.
    """
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStarKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'products': result
        }
        return buildResponse(200, body)
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return buildResponse(500, {'error': 'Unable to fetch products'})

def saveProduct(requestBody):
    """
    Saves a new product to the DynamoDB table.
    """
    try:
        table.put_item(Item=requestBody)
        """
        We're using these 'body' dictionaries to serialize data into a JSON response 
        by the 'buildResponse' function to send it back to the client.
        So 'body' is the response payload, and you could customize this to include 
        a timestamp for example if you wanted, to help with debugging.
        """
        body = {
            'Operation': 'SAVE',  # What's happening in the operation
            'Message': 'SUCCESS',  # Confirm that it was successfully completed
            'Item': requestBody  # This is both the product data saved to DynamoDB and a way to verify data matches request
        }
        return buildResponse(200, body)
    except Exception as e:
        logger.error(f"Error saving product: {e}")
        return buildResponse(500, {'error': 'Unable to save product'})

def modifyProduct(productID, updateKey, updateValue):
    """
    Updates a specific attribute of a product in the DynamoDB table.
    """
    try:
        response = table.update_item(
            Key={
                'productID': productID
            },
            UpdateExpression='set %s = :value' % updateKey,
            ExpressionAttributeValues={':value': updateValue},
            ReturnValues='UPDATED_NEW'  # Return the updated attributes
        )
        """
        We're dynamically setting so that we won't need to hardcode and maintain separate logic for each field.
        It'll make the function more flexible and reusable when the inventory scales with new attributes 
        like 'warehouseLocation' or 'supplierName.
        """
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response
        }
        return buildResponse(200, body)
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return buildResponse(500, {'error': 'Unable to update product'})

def deleteProduct(productID):
    """
    Deletes a product from the DynamoDB table.
    """
    try:
        response = table.delete_item(
            Key={'productID': productID},
            ReturnValues='ALL_OLD'  # Return the deleted item details
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return buildResponse(500, {'error': 'Unable to delete product'})

def buildResponse(statusCode, body=None):
    """
    Helper function to build an HTTP response.
    """
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Allows cross-origin requests, which lets frontends on different domains interact with the API.
        }
    }
    if body is not None:
        # Serialize the response body using a custom encoder
        # because DynamoDB returns decimal numbers but need to be converted when passed to JSON
        response['body'] = json.dump(body, cls=CustomEncoder)
    return response