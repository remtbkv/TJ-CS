import random, time, os
from datetime import datetime
from math import sin, cos
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle
from matplotlib.widgets import Button
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

class BallBeam():
    """
    Simple ball and beam simulation built to interface easily with OpenAI's
    gym environments.

    System dynamics
    ---------------
    dx/dt = v(t)
    dv/dt = -m*g*sin(theta(t))/((I + 1)*m)
    """

    def __init__(self, timestep=None, unit_conversion=None, beam_length=None, ball_radius=None, max_angle=None, setpoint=None, init_velocity=None, random_init_vel=None, random_set=None, sleep=None):
        self.g = 9.8
        self.dt = timestep 
        self.ball_radius = ball_radius*unit_conversion  # cm
        self.L = beam_length*unit_conversion            # m
        self.beam_radius = self.L/2         
        self.setpoint = setpoint
        self.max_random_set = 0.3                       # fraction for farthest point at which to balance ball. remember 0.5 is the end of the beam on positive side (right)
        self.max_random_vel = 0.3                       # fraction of max velocity for which to randomly set velocity
        self.point = self.setpoint*self.L               # actual balance point on beam (meters), for rendering purposes
        self.goal = self.point                       
        self.random_set = random_set
        self.I = 2/5*self.ball_radius**2                # solid ball inertia (omits mass)
        self.random_init_vel = random_init_vel
        self.init_velocity = init_velocity*unit_conversion
        self.max_angle = max_angle
        self.max_a = self.g*sin(max_angle)
        self.max_v = (self.init_velocity**2 + 10/7*self.g*self.L*sin(max_angle))**0.5
        self.reset()
        self.sleep = sleep
        self.human_rendered = self.machine_rendered = False
        self.ep = self.frame = 0

    def get_state(self):
        """
        Return current simulation state.

        Returns
        -------
        state : [x, v, theta], list of floats
        """
        return np.array([self.x, self.v, self.theta])

    def get_max_state(self):
        return np.array([self.L/2, self.max_v, self.max_angle])

    def get_goal(self):
        return self.goal

    def reset(self):
        """
        Reset simulation to initial (mostly random) state. Returns state.
        """
        if self.random_set:
            self.setpoint = np.random.uniform(-self.max_random_set, self.max_random_set)
            self.point = self.setpoint*self.L
            self.goal = self.point
        self.x = random.uniform(-self.max_random_set,self.max_random_set)*self.L
        self.y = self.ball_radius# + 40 # ball is not actually rendered on top of the beam? (small radius ball is barely visible, as it's inside of the beam)
        self.v = np.random.uniform(-self.max_v*self.max_random_vel, self.max_v*self.max_random_vel) if self.random_init_vel else self.init_velocity
        self.a = 0
        self.theta = 0
        self.ang_v = 0
        self.ang_a = 0
        self.lim_x = [-self.beam_radius, self.beam_radius]
        self.lim_y = [0,0]
        self.t = 0
        return self.get_state()

    def update(self, action):
        """ 
        Update simulation with one time step. Returns state.

        Parameters
        ----------
        action : angle to which beam should be set, float (rad)
        """
        if isinstance(action, np.ndarray):
            action = action.item()

        theta = max(-self.max_angle, min(self.max_angle, action)) 
        
        v_final = (theta - self.theta)/self.dt
        self.ang_a = (v_final - self.ang_v)/self.dt
        self.theta = theta
        self.ang_v = v_final

        x = self.x
        v = self.v

        self.v += -self.g/(1 + 2/5)*sin(self.theta)*self.dt
        self.x += self.v*self.dt
        self.y = self.ball_radius/cos(self.theta) + self.x*sin(self.theta)
        
        self.v = (self.x - x)/self.dt
        self.a = (self.v - v)/self.dt
        
        self.lim_x = [-cos(self.theta)*self.beam_radius, cos(self.theta)*self.beam_radius]
        self.lim_y = [-sin(self.theta)*self.beam_radius, sin(self.theta)*self.beam_radius]
        
        self.t += self.dt
        return self.get_state()

    def pause(self, event): 
        if self.sleep is not None:
            time.sleep(self.sleep)

    def screenshot(self, event):
        ss_dir = 'screenshots'
        if not os.path.exists(ss_dir):
            os.makedirs(ss_dir)
        fn = "ep={}_frame={}_tstep={}_time={}".format(self.ep, self.frame, round(self.t, 2), datetime.now().strftime("%H;%M;%S;%f")[:-3])
        self.fig.savefig(f"{ss_dir}/{fn}.png", dpi=self.fig.dpi, bbox_inches='tight')

    def _init_render(self, mode):
        """ Initialize rendering """
        if mode == 'human':
            self.human_rendered = True
            plt.ion()
            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            fig.canvas.manager.set_window_title('Ball & Beam')
            ax.set(xlim = (-2*self.beam_radius, 2*self.beam_radius), ylim = (-self.L/2, self.L/2))
            ax.set_axis_off() # removes everything for blank background
            
            # draw ball
            self.ball_plot = Circle((self.x, self.y), self.ball_radius)
            ax.add_patch(self.ball_plot)
            ax.patches[0].set_color('red')
            
            # draw beam
            ax.plot([-cos(self.theta)*self.beam_radius, cos(self.theta)*self.beam_radius],
                    [-sin(self.theta)*self.beam_radius, sin(self.theta)*self.beam_radius], lw=4, color='black')
            
            # draw pivot
            ax.plot(0.0, 0.0, '.', ms=15)

            # draw setpoint
            ax.add_patch(Polygon([
                [self.point*cos(self.theta), -0.01*self.L + self.point*sin(self.theta)],
                [self.point*cos(self.theta) - 0.015*self.L, -0.03*self.L + self.point*sin(self.theta)],
                [self.point*cos(self.theta) + 0.015*self.L, -0.03*self.L + self.point*sin(self.theta)]]))
            ax.patches[1].set_color('green')

            # draw screenshot button
            ss_ax = plt.axes([0, 0, 1, 1])
            ss_ax.set_axes_locator(InsetPosition(ax, [0.8, 0.8, 0.16, 0.1]))
            self.btn_ss = Button(ss_ax, "Screenshot")
            self.btn_ss.on_clicked(self.screenshot)

            # draw button
            if self.sleep:
                pause_ax = plt.axes([0, 0, 1, 1])
                pause_ax.set_axes_locator(InsetPosition(ax, [0.8, 0.68, 0.16, 0.1]))
                self.btn_pause = Button(pause_ax, "Pause")
                self.btn_pause.on_clicked(self.pause)

            self.fig = fig
            self.ax = ax
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        else:
            self.machine_rendered = True
            fig, ax = plt.subplots(1, 1, figsize=(8, 4))

            # avoid drawing plot but still initialize
            _ = fig.canvas.manager.set_window_title('Ball & Beam')
            _ = ax.set(xlim = (-2*self.beam_radius, 2*self.beam_radius), ylim = (-self.L/2, self.L/2))
            
            # draw ball
            self.ball_plot = Circle((self.x, self.y), self.ball_radius)
            _ = ax.add_patch(self.ball_plot)
            _ = ax.patches[0].set_color('red')
            # draw beam
            _ = ax.plot([-cos(self.theta)*self.beam_radius, cos(self.theta)*self.beam_radius],
                        [-sin(self.theta)*self.beam_radius, sin(self.theta)*self.beam_radius], lw=4, color='black')
            _ = ax.plot(0.0, 0.0, '.', ms=20)
            _ = ax.add_patch(Polygon(
                [[self.point*cos(self.theta), -0.01*self.L + self.point*sin(self.theta)],
                 [self.point*cos(self.theta) - 0.015*self.L, - 0.03*self.L + self.point*sin(self.theta)],
                 [self.point*cos(self.theta) + 0.015*self.L, -0.03*self.L + self.point*sin(self.theta)]]))
            _ = ax.patches[1].set_color('green')

            self.machine_fig = fig
            self.machine_ax = ax

    def render(self, button_info=None, mode='human'):
        """ 
        Render simulation at its current state

        Parameters
        ----------
        mode : rendering mode, str [human, machine]
        """
        if button_info is not None:
            self.ep, self.frame = button_info
        if (not self.human_rendered and mode == 'human') or (not self.machine_rendered and mode == 'machine'):
            self._init_render(mode)
        elif mode == 'human':
            # update ball
            self.ball_plot.set_center((self.x, self.y))
            
            # update beam
            self.ax.lines[0].set(xdata=self.lim_x, ydata=self.lim_y)
            
            # update setpoint
            self.ax.patches[1].set_xy([
                [self.point*cos(self.theta), -0.01*self.L + self.point*sin(self.theta)],
                [self.point*cos(self.theta) - 0.015*self.L, -0.03*self.L + self.point*sin(self.theta)],
                [self.point*cos(self.theta) + 0.015*self.L, -0.03*self.L + self.point*sin(self.theta)]])

            # update figure
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        else:
            _ = self.ball_plot.set_center((self.x, self.y))
            _ = self.machine_ax.lines[0].set(xdata=self.lim_x, ydata=self.lim_y)
            _ = self.machine_ax.patches[1].set_xy([
                [self.point*cos(self.theta), -0.01*self.L + self.point*sin(self.theta)],
                [self.point*cos(self.theta) - 0.015*self.L, -0.03*self.L + self.point*sin(self.theta)],
                [self.point*cos(self.theta) + 0.015*self.L, -0.03*self.L + self.point*sin(self.theta)]])
            _ = self.machine_fig.canvas.draw()
            _ = self.machine_fig.canvas.flush_events()

    @property
    def on_beam(self):
        return self.lim_x[0] < self.x < self.lim_x[1]

    @property
    def balanced(self, margin=4):
        return round(self.theta, margin)==0 and round(self.a, margin)==0 and round(self.v, margin)==0 and round(self.x, margin)==self.setpoint