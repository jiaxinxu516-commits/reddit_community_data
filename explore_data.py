from data_loader import load_data
import json

data = load_data("data/reddit_rokid_glasses_data.json")

print(type(data))
print(len(data))

print(json.dumps(data[0], indent=4, ensure_ascii=False))