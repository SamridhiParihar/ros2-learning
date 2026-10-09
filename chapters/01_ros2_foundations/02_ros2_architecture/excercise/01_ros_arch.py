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


# ---- refine answers ----

# ============================================================
# Exercise 2 — Trace a ROS 2 message through the layers
#
# Concepts
#
# rclpy:
# A ROS 2 client library used by Python programs. It gives my
# Python code methods for creating nodes, publishers, subscriptions,
# timers, and other ROS features. It does not convert my whole
# Python program into C.
#
# rclcpp:
# A ROS 2 client library used by C++ programs. It provides similar
# ROS features through a C++ API. C++ programs are compiled into
# native machine instructions; rclcpp does not translate them into C.
#
# rcl:
# A common ROS client library written in C. rclpy and rclcpp use
# the lower ROS layers through it. It provides common ROS client
# functionality, but it does not create a dedicated background
# thread for every node.
#
# RMW interface:
# The middleware-neutral boundary between the ROS client layers
# and a middleware implementation. Using this boundary helps keep
# application code from depending directly on one middleware
# vendor's API.
#
# RMW implementation:
# A particular implementation of the RMW interface. It connects
# ROS communication operations to the chosen middleware. The
# middleware can handle discovery and data distribution, and may
# use OS networking when communication crosses processes or
# machines.
#
# Node:
# A logical participant in the ROS graph. A node performs one or
# more parts of a robot application and can contain publishers,
# subscriptions, and other ROS interfaces.
#
# Publisher:
# An object inside a node that publishes messages of a particular
# type on a topic. A node can contain multiple publishers.
#
# Subscription:
# An object inside a node that receives messages of a particular
# type from a topic. A node can contain multiple subscriptions.
#
# Topic:
# A named communication channel in the ROS graph. Publishers and
# subscriptions use the same topic name and compatible message
# types to communicate. A topic is not a central storage server.
#
# Process:
# A running program managed by the operating system.
#
# Thread:
# A path of execution inside a process. Threads in one process
# share many process resources, such as memory, but each thread
# has its own execution state and stack.
#
# Executor:
# ROS machinery that waits for callbacks to become ready and runs
# them using the executor's available thread or threads. A node
# does not automatically receive its own thread.
#
# Socket:
# An operating-system communication endpoint. The OS manages its
# state and send/receive buffers. The bucket analogy helps me
# picture data waiting to be sent or received, but a socket is not
# literally two memory buckets.
#
# Protocol:
# A set of rules for communication. TCP and UDP are examples of
# transport protocols with different behavior and guarantees.
#
# Operating system:
# Software that manages computer resources such as processes,
# threads, memory, CPU scheduling, and networking.
#
# Device driver:
# Software that lets the operating system work with a particular
# hardware device while hiding many hardware-specific details.
#
#
# 1. Python and C++ in the ROS stack
#
# rclpy provides Python methods that connect Python application
# code to the lower ROS layers. rclcpp provides a C++ API for
# C++ programs. Neither library translates the whole application
# into C.
#
#
# 2. Trace one image message
#
# Camera application code creates an Image message and calls
# publish().
#
# The call goes through rclpy (or rclcpp for a C++ node), then
# through rcl and the RMW interface to the selected middleware
# implementation. The middleware handles communication with
# matching subscriptions.
#
# If the camera and perception nodes are on separate computers,
# the middleware uses the operating systems' networking facilities.
# The sender's OS network stack and network hardware carry the
# packets. On the receiving computer, its OS network stack passes
# received data to the middleware.
#
# The receiving ROS client stack makes the sample available to
# the perception node's subscription. The executor notices that
# the subscription callback is ready and runs it.
#
# The full path is approximately:
#
# Camera code
#     -> rclpy / rclcpp
#     -> rcl
#     -> RMW interface
#     -> middleware implementation
#     -> sender OS and network, if needed
#     -> receiver OS and middleware, if needed
#     -> receiving RMW and client library
#     -> executor
#     -> perception callback
#
# The exact path depends on the middleware and whether communication
# is inside one process, between processes, or between computers.
#
#
# 3. Raspberry Pi and laptop
#
# If the camera node runs on a Raspberry Pi and the perception node
# runs on a laptop, ROS middleware discovers compatible endpoints
# and distributes the image sample. The operating systems'
# networking stacks, network interface drivers, and Wi-Fi or
# Ethernet hardware carry the data between computers.
#
# The middleware and operating system cooperate. It is not safe
# to assume that each ROS node has its own socket or that the RMW
# layer directly controls the network hardware.
#
#
# 4. Corrections to the statements
#
# "ROS creates one socket for every node."
# This is not guaranteed. A node is a logical ROS participant,
# not a socket. Middleware may share networking resources, and
# communication inside one process may use memory without a
# network socket.
#
# "A socket is just a pair of memory buckets."
# The buckets are an analogy for send and receive buffers. A socket
# is an OS communication endpoint with state and an API. On Linux,
# bind() associates a local address with the socket; it does not
# physically attach memory to a network card.
#
# "The ROS clock synchronizes every computer."
# ROS provides clock and time abstractions, including ROS time for
# simulation and playback. It does not automatically synchronize
# physical clocks on different computers. That requires a separate
# clock synchronization setup when the system needs it.
#
# "Every message stays on the topic until a subscriber receives it."
# A topic is not a persistent message store. Delivery and history
# depend on QoS. With volatile durability, a late-joining
# subscriber does not receive old samples. Transient-local
# durability can retain a configured history for late joiners.
#
# "Creating a node automatically creates a new thread."
# Creating a node does not automatically create a dedicated thread.
# An executor runs callbacks using its available thread or threads.
#
#
# 5. Socket bucket analogy
#
# The bucket part helps me picture data waiting in send and receive
# buffers. The valve part helps me picture software controlling
# when it reads, writes, or closes a socket.
#
# The analogy can mislead me into thinking a socket is literally
# a private pipe with exactly two buckets, or that every ROS node
# gets its own socket. The real socket is managed by the operating
# system, and middleware may use shared resources or a memory-based
# path.
#
# ============================================================