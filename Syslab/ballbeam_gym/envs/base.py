import time, gym
import numpy as np
from gym.utils import EzPickle
from gym.spaces import Box, Discrete
from ballbeam_gym.ballbeam import BallBeam

class BallBeamBaseEnv(gym.Env, EzPickle):
    def __init__(self, timestep=None, max_timesteps=None, unit_conversion=None, beam_length=None, ball_radius=None, max_angle=None, max_angle_change=None, init_velocity=None, setpoint=None, random_set=None, random_init_vel=None, sleep=None, action_mode=None):
        EzPickle.__init__(self)
        self.timestep = timestep
        self.max_timesteps = max_timesteps
        self.max_angle = max_angle
        self.max_angle_change = max_angle_change
        self.action_mode = action_mode
        if action_mode == 'continuous':
            self.action_space = Box(low=np.array([-max_angle], dtype=np.float32), high=np.array([max_angle], dtype=np.float32))
        elif action_mode == 'discrete':
            self.action_space = Discrete(3)
            self.angle = 0
        self.bb = BallBeam(timestep=timestep,
                           unit_conversion=unit_conversion,
                           beam_length=beam_length,
                           ball_radius=ball_radius,
                           max_angle=max_angle,
                           init_velocity=init_velocity, 
                           random_init_vel=random_init_vel,
                           setpoint=setpoint,
                           random_set=random_set,
                           sleep=sleep,
                           )
        self.goal = self.bb.get_goal()
        self.state = self.bb.get_state()
        self.max_state = self.bb.get_max_state()
        self.last_sleep = time.time()
        self.current_step = 0

    def _sleep_timestep(self):
        """ 
        Sleep to sync cycles to one timestep for rendering by 
        removing time spent on processing.
        """
        duration = time.time() - self.last_sleep
        if not duration > self.timestep:
            time.sleep(self.timestep - duration)
        self.last_sleep = time.time()

    def step(self):
        """
        Update environment for one action
        """
        self.current_step +=1

    def reset(self):
        self.current_step = 0
        self.goal = self.bb.get_goal()
        self.state = self.bb.reset()
        return self.state

    def render(self, button_info=None):
        """
        Render a timestep and sleep correct time
        """
        self.bb.render(button_info=button_info)
        self._sleep_timestep()

    def _action_conversion(self, action):
        """
            Convert action to proper domain action space (continuous)

            Parameters
            ----------
            action [continuous] : set angle, float (rad)
            action [discrete] : keep, increase, decrease angle, int [0, 1, 2]

            Returns
            -------
            action : set angle, float (rad)
            """
        if self.action_mode == 'discrete':
            self.angle += [-1, 0, 1][action]*self.max_angle_change
            self.angle = max(-self.max_angle, min(self.max_angle, self.angle))
            action = self.angle

        return action

    @property
    def done(self):
        """
        Environment has run a full episode duration OR IS COMPLETE?
        """
        if self.max_timesteps is None:
            done = not self.bb.on_beam
        else:
            done = self.current_step + 1 >= self.max_timesteps or not self.bb.on_beam or self.bb.balanced
        return done
