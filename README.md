# Custom-Built Serverless Product Inventory REST API using Python and AWS 
A Custom-Built Serverless Product Inventory REST API leveraging AWS Lambda, DynamoDB, and API Gateway to handle inventory management operations efficiently. This project demonstrates a scalable, cost-effective solution for managing product data without the need to manage server infrastructure.

## System Design 
![image](https://github.com/user-attachments/assets/f964b622-5cde-4e68-a453-e4c2aeab4fd8)
User → API Gateway → [IAM: Invoke Lambda] → Lambda → [IAM: Access DynamoDB] → DynamoDB
1. **User Request**: A user sends a request from the frontend to the API Gateway.
2. **API Gateway**: The API Gateway receives the request and securely invokes the Lambda function using an IAM role to ensure it has the proper permissions.
3. **Lambda Function**: The Lambda function processes the request by validating the input, determining the type of operation (e.g., retrieving product details or adding a new product), and preparing the necessary data for the database interaction.
4. **DynamoDB Interaction**: The Lambda function interacts with DynamoDB to perform the database operations (reading product details, adding a new product, updating existing data) using its own IAM execution role for secure access.
5. **Response Generation**: Once the database operation is complete, the Lambda function generates a response with data and confirmation.
6. **Response Delivery**: The response is sent back to the API Gateway, which formats and delivers it to the user.

## Serverless APIs vs Server-Based (traditional) APIs 
When designing an API, one of the biggest decisions is choosing between serverless and server-based (traditional) architectures. Both have their pros and cons, but the right choice depends on your use case and priorities.

### Serverless API:
Serverless APIs are simple and scalable. AWS manages the servers for you, so you can focus on your application logic. No provisioning, no configuration, no updates. They scale automatically based on demand and you only pay for what you use. So, the biggest upside: you aren’t required to manage your own infrastructure and it’s often cheaper than needing to pay for maintenance of your own server. 
Downsides of Serverless APIs:
* **Cold Starts**: Idle functions take longer to respond initially, causing slight delays for users.
* **Time Limits**: Functions can’t run longer than 15 minutes and it’s not ideal for heavy processing tasks.
* **Vendor Lock-In**: Serverless solutions are tightly integrated with specific cloud providers, making migrations to another platform more difficult.
* **Debugging**: Distributed architecture can make debugging more challenging, so it’s important to have someone familiar with cloud services to troubleshoot and resolve issues.
* **High Traffic Costs**: While serverless can save money in most cases, it can become very expensive if your app handles consistently high traffic and isn’t optimized for cost efficiency.
* **Lack of Environment Control**: Serverless doesn’t provide full control over the underlying environment like server-based can, making customization or fine-tuning very difficult.

### Which to Choose?
If you’re looking for a scalable, cost-effective solution with minimal infrastructure management, serverless is the way to go. It’s especially useful for dynamic, event-driven applications or projects with unpredictable traffic. On the other hand, if you need complete control over the environment or have highly specific requirements, a server-based approach might make more sense. You should choose serverless if you want to simplify the architecture, reduce latency, and plan on scaling the size of your data, and that’s what this project covers. 

## Use Cases 
This serverless REST API is designed to handle CRUD operations (Create, Read, Update, Delete) in a scalable and cost-effective way, making it perfect for managing dynamic data-driven applications. 
I designed this instance as a centralized inventory management system, where users can add new products, retrieve product info, update inventory levels, and delete outdated entries. 

And though this project was made for that purpose, it can also be easily adapted to other systems like user account management for SaaS platforms to handle user profiles and user settings. It can serve as any great backbone for any application that requires structured data manipulation while having the benefit of not needing to manage your own servers. It can make your architecture more reliable, low latency, and scalable. 

## How It Works 
First, open up the Postman Desktop app to run the API. Enter in the URL for your API that you can find in the API Gateway console on AWS, and then add on the path (like /health or /product) to interact with the API and make calls to it. 

It's a good idea to first check the health of your API and running into errors later that are hard to pinpoint. You can do that by using GET with the /health path and when you see 200 OK, that means your API is healthy and good to go. 
![Untitled design](https://github.com/user-attachments/assets/b906e3a1-3130-4008-bd64-3955b0805dcc)

Add products into your database with different details on each of them with POST. 
![post](https://github.com/user-attachments/assets/9e3f17c1-d39c-460c-baea-76779f54fbb6)

Retrieve info on your items with GET or pull all of the info on every item in your database by changing the path to /products.
![get-products](https://github.com/user-attachments/assets/bf7d5072-7e7a-4e02-bd8d-90601199e42a)

Update info on items with PATCH 
![patch](https://github.com/user-attachments/assets/a8ca57c5-3f52-4bb8-a3c4-3ee8dfbc42b5)

DELETE an item by entering in the productID.
![delete](https://github.com/user-attachments/assets/9b3f4611-c5b4-4abd-a1c9-712483ed96c5)

## Step-By-Step Instructions 
If you came across this wanting to make a serverless API similar to this one, you can follow along with the step-by-step-instruction file that I’ve attached next to the code. 

### What you’ll need: 
* [AWS free tier account](https://aws.amazon.com/free/)
* [Postman desktop app](https://www.postman.com/downloads/)
* The 2 Python files in this repo for the Lambda function

> [!IMPORTANT]
> But first note: </br>
> 1. **AWS Charges**: Even on the free tier, there are limits to usage, and you should still be monitoring your API Gateway and Lambda usage. Once you go over:
>  - 1 million requests or 400,000 GB for AWS Lambda
>  - 1 million HTTP API calls for Amazon API Gateway
>  - 25 GB of storage or 2.5 million read/write requests </br></br>
> at some point within a month, you’ll be charged. With AWS, you get charged for what you use. But this exceedance only really happens if you’re using this project heavily, like for a business. </br>
> 2. **CloudWatch Logs is your best friend**: It is 99.9% of the time going to be an error from the Lambda function code. Learning how to use this AWS service can save you a lot of time. </br>
> 3. **Cleanup**: Delete resources (API Gateway, Lambda function, and DynamoDB tables) when you're done to avoid additional charges.

![navigating-aws](https://github.com/user-attachments/assets/cec4f1c0-d835-4868-bb01-cc04d21a22fd)
![delete-api-gateway](https://github.com/user-attachments/assets/37246951-ae06-4f6e-9095-76c7a0f63408)
![delete-lambda-function](https://github.com/user-attachments/assets/b7d3b678-2641-4b04-9c69-783da8766dd7)
![delete-dynamodb](https://github.com/user-attachments/assets/3d38a754-8c65-4740-ac5a-23c631d8f78c)



## Troubleshooting 
* It is 99.999% of the time going to be an error from the Lambda function code, or at least it was in my experience.
  - When this happens, check CloudWatch logs first. It can immediately tell you things like if you had a typo in your Lambda function or if the function didn’t receive the expected input like missing httpMethod/path keys or if the function failed to connect to DynamoDB in the first place.
  - Test Mock Data in the Lambda Test feature that’s underneath the ‘Deploy Lambda Code’ button. This was the test I used when I had issues with 
    * { "httpMethod": "GET", "path": "/", "queryStringParameters": null, "body": null }
    * It (1) checks if the Lambda function is receiving and processing the event properly and (2) confirms that your function returns the correct response for the root path (/).
    * You’ll know it works when the status code in the response is ‘200 OK’ and the response body contains the working message we put in the code ‘API is working’
* Another issue to watch for would be incorrect formatting.
  - You could have incorrect file structure in your API, meaning you’d need to go to API Gateway and verify your resources match the paths you’re trying to call.
  - You may have issues with DynamoDB, such as missing or incorrect primary keys, which could cause your Lambda function to fail when querying or updating the database.
  - You could also possibly have errors in Postman from incorrect JSON syntax (e.g., missing quotes/commas, mismatched brackets, sending invalid JSON in the request body) or forgetting to change the path when you’re performing a different operation (e.g., still using /products but you wanted to DELETE). 
*	CORS Issues: When creating your resources for your API in API Gateway, always check off ‘Enable API Gateway CORS.’ This is what’s allowing your API to handle requests from different origins (your frontend or Postman). 
*	200 OK – Good: Your API is working. 
* 400 Error – Resource not found:  Issue with the request (incorrect path, missing parameters). Check API Gateway. 
* 500 Error – Internal server error: Issue with the Lambda function. Check CloudWatch logs.

Good luck! This project is great for learning how to create your own serverless API, work with Event-Driven Architecture, and see how Lambda interacts with other AWS Services. It’s a lot of fun and it can branch out into a lot of other different projects. You could easily make this into a project management system or an expense tracker. 
