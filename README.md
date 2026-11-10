# ROS 2 Learning Roadmap

We’ll follow the dependencies between ideas: first learn how ROS organizes and connects programs, then build and inspect a small system, then add the robotics concepts needed to work with real robots.

## Chapter READMEs

| Section | Chapter | README |
|---|---|---|
| Part I — ROS 2 Foundations | Chapter 1 — Why ROS Exists | [Open README](chapters/01_ros2_foundations/01_why_ros_exists/README.md) |
| Part I — ROS 2 Foundations | Chapter 2 — ROS 2 Architecture | [Open README](chapters/01_ros2_foundations/02_ros2_architecture/README.md) |
| Part I — ROS 2 Foundations | Chapter 3 — The ROS Graph | [Open README](chapters/01_ros2_foundations/03_the_ros_graph/README.md) |
| Part I — ROS 2 Foundations | Chapter 4 — Nodes And Execution | [Open README](chapters/01_ros2_foundations/04_nodes_and_execution/README.md) |
| Part I — ROS 2 Foundations | Chapter 5 — Topics And Messages | [Open README](chapters/01_ros2_foundations/05_topics_and_messages/README.md) |

## Part I — ROS 2 Foundations

1. **Why ROS Exists** — the integration problems ROS solves and the role it plays in a robot system
2. **ROS 2 Architecture** — nodes, client libraries, middleware, DDS, and the operating system
3. **The ROS Graph** — how ROS nodes discover and connect to one another
4. **Nodes and Execution** — node lifecycle, callbacks, executors, processes, and threads
5. **Topics and Messages** — publishers, subscribers, message types, queues, and quality of service
6. **Services** — request-and-response communication
7. **Actions** — long-running tasks, feedback, cancellation, and results
8. **Parameters** — configuring node behavior at runtime
9. **ROS Command-Line Tools** — inspecting nodes, topics, services, actions, and parameters

## Part II — Building ROS 2 Programs

10. **ROS 2 Packages and Workspaces** — package structure, `package.xml`, Python modules, and `colcon`
11. **Your First `rclpy` Node** — connecting Python classes and ROS nodes
12. **Building a Publisher and Subscriber** — creating and connecting a small ROS application
13. **Building Services and Actions** — implementing request-response and long-running interactions
14. **Launch Files** — starting and configuring a group of nodes
15. **Debugging ROS 2 Systems** — tracing failures across nodes, interfaces, and communication

## Part III — From ROS Programs to Robot Systems

16. **ROS Interfaces and Custom Messages** — designing the data contracts between components
17. **Timing, Latency, and Quality of Service** — rates, queues, stale data, reliability, and deadlines
18. **TF2 and Coordinate Frames** — representing and transforming positions and orientations
19. **URDF and Robot Description** — describing a robot’s links, joints, and sensors
20. **Simulation** — connecting ROS 2 to a simulated robot and environment
21. **Controllers and Hardware Interfaces** — sending commands to robot hardware safely and predictably
22. **Sensors and Perception Pipelines** — connecting camera and sensor data to perception software

## Part IV — Robotics Capabilities

23. **Robot Geometry and Kinematics** — configurations, forward kinematics, and inverse kinematics
24. **Motion Planning** — planning paths and motions around constraints and obstacles
25. **Feedback and PID Control** — using sensor feedback to adjust robot behavior
26. **Localization and Mapping** — estimating where the robot is and building maps
27. **Navigation and Manipulation** — combining perception, planning, and control for robot tasks

## Part V — Toward Agentic Robot Learning

28. **Python, NumPy, and PyTorch in ROS Systems** — connecting robotics software with machine-learning tools
29. **Reinforcement Learning and Robot Learning** — policies, training environments, and deployment considerations
30. **VLM and LLM Agent Integration** — connecting high-level reasoning to robot actions
31. **System Design for Agentic Robots** — deciding where planning, policy, and control belong
32. **Reading and Contributing to Robotics Codebases** — tracing data flow, reviewing designs, and making changes

We’ll begin with **Chapter 1, “Why ROS Exists,”** which we’ve already started. We can adjust the order as your understanding develops—for example, bringing simulation or a small Python node earlier if that helps make the concepts concrete.

