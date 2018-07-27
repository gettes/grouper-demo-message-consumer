# grouper/demo-message-consumer

RabbitMQ config - connect to rabbitmq on port 5672 - default username/password = guest/guest

Create the following 3 queues
    Grouper or G2 or G3
On the Exchanges tab:
    Create bindings for routing based on all messages to queue or on routing_key to cause messages to be sent to queues named:
        - consumer.py will simultaneously read from the above 3 queues
        - In grouper, the Grouper queue is configured to receive every changelog entry as a message.
            See grouper configs in Grouper Demo TIER repo for grouper-loader and grouper.client configs
        - The University of Hawaii code developed by Unicon sends AMQP messages and can be configured to send to a topic which then routes messages based on routing_key so you can selectively displlay which queue gets messages.
                - Hawaii code is at https://github.com/Unicon/grouper-amqp-esb-publisher
                - The Hawaii code is the more powerful solution but, seeing everything Grouper generates is also useful.  A request was made to include the key differences in the H code and include them in Grouper.

In Admin, create an account called readerG2 with password readerG2 with no privs and allow it to read any queue on virtual host /

docker-compose build demo-message-consumer
    creates docker container with consumer.py and installs python3.7 (latest) and adds pika for AMQP handling

