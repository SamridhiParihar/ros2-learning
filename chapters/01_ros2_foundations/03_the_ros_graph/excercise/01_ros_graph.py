# ============================================================
# Exercise 3 — Describe a ROS graph
#
# Goal:
# Explain what the ROS graph shows and what it does not show.
#
# Concepts:
# - Nodes and communication interfaces
# - Topics and data flow
# - Namespaces and topic names
# - Discovery and domain IDs
# - Logical graph versus physical computer layout
#
# Assignment:
# Imagine a robot that must find a red cup and move near it.
# It has a camera, perception, planner, controller, and hardware
# interface.
#
# 1. Describe or draw its ROS graph.
#
# 2. State what each node publishes or subscribes to.
#
# 3. Explain how one topic could connect one publisher to more
#    than one subscriber.
#
# 4. Explain how a namespace such as /robot1 can organize node
#    and topic names.
#
# 5. Explain how nodes discover each other in a typical
#    DDS-based ROS 2 setup.
#
# 6. Explain why seeing a publisher and subscription in the graph
#    does not prove that messages are arriving.
#
# 7. Explain why the ROS graph does not show which process,
#    computer, or network path each node uses.
#
# 8. Does ROS 2 need a central ROS master to relay every message?
#    Explain your answer.
#
# Do not write ROS code yet. Use your own words and reasoning.
# ============================================================


# ============================================================
# Exercise 3 — My answer
#
# My robot can have these nodes:
#
# Camera node
#     publishes images on /robot1/camera/image
#
# Perception node
#     subscribes to /robot1/camera/image
#     publishes cup detections on /robot1/detections
#
# Planner node
#     subscribes to /robot1/detections
#     publishes a motion plan on /robot1/motion_plan
#
# Controller node
#     subscribes to /robot1/motion_plan
#     publishes commands on /robot1/cmd_vel
#     subscribes to robot measurements on /robot1/measurements
#
# Hardware interface node
#     subscribes to /robot1/cmd_vel
#     publishes robot measurements on /robot1/measurements
#
# The flow is:
#
# Camera
#   -> /robot1/camera/image
#   -> Perception
#   -> /robot1/detections
#   -> Planner
#   -> /robot1/motion_plan
#   -> Controller
#   -> /robot1/cmd_vel
#   -> Hardware interface
#
# The hardware interface sends information to the robot and also
# sends measurements back. The controller uses those measurements
# to check how the robot actually moved.
#
# One topic can have one publisher and many subscribers. For example,
# both the perception node and an image-viewer node could subscribe
# to /robot1/camera/image.
#
# A namespace groups names. If a node is in the /robot1 namespace,
# a relative topic name like camera/image can become
# /robot1/camera/image. A namespace is a ROS name; it is not an
# IP address or a computer.
#
# In a typical DDS-based setup, middleware discovery lets ROS
# participants learn about each other's nodes and communication
# interfaces. They usually need to use the same ROS domain ID and
# have a working network configuration to discover each other.
#
# Seeing the publisher and subscription in the graph tells me that
# the endpoints were discovered. It does not prove that messages
# arrive. The topic names, message types, QoS settings, middleware,
# and network must also allow communication.
#
# The ROS graph is a logical view of nodes and their interfaces.
# It does not tell me whether two nodes are in the same process,
# on different computers, or which exact network path the data uses.
#
# ROS 2 does not need one central ROS master to relay every message.
# Discovery is distributed in common DDS-based setups, though the
# exact details depend on the middleware and its configuration.
# ============================================================