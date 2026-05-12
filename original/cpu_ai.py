# cpu_ai.py
import random

def think_action(p1_info):
    """何も考えず、手札からランダムに1枚出すだけのCPU"""
    return random.choice(p1_info["my_hand"])

