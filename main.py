import sys

sma_period = sys.argv[1]
env_weight = sys.argv[2]

if len(sys.argv) != 3:
    print("ERROR: insufficient arguments")
    sys.exit()

sma_period = int(sma_period)
env_weight = float(env_weight)

print(f'PERIOD: {sma_period}, WEIGHT: {env_weight}')
print(f'type: {type(sma_period)}, type: {type(env_weight)}')
