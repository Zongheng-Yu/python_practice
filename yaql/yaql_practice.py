import yaql
import yaml

print dir(yaql)

data_source = yaml.load(open('data.yaml', 'r'))
engine = yaql.factory.YaqlFactory().create()
expression = engine(
    '$.customers.orders.selectMany($.where($.order_id = 4))')
order = expression.evaluate(data=data_source)
print order

bytes
