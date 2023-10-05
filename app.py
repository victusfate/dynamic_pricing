from flask import Flask, render_template, request
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from lib.RestaurantPricingEnv import RestaurantPricingEnv
import io
import sys

app = Flask(__name__)

env = DummyVecEnv([lambda: RestaurantPricingEnv()])

model = PPO("MlpPolicy", env, verbose=1)

def capture_logs(func):
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    func()
    sys.stdout = old_stdout
    return new_stdout.getvalue()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = ""
    logs = ""
    
    if request.method == 'POST' and 'timesteps' in request.form:
        timesteps = int(request.form['timesteps'])
        # Capture logs during training
        logs = capture_logs(lambda: model.learn(total_timesteps=timesteps))

    if request.method == 'POST' and 'action' in request.form:
        action = request.form['action']

        if action == 'Get Price':
            day_of_week = int(request.form['day_of_week'])
            hour = int(request.form['hour'])

            obs = np.array([0, 1, day_of_week, hour])
            action, _ = model.predict(obs)
            price_point = 10 + action
            results = f"Predicted Price for Day {day_of_week} and Hour {hour}: ${price_point}"

        elif action == "Generate Week's Prices":
            hour = int(request.form['hour_week'])
            prices = {}
            for day in range(1, 8):
                obs = np.array([0, 1, day, hour])
                action, _ = model.predict(obs)
                price_point = 10 + action
                prices[day] = price_point
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            results = "\n".join([f"{days[day-1]}: ${prices[day]}" for day in range(1, 8)])
    return render_template('index.html', results=results, logs=logs)    

if __name__ == "__main__":
    app.run(debug=True)
