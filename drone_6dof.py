"""6DOF Drone Controller
=======================

This script merges features from two prior implementations to provide a
minimal working 6DOF drone controller.  It uses PyGame for input and
PyMAVLink for communication with a Pixhawk running the provided 16-motor
configuration.  The controller translates keyboard commands relative to a
free camera orientation and solves the required motor PWM values.

Usage
-----
Run the script on a system with PyGame and PyMAVLink installed.  The Pixhawk
should be connected via serial (default `/dev/ttyUSB0` 115200 baud).  The
``pixhawk_6dof.params`` file included in this repository contains a set of
parameters for the 16‑motor setup.
"""

import math
import time
from dataclasses import dataclass, field
from typing import List

import numpy as np
from scipy.optimize import lsq_linear
from pymavlink import mavutil
import pygame
from pygame.locals import *


# ---------------------------------------------------------------------------
# Vector and orientation helpers
# ---------------------------------------------------------------------------

@dataclass
class Vector3D:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def normalize(self) -> "Vector3D":
        n = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        if n > 0:
            self.x /= n
            self.y /= n
            self.z /= n
        return self


@dataclass
class FreeCamState:
    """Stores camera orientation and derives look/right/up vectors."""

    yaw: float = 0.0   # radians
    pitch: float = 0.0  # radians

    look: Vector3D = field(default_factory=lambda: Vector3D(1, 0, 0))
    right: Vector3D = field(default_factory=lambda: Vector3D(0, 1, 0))
    up: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 1))

    def update_from_mouse(self, dx: float, dy: float, sensitivity: float = 0.003) -> None:
        self.yaw += dx * sensitivity
        self.pitch -= dy * sensitivity
        self.pitch = max(-math.pi / 2, min(math.pi / 2, self.pitch))

        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        self.look = Vector3D(cy * cp, sy * cp, sp)

        right = np.cross(self.look.as_array(), np.array([0, 0, 1]))
        if np.linalg.norm(right) == 0:
            right = np.array([1, 0, 0])
        self.right = Vector3D(*right).normalize()
        up = np.cross(self.right.as_array(), self.look.as_array())
        self.up = Vector3D(*up).normalize()


# ---------------------------------------------------------------------------
# Motor definition and PID controller
# ---------------------------------------------------------------------------

@dataclass
class Motor:
    pos: Vector3D
    thrust_dir: Vector3D


class PID:
    def __init__(self, kp: float, ki: float, kd: float) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = np.zeros(3)
        self.integral = np.zeros(3)

    def compute(self, error: np.ndarray, dt: float) -> np.ndarray:
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


# ---------------------------------------------------------------------------
# Drone controller
# ---------------------------------------------------------------------------

class Drone6DOFController:
    def __init__(self, motors: List[Motor], device: str = "/dev/ttyUSB0", baud: int = 115200) -> None:
        self.motors = motors
        self.pid_force = PID(1.0, 0.0, 0.3)
        self.pid_torque = PID(1.0, 0.0, 0.3)
        self.mav = mavutil.mavlink_connection(device, baud=baud)
        self.mav.wait_heartbeat()
        self.arm()
        self.last_time = time.time()

    def arm(self) -> None:
        self.mav.mav.command_long_send(
            self.mav.target_system,
            self.mav.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
        )

    def disarm(self) -> None:
        self.mav.mav.command_long_send(
            self.mav.target_system,
            self.mav.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )

    def send_pwm(self, pwm_values: List[float]) -> None:
        pwm_scaled = [int(1000 + pwm * 1000) for pwm in pwm_values]
        pwm_full = pwm_scaled + [1000] * (16 - len(pwm_scaled))
        self.mav.mav.rc_channels_override_send(
            self.mav.target_system, self.mav.target_component, *pwm_full
        )

    def solve_pwm(self, desired_force: np.ndarray, desired_torque: np.ndarray) -> np.ndarray:
        A = np.zeros((6, len(self.motors)))
        for i, m in enumerate(self.motors):
            A[0:3, i] = m.thrust_dir.as_array()
            A[3:6, i] = np.cross(m.pos.as_array(), m.thrust_dir.as_array())
        b = np.concatenate((desired_force, desired_torque))
        res = lsq_linear(A, b, bounds=(0, 1))
        return np.clip(res.x, 0, 1)

    def update(self, force_error: np.ndarray, torque_error: np.ndarray) -> None:
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        corrected_force = self.pid_force.compute(force_error, dt)
        corrected_torque = self.pid_torque.compute(torque_error, dt)
        pwm = self.solve_pwm(corrected_force, corrected_torque)
        self.send_pwm(pwm)


# ---------------------------------------------------------------------------
# Motor layout
# ---------------------------------------------------------------------------

MOTORS = [
    Motor(Vector3D(15.9, 15.9, 4.5), Vector3D(0, 0, 1)),
    Motor(Vector3D(-15.9, 15.9, 4.5), Vector3D(0, 0, 1)),
    Motor(Vector3D(-15.9, -15.9, 4.5), Vector3D(0, 0, 1)),
    Motor(Vector3D(15.9, -15.9, 4.5), Vector3D(0, 0, 1)),
    Motor(Vector3D(15.9, 15.9, -4.5), Vector3D(0, 0, -1)),
    Motor(Vector3D(-15.9, 15.9, -4.5), Vector3D(0, 0, -1)),
    Motor(Vector3D(-15.9, -15.9, -4.5), Vector3D(0, 0, -1)),
    Motor(Vector3D(15.9, -15.9, -4.5), Vector3D(0, 0, -1)),
    Motor(Vector3D(15.9, 4.5, 15.9), Vector3D(0, 1, 0)),
    Motor(Vector3D(-15.9, 4.5, 15.9), Vector3D(0, 1, 0)),
    Motor(Vector3D(-15.9, 4.5, -15.9), Vector3D(0, 1, 0)),
    Motor(Vector3D(15.9, 4.5, -15.9), Vector3D(0, 1, 0)),
    Motor(Vector3D(15.9, -4.5, 15.9), Vector3D(0, -1, 0)),
    Motor(Vector3D(-15.9, -4.5, 15.9), Vector3D(0, -1, 0)),
    Motor(Vector3D(-15.9, -4.5, -15.9), Vector3D(0, -1, 0)),
    Motor(Vector3D(15.9, -4.5, -15.9), Vector3D(0, -1, 0)),
]


# ---------------------------------------------------------------------------
# Main control loop using PyGame
# ---------------------------------------------------------------------------


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    controller = Drone6DOFController(MOTORS)
    cam = FreeCamState()

    try:
        while True:
            keys = pygame.key.get_pressed()
            movement = np.zeros(3)
            torque = np.zeros(3)

            for event in pygame.event.get():
                if event.type == QUIT:
                    raise KeyboardInterrupt

            dx, dy = pygame.mouse.get_rel()
            cam.update_from_mouse(dx, dy)

            # Movement relative to camera orientation
            if keys[K_w]:
                movement += cam.look.as_array()
            if keys[K_s]:
                movement -= cam.look.as_array()
            if keys[K_d]:
                movement += cam.right.as_array()
            if keys[K_a]:
                movement -= cam.right.as_array()
            if keys[K_SPACE]:
                movement += cam.up.as_array()
            if keys[K_LCTRL]:
                movement -= cam.up.as_array()
            if keys[K_q]:
                torque[2] += 0.2
            if keys[K_e]:
                torque[2] -= 0.2

            controller.update(movement, torque)
            clock.tick(30)

    except KeyboardInterrupt:
        controller.disarm()
        pygame.quit()
        print("Motors disabled. Program terminated.")


if __name__ == "__main__":
    main()
