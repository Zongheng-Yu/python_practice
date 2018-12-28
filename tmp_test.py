import json

raw_string = '[{"a":"aa", "b":"bb"},{"c":"cc", "d":"dd"}]'
obj = json.loads(raw_string)
print(obj)
print(obj[0])
