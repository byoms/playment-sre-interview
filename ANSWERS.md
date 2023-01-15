Q1: Please explain what is the advantage of using SQS in this solution.

> Some advantages of using a message broker like SQS in these scenarios
>   - **Decoupling of service dependencies** reduces the scope of failure and making the 
>     architecture more resilient. The producer and consumer can afford some downtime 
>     without breaking the overall system.
>   - Allows better control over the flow of events. The queue essentially functions as a 
>     buffer and as **consumers can choose the rate of processing**, there is a lesser chance 
>     of an unexpected traffic surge overloading the system and affecting availability.
>   - **Eventual guaranteed processing** is a feature of this architecture which works well
>     for asynchronous, non-realtime applications.
>   - Since the interface for both producer and consumer is the queue there is no
>     implementation dependency or need for maintaining compatibility between the two.
>      This results in **better separation of concerns**.
>
> Advantage of SQS specifically is that it is fully managed by AWS with scale elasticity,
>  resilience and cost-effective *pay for what you use* pricing. The first class integration
> one gets with the AWS eco-system (as with any other service) makes it a very attractive
>  option if clients are already on AWS.

<br>

Q2: Compare SQS to a message broker you have used before. What are the differences?
Strong/weak points? (If you did not use such a solution, please skip this question)

> Apart from Amazon SQS, I have worked with **RabbitMQ and Apache Kafka** so far. This is 
> how SQS compares to:
>
> **RabbitMQ** <br>
> 
> RabbitMQ complies with the AMQP standard protocol and contains an component called **exchange**. The 
> producers send messages to exchanges instead of queues directly. This allows the same message 
> to be published to multiple queues and in combination with a routing key configuration acheive 
> any desired behavior. However in AWS, SNS is required to be used in combination with SQS 
> (which is a standard/common pattern) to serve such requirements. Additionally, RabbitMQ 
> creates a special exchange called the default exchange for each queue. This can be used along 
> with queue name as the routing key to make it seemingly possible to publish to queues directly. 
> This reduces it to function like SQS, without having to worry about a message exchange for 
> simpler use cases (although under the hood each message goes through an exchange). It also 
> supports multiple **standard protocols** that provides freedom to users to switch to a different
> platform with minimum effort.
>
> In RabbitMQ consumers are long running services that need to maintain an active connection with
> the broker and message delivery is the responsibility of the broker. Messages are delivered
> by a *push* mechanism which is in contrast with SQS where consumers continually need to poll for
> and *fetch/pull* messages. This is by design as the latter is likely to be wasteful in systems 
> where message publishing is sporadic and queues can stay empty for prolonged periods of time.
> 
> For management and monitoring, RabbitMQ has a very rich and featureful web admin console that
> serves for all management needs of queues, exchanges, users, access control etc. (along with 
> CLI and HTTP-API). In this regard it compares well with SQS and in my opinion better than
> Apache Kafka
> 
> **Kafka**
> 
> I haven't had the opportunity to work with or understand kafka internals in depth so I do not
> have as much insight to offer here. From whatever limited experience I have gathered, I know that it can
> function as both a queue and pub-sub and is a powerful platform that can serve many other
>  sophisticated use cases. It is designed around the more generic idea of message streaming,
>  built well for scalability and resilience. However it can be an overkill for simpler use cases
>  that do not need to worry about scale and where the cost of running, managing and operating
>  it may not be worth it.

<br>

Q3: If we run multiple instances of this tool, what prevents a message from processed twice?

> Once a message is received by a consumer, SQS changes it's **visibility** with a timeout.
> The message is no longer visible to any other consumer and this prevents the message from 
> being processed more than once. 
>
> It is the responsibility of the consumer to process and delete the message before the timeout,
>  completing the lifecycle of the message and it's processing. 
> If the message is not deleted before the timeout, it is made visible again to consumers, 
> assuming that message processing failed. Hence the timeout mechanism is necessary to re-attempt 
> message processing in scenarios where the message was received but failed to process. 
>
> Additionally, it is important to note that although standard queues ensure *at least once delivery*,
> they do not guarantee *exactly once processing*. Therefore it is advisable to build some 
> de-duplication mechanism or keep the message processing operation idempotent. This has been 
> incorporated in the implementation of the tool by using the message id (unique identifier of 
> a message) itself as the primary key and conditionally writing to the DB only if it is not 
> already present.


Q4: In very rough terms, can you suggest an alternative solution aside from using SQS from your previous experience using different technologies?

> RabbitMQ, Kafka, Azure Service Bus, Google Pub/Sub etc.
