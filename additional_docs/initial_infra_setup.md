# ROS 2 Learning Workspace — Environment Setup

This document records the current development setup and the steps used to recreate it on a similar machine. It distinguishes the system-wide ROS installation from the project-local Pixi environment.

## 1. Host and virtual machine

### Host

- MacBook Pro with Apple Silicon (M1 Pro)
- UTM 4.7.5

### Ubuntu VM

- Ubuntu 26.04 LTS (`resolute`)
- ARM64 / `aarch64`
- 4 CPU cores
- 4 GB RAM
- Approximately 62 GB virtual disk

The VM architecture matters: Pixi targets `linux-aarch64`, not an x86-64 Linux platform.

## 2. Two ROS 2 installations

This machine has two separate ROS 2 Lyrical installations:

| Installation | Scope | Location | How it is used |
| --- | --- | --- | --- |
| Ubuntu apt ROS | System-wide | `/opt/ros/lyrical` | Available to the operating system; source its setup file in a terminal when using this installation. |
| RoboStack ROS | Project-local | `~/ros2_ws/.pixi/envs/default` | Managed by Pixi for this repository; run commands through `pixi run` or enter the environment with Pixi. |

Both use the **Lyrical Luth** ROS distribution, but their individual package builds and versions may differ. The Pixi lockfile records the exact RoboStack package builds resolved for this project.

Keep the environments separate. In particular, do not source `/opt/ros/lyrical/setup.bash` in a shell where you intend to use the Pixi ROS environment; mixing environment paths can cause Python package and ROS library conflicts.

## 3. System-wide ROS installed with apt

The apt installation lives under `/opt/ros/lyrical`. It was verified with `ros2 doctor` and the C++ demo talker.

To use the apt installation in a terminal:

```bash
source /opt/ros/lyrical/setup.bash
```

Check whether it is active in the current terminal:

```bash
printenv ROS_DISTRO
```

Expected output when the apt setup file has been sourced:

```text
lyrical
```

The apt setup line was removed from automatic shell startup so fresh terminals do not silently activate the system ROS before choosing which environment to use. To check the current `.bashrc` setting:

```bash
grep -n 'opt/ros/lyrical/setup.bash' ~/.bashrc
```

If the line begins with `#`, it is commented out and will not source apt ROS automatically.

## 4. Pixi and RoboStack ROS for this project

Pixi is installed for the Ubuntu user at:

```text
~/.pixi/bin/pixi
```

The installer added Pixi's `bin` directory to `~/.bashrc`, so new Bash terminals can find the `pixi` command. Check it with:

```bash
pixi --version
```

The project manifest is `~/ros2_ws/pixi.toml`. Its important settings are:

```toml
[workspace]
channels = ["https://prefix.dev/robostack-lyrical"]
name = "ros2_ws"
platforms = ["linux-aarch64"]
version = "0.1.0"

[dependencies]
ros-lyrical-ros-base = ">=0.13.0,<0.14"
ros-lyrical-demo-nodes-cpp = ">=0.37.9,<0.38"
```

Pixi created `pixi.lock` when it resolved and installed the environment. Commit both `pixi.toml` and `pixi.lock`: the manifest describes the requested environment, while the lockfile records the exact resolved packages.

From the project directory, recreate or update the environment with:

```bash
cd ~/ros2_ws
pixi install
```

Run a command using the Pixi environment with:

```bash
pixi run printenv ROS_DISTRO
```

Expected output:

```text
lyrical
```

Use `pixi run <command>` for project commands so they run inside the project environment. The `.pixi/` directory contains local environment files and is ignored by Git; the lockfile and manifest are the reproducible, shareable configuration.

## 5. Git and GitHub

Git is installed with Ubuntu's package manager. Git's author identity is configured globally for the Ubuntu user:

```bash
git config --global user.name "Samridhi Parihar"
git config --global user.email "samparihargeorge@gmail.com"
```

The local Git repository is `~/ros2_ws`; its GitHub remote is named `origin` and uses SSH:

```text
git@github.com:SamridhiParihar/ros2-learning.git
```

The Ubuntu VM has its own Ed25519 SSH key pair under `~/.ssh/`:

```text
id_ed25519       private key — keep private
id_ed25519.pub   public key — added to GitHub
```

The Mac and Ubuntu VM are separate machines. Each can have its own SSH key registered with GitHub. Never share or upload the private key. A connection test is:

```bash
ssh -T git@github.com
```

## 6. Recreating this setup on another ARM64 Ubuntu VM

1. Install Git and Pixi for the Ubuntu user.
2. Install ROS 2 Lyrical system-wide with the official ROS apt instructions for the Ubuntu release and architecture. Verify the apt installation before proceeding.
3. Create the project directory and initialize Git.
4. Initialize Pixi with the RoboStack Lyrical channel and `linux-aarch64` platform.
5. Add the project's ROS packages, then run `pixi install`.
6. Copy or clone this repository and run `pixi install` to recreate the locked project environment.
7. Configure Git identity and create a separate SSH key for that machine if it needs to push to GitHub.
8. Keep apt ROS and Pixi ROS environments separate when building or running ROS programs.

For another architecture or Ubuntu release, check package availability and the platform identifier before reusing this configuration. The package versions and availability can differ.

