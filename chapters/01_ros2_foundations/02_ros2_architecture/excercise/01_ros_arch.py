# ============================================================
# Exercise 2 — Trace a ROS 2 message through the layers
#
# Goal:
# Explain what happens when a camera node publishes an image
# and a perception node receives it. Describe the responsibilities
# of the ROS layers and the operating system.
#
# Concepts:
# - rclpy, rclcpp, and rcl
# - RMW interface and middleware implementation
# - Nodes, publishers, subscriptions, and topics
# - Processes, threads, and executors
# - Sockets, protocols, operating systems, and device drivers
# - What ROS 2 does and does not guarantee
#
# Assignment:
# Imagine a camera node publishes an image and a perception node
# receives and processes it.
#
# 1. Trace the message from the camera's publish() call until the
#    perception callback runs. Name each relevant layer in order
#    and describe its job.
#
# 2. Explain how rclpy relates to rcl, and how this differs from
#    rclcpp. Does either library translate your whole program into C?
#
# 3. Explain the difference between the RMW interface and an RMW
#    implementation.
#
# 4. Distinguish these concepts:
#    node, publisher, topic, subscription, process, thread, executor.
#
# 5. Suppose the camera node runs on a Raspberry Pi and the
#    perception node runs on a laptop. Explain how the middleware,
#    operating systems, network hardware, and device drivers take
#    part in communication.
#
# 6. Correct each statement and explain what is wrong with it:
#    - "ROS creates one socket for every node."
#    - "A socket is just a pair of memory buckets."
#    - "The ROS clock synchronizes every computer."
#    - "Every message stays on the topic until a subscriber receives it."
#    - "Creating a node automatically creates a new thread."
#
# 7. Explain one way the bucket or valve analogy helps describe
#    sockets, and one way it can give the wrong impression.
#
# Do not write ROS code yet. Use your own words and reasoning.
# ============================================================

# intial my version of answer : 

# concepts : 
# rclpy : a ros client interface that helps us to convert our application code in such a way that it invokes the rcl core client
#         functions . It for codes written in python 

# rclpp : this does the same thing but for c++ codes and also underneath the mechanism how it does changes 

# rcl : ros core client C library it handles all the non communication related responsibilites for us , like clock management , name 
#       management , allocation of the memory , background thread management ...etc etc  

# rmw interface : this is the layer after rcl , whenenver rcl needs to communicate the info , it uses this interface . instead
#                 of using direct impl it uses interface so that we aren't coupled with the vendor implementation and can switch
#                 later whenever we require to switch rwm implmentation .

# rwm implementation : this is concrete implementation of the rwm interface whose responsibility is to handle the communication of data
#                      between the nodes . I handles discovery of nodes , bindidng the socket and actual data transmission . It handles 
#                      all the calls required for communcation of data , with os

# Node : A logical participant in ROS which performs a or some unit of work in robotic system . It can communicate with other node
#        inorder to exchange data . 

# Publishers : It is an object inside a node that sends message of a particular type on a topic . There could be many publishers on 
#              a node 

# Subscribers : It is an object inside a node that recieve message of a particular type of a topic . There could be many subscriber on 
#              a node

# Topic : A logical named communication channel in ROS graph inorder to publish or subscribe . It is not a persistent central storage
#         like Kafka topic .


# process : these are running programs in the OS 

# threads : these are smallest unit of execution of a task in os . A program could have multiple threads or single thread and all the
#           the thread share program resource and memory but has its own stack space 

# executors : in ROS there are callbacks waiting in nodes to be executed and it is being managened via executor , like which will run when 
#             and it can be singlethreaded or multithreaded 

# Sockets : Socket can be imagined as combination of two things : (i) two memory buckets/buffers (outbound and inbound) for dumping outgoing data
#           and for recieving the data respectively . (ii) the addressing : ip address + port address + protocl ; for any communicaiton
#           to happen . actully tuple address ( source + dest : ip and port)

# Protocols : A set of rules for communication to happen in networking specifically we come accross mostly TCP and UDP.

# OS : the software program which manages and coordinate all the actions of cpu and hardware resources by sitting as an interface between user and hardware 
#      resource 

# Device Drivers : These are the actual programs that operates/instruct the hardware to perform action and it act as interface between
#                  os instructions for hardware and hardware 

# What ROS2 does and what it doesn't guarantee : ROS2 does provide us all the libraries and tools to manage our application and our
#                                                application logic like separation of concerns of business logic and communication and resource
#                                                allocation . It doesn't guarantee zero-copy delivery , one socket per node, one thread per node
#                                                zero latency behavior (that can depend upon how os scheduled jobs)


# Describing a system (Camera Node publishes an image ----> Perception Node recieves the image and processes it)

# 1. rclpy provides python methods that conncet to that native ROS impl and c++ program is compiled into native machine instructions
# and uses the ROS c++ client library 

# 2. Trace the message from the camera's publish() call until the
#    perception callback runs. Name each relevant layer in order
#    and describe its job. :   
#    camera node publishes --> rclpy/rclpp publish operation ---> rcl does middleware publish request ---> rwm interface send typed(contract) sample
#    ---> rwm impl use os networking  ---> OS(sender) transmit packet ---> packet arrives --> OS(reciever) packets arrives --> pass recieved data to 
#    to middleware ---> middlware impl deliver sample to matching subscripiton ---> rwm interface makes subscription data available --> rcl subcription 
#    is ready --> executor execute the callback 

# 3. for raspberry example : mostly same as above 

# 4. Correct each statement and explain what is wrong with it:
#    - "ROS creates one socket for every node." : ROS doesn't guarantee that instead A ROS node can create multiple sockets, or share existing sockets, depending on its active topics, services, and the underlying communication middleware (like DDS)
#    - "A socket is just a pair of memory buckets." No apart from memory buffers it requires address binding 
#    - "The ROS clock synchronizes every computer." : The ROS clock manages time within the robotics framework , but it relies on external operating system protocols like NTP or Chrony to actually synchronize the physical clocks of multiple computers
#    - "Every message stays on the topic until a subscriber receives it." : ROS messages are transient; by default, a message is published instantly to any currently active subscribers, and if no one is listening at that exact millisecond, the message is permanently dropped and lost. However we can use QOS for last message to persist on publisher
#    - "Creating a node automatically creates a new thread.": Creating a node simply instantiates a logical data structure; it relies on an external entity called an Executor to assign threads and process its execution callbacks