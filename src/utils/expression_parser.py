def parse(expression):
    command = []

    if expression is None:
        return command

    split_by_and = expression.split("and")

    for and_expression in split_by_and:
      split_by_symbol = and_expression.split()
      value = split_by_symbol[1]
      symbol = split_by_symbol[0]

      print(symbol, value)

      type = None
      if symbol == "<":
        type = "lt"
      elif symbol == ">":
        type = "gt"
      elif symbol == "=":
        type = "eq"
      elif symbol == "<=":
        type = "lte"
      elif symbol == ">=":
        type = "gte"
      elif symbol == "!=":
        type = "neq"

      command.append({"type": type, "value": value})

    return command
