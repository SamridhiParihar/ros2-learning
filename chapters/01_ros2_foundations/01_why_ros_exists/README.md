# Chapter 1 — Why ROS Exists

## The short answer

ROS exists to help developers build a robot application from separate software components and connect those components through shared interfaces. A robot may have software for cameras, perception, localization, planning, control, and hardware. ROS provides common ways for these parts to exchange data, coordinate work, and be inspected while the robot is running.

ROS does not provide the robot's intelligence automatically. It provides a software framework and ecosystem; the application code supplies the perception algorithms, plans, policies, and control behavior.

## The integration problem in robotics

A robot is a system of interacting parts. A camera produces data, perception interprets it, a planner decides what motion is possible, and a controller turns that motion into hardware commands. These parts may use different libraries and programming languages, run at different rates, and be developed by different people.

Without shared interfaces, every component can end up with a custom connection to other components. Replacing a camera or changing the format of its output may then require changes throughout the application. Testing can also become difficult because each component depends on the details of the others.

ROS helps by providing common software concepts and conventions for organizing components and exchanging data. This reduces the amount of custom integration code teams must write and gives them tools to inspect the connections.

## A mental model for a ROS application

Think of ROS as a common communication and integration layer around robot software:

```text
Robot application components
        ↓
ROS client libraries and interfaces
        ↓
ROS middleware abstraction
        ↓
Operating system and network
```

Application components contain the robot-specific behavior. ROS client libraries expose ROS concepts to application code. In Python, the client library is `rclpy`; in C++, it is `rclcpp`. Beneath them, ROS uses a middleware interface so the application is not tied to one communication implementation. DDS is commonly used, and ROS 2 can support different middleware implementations.

The operating system still manages processes, memory, files, networking, and CPU scheduling. ROS runs on top of the operating system; ROS is not a replacement for Linux, macOS, or another operating system.

## Nodes: logical ROS participants

A **node** is a named participant in the ROS graph. It performs some part of the application and can use ROS interfaces to communicate with other nodes.

For example, a camera node may publish images, while a perception node subscribes to those images and publishes detected objects.

It is useful to keep these terms distinct:

| Term | Meaning |
| --- | --- |
| ROS node | A logical ROS participant that has a name and ROS interfaces. |
| Operating-system process | A running program managed by the operating system. |
| Thread | A path of execution inside a process. |
| ROS service | A specific request-and-response communication pattern. |

A node is not automatically a separate process, thread, or service. Nodes often run in separate processes, but ROS 2 also supports running multiple nodes within one process. A node can publish and subscribe to topics, offer or call services, use actions, and do several of these things at once.

The Java-services analogy is useful for understanding modularity, but a ROS node is not simply a Java microservice. It is a ROS participant, and ROS has a specific interface named a *service* for request-and-response interactions.

## Communication between components

ROS provides several interaction patterns. We will study them in later chapters; for now, their purpose is enough to distinguish them:

| Pattern | General use |
| --- | --- |
| Topic | A stream of data, such as camera images or robot state. Publishers send messages; subscribers receive matching messages asynchronously. |
| Service | A request followed by a response, usually for a relatively short operation. |
| Action | A longer-running task that can report progress and support cancellation. |

Each interaction has an interface. For data to be useful, components must agree on more than a programming-language type. They must agree on the meaning of the fields, units, coordinate frames, timestamps, and communication expectations. For example, a position value without an agreed coordinate frame can be syntactically valid but interpreted incorrectly.

ROS 2 uses distributed discovery rather than requiring one central broker for normal node discovery. DDS is a common middleware that supports discovery and data transport. “Peer-to-peer” is a helpful high-level description of this distributed design, but the exact path data takes depends on the selected middleware, process layout, and network configuration.

## Example: finding a red cup and moving near it

One possible design is:

```text
Camera node
    │ publishes image data
    ▼
Perception node
    │ publishes detected cup and its location
    ▼
High-level decision-maker
    │ decides the task is to approach the cup
    ▼
Motion planner
    │ computes a feasible path or trajectory
    ▼
Controller
    │ turns the trajectory into control commands
    ▼
Hardware interface
    │ sends commands to actuators and reports measurements
    ▼
Robot
```

