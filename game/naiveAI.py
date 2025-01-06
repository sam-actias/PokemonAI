import random

def naiveAiChoose(choices):
  if len(choices) == 1:
    return 0

  return random.randint(0, len(choices) - 1)