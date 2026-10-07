# ============================================================
# Exercise 1 — Why ROS, and how would you divide the robot software?
#
# Goal:
# Show that you understand why ROS is useful for connecting robot
# components, and distinguish ROS nodes from processes, threads,
# and ROS services.
#
# Concepts:
# - Modular robot software
# - Nodes and their responsibilities
# - Communication between components
# - Latency and feedback
# - What ROS provides—and what it does not guarantee
#
# Requirements:
# Imagine a robot that must find a red cup and move near it.
# Draw or describe a system containing a camera, perception, a
# high-level decision-maker, a motion planner, a controller, and
# a hardware interface.
#
# For each component, state:
# 1. What job it performs.
# 2. What information it receives and sends.
# 3. Why it makes sense to keep it as a separate software component.
# 4. Which work needs to happen quickly and predictably, and which
#    work can take longer.
#
# Also explain:
# - What ROS contributes to this system.
# - Why a ROS node is not automatically a Java service, an
#   operating-system process, or a thread.
# - Why ROS can help with latency management but does not promise
#   zero latency.
#
# Your answer:
#
# ============================================================


# my version initially : 
# concepts : 
# 1. Modular Robot Software  : ROS basically helps us in building modular nodes in a way that we can actually 
# build different nodes simultaneously for different actions and also can replace one node with another as long
# as contracts are same with the interface depending upon the requirements , so basically it's all about isloating
# the bigger problem into different chunks and parallely working on that and updating as per env and requirement

# 2.Nodes And their responsibilites : On a high level what I understood is nodes are like standalone program which
# can communicate with other nodes and it probably solves one unit of task and also it kind of follows contract as 
# per interface .

# 3.Communication between components : communication between component helps via dds layer , it can use topics
# and messages , services and actions for communication , here the communication is mostly done peer to peer 

# 4. Latency and feedback : as each component sort of broadcast and peer to peer communication happens between 
# the nodes/components the latency dependeds upon how we configure things via parameters and it's not like a 
# central broker where publisher pushes and consumer polls 

# 5. What Ros provides and what it does not gurantee :first thing ROS is not some OS , it actually runs on top
# of an OS and it uses OS memory , process , networking ...etc . It is sort of an eco system of robotics related
# libraries , tools and other capabilites . It also posesses some orchestration like feature . And most 
# importantly it doesn't provide the business logic and with business logic I mean the robot's intelligence and
# that's on us to decide whether it's algorithm , policies , etc ....



# Robot for finding red cup and moving near it : 

# Camera node ( it will publish image data ) --> Perception Node (it will process the raw data and with logic 
# it had to publish the detected cup) --> Planner Node (based on detected cup info it need to plan action for motion)
# ---> Controller (based on plan action it will need to produce control outputs) --> Hardware node (communicate with 
# actual robot hardware)

# based on my intuiton , planner and perception node should take more time as compared to others 



# refined version :

# Concepts:
#
# 1. Modular robot software:
# ROS helps us divide a bigger robot application into smaller components.
# These components can be developed by different people at the same time,
# and one component can sometimes be replaced by another if their interfaces
# are compatible. This makes the system easier to change as the robot or
# its requirements change.
#
# An interface is more than just having the same message type. The components
# also need to agree on what the data means, such as its units, coordinate
# frame, and timestamp.
#
# 2. Nodes and their responsibilities:
# A node is a logical ROS participant that performs some part of the robot's
# work and communicates with other nodes through ROS interfaces.
#
# A node is not necessarily a standalone program or operating-system process.
# Multiple nodes can run inside one process. A process is managed by the
# operating system, while a node is a concept in ROS.
#
# 3. Communication between components:
# ROS components can communicate using topics and messages, services, and
# actions. Topics are useful for streams of data, while services and actions
# support other kinds of interaction.
#
# ROS 2 uses a client library and a middleware layer for communication. DDS
# is a common middleware used by ROS 2. Nodes can discover compatible
# publishers and subscribers without relying on one central message broker,
# though the exact data path depends on the middleware and system setup.
#
# 4. Latency and feedback:
# Latency can come from the work a component performs, waiting for callbacks,
# message queues, copying or serializing data, middleware, networking, and
# communication with hardware.
#
# ROS communication settings such as QoS can affect how data is delivered
# and queued, but ROS does not promise zero latency. General node parameters
# are not the only way to control timing.
#
# Feedback is also important. After the controller sends commands through
# the hardware interface, sensors and hardware should report the robot's
# measured state. The controller can use that feedback to adjust later
# commands.
#
# 5. What ROS provides and does not guarantee:
# ROS is not an operating system. It runs on top of an operating system and
# uses the operating system's processes, memory, networking, and scheduling.
#
# ROS is a robotics software ecosystem of libraries, communication tools,
# conventions, and packages. It has tools for starting groups of nodes, but
# it does not provide the robot's task logic or intelligence automatically.
# We have to implement that using algorithms, policies, planners, and
# controllers.
#
# ROS helps us build and connect the components, but it does not guarantee
# that they will always be fast, safe, or correct.
#
# Robot system:
#
# Camera node
#     publishes images
#         ↓
# Perception node
#     detects the red cup and publishes detection information
#         ↓
# High-level decision-maker
#     decides that the robot should approach the cup
#         ↓
# Planner node
#     plans a path or motion toward the cup
#         ↓
# Controller node
#     turns the planned motion into control commands
#         ↓
# Hardware interface
#     sends commands to the robot and reports measured state
#         ↓
# Robot
#
# The robot's measured state is fed back to the controller so it can adjust
# its commands. The planner and high-level decision-maker can also use
# updated information about the robot and its surroundings.
#
# Timing:
# Perception and planning may need substantial computation. The high-level
# decision-maker may take even longer. The controller and hardware interface
# usually need to respond more frequently and predictably, so a slow
# high-level decision should not stop the controller from using feedback
# and continuing to control the robot.

