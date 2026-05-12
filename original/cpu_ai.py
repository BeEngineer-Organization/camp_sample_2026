# cpu_ai.py
import random

def think_action(cpu_info):
    """何も考えず、手札からランダムに1枚出すだけのCPU"""
    return random.choice(cpu_info["own_hand"])