The hardware interface and sensors also provide feedback. For example, wheel encoders or joint sensors report the robot's measured movement. The controller compares that measured state with the desired motion and adjusts its commands:

```text
Robot measurements → hardware interface → controller
         ▲                                  │
         └──────────── robot motion ◀───────┘
```

This is a **feedback loop**. The system does not merely issue a command and assume the robot followed it; it measures the result and responds to it.

The division of responsibility is important. The high-level decision-maker may decide *what task to perform*. The planner determines *how to move*. The controller handles *how to execute that motion using current feedback*. The hardware interface translates between ROS-level commands and the robot's actual devices.

## Why modularity helps

Separating responsibilities can make a robot system easier to develop and maintain:

- Different people can work on perception, planning, and hardware integration in parallel.
- A camera driver can potentially be replaced while keeping the downstream interface stable.
- Perception can be tested with recorded images before connecting a real camera.
- A component can run on another computer if the system's performance and network allow it.
- ROS tools can help inspect which nodes, topics, services, and actions exist.

Modularity does not happen automatically just because code is split into nodes. Developers still need to define clear responsibilities and stable interfaces. They must also handle failure, invalid data, and timing explicitly.

“The interfaces are the same” must mean that the components agree on data types and semantics, not merely that their code happens to compile. For robotics, units, timestamps, coordinate frames, and quality-of-service expectations can all affect whether components interpret data correctly.

## Latency, scheduling, and feedback

ROS does not promise zero latency. A message may experience delay from several sources:

- The computation performed by a component
- Waiting for a callback or executor to run
- Queued messages waiting to be processed
- Serialization, copying, and memory allocation
- Middleware and network transport
- Operating-system scheduling
- Communication with sensors and actuators

ROS communication settings, especially Quality of Service (QoS), can affect reliability, queue history, and delivery behavior. But timing is an end-to-end system property; it cannot be controlled by one setting alone. A design must consider the work done at each stage, how quickly it runs, how old data may become, and what the system should do when data arrives late or is missing.

Different components have different timing needs. A high-level decision-maker or motion planner may perform expensive work and take longer. A low-level controller often needs to run frequently and predictably so that it can respond to sensor feedback. A slow high-level decision should not prevent the controller from continuing its local feedback loop.

Perception can also be computationally expensive. The system must consider both how long perception takes and whether the resulting detection is still fresh enough for the planner to use. Timestamps and feedback help the system reason about the age and relevance of information.

ROS helps developers choose communication patterns and organize timing-sensitive work, but it does not automatically make an application real-time, safe, or correct. Those properties require deliberate system design, suitable operating-system and hardware choices, and validation.

## What ROS is—and what it is not

ROS is a robotics software framework and ecosystem. It includes client libraries, communication interfaces, middleware integration, command-line tools, build conventions, and reusable packages.

ROS has orchestration-like features. For example, launch tools can start and configure groups of nodes. But ROS alone is not a complete deployment manager that automatically schedules every component across a cluster, restarts all failures, or guarantees robot safety.

ROS also does not decide what the robot should do. That behavior comes from application code: perception algorithms, planners, controllers, learned policies, or high-level agents. ROS provides common ways for those parts to communicate and be integrated.

## Key ideas to remember

1. A robot application is made of interacting software and hardware components.
2. ROS provides common interfaces and tools for connecting robot software.
3. A node is a logical participant in the ROS graph; it is not automatically a process, thread, or ROS service.
4. Topics, services, and actions are different communication patterns for different needs.
5. Data contracts include meaning—units, frames, timestamps, and behavior—not only field types.
6. Feedback lets a robot compare desired behavior with measured results and adjust its commands.
7. Latency can come from computation, queues, middleware, the operating system, networks, and hardware.
8. ROS helps organize communication, but application behavior, safety, and timing guarantees require deliberate design.

