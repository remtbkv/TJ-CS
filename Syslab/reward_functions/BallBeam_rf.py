def user_reward(self):
	pos, vel, ang = self.state
	K_pos, K_vel, K_ang = self.reward_scale
	setpoint = self.goal
	return -(pos-setpoint)**2
