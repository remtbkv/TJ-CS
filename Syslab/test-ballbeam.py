import gym
import ballbeam_gym

# Create environment
env = gym.make('BallBeamSetpoint-v0')
observation = env.reset()


env.state = [0.1, 0.0, 0.0, -0.1]


for _ in range(1000):
    env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    if done:
        env.reset()
