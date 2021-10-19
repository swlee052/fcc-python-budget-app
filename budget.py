class Category:
  def __init__(self, name:str):
    self.ledger = list()
    self._balance = 0
    self._name = name

  def __str__(self):
    title = self._name.center(30, "*") + "\n"
    content = ""
    for rec in self.ledger:
      desc = rec["description"][:23]
      amnt = rec["amount"]
      content = content + '{desc:<23}{amnt:>7.2f}'.format(desc=desc, amnt=amnt) + "\n"
    total = f"Total: {self._balance}"
    return title + content + total 

  def get_name(self) -> str:
    return self._name

  def deposit(self, amount: int, description: str = "") -> None:
    self._add_record(amount, description)

  def withdraw(self, amount: int, description: str = "") -> bool:
    if not self.check_funds(amount):
      return False
    self._add_record(-amount, description)
    return True

  def transfer(self, amount: int, destination) -> bool:
    if not self.check_funds(amount):
      return False

    src = self._name
    dest = destination.get_name()
    self._add_record(-amount, f"Transfer to {dest}")
    destination.deposit(amount, f"Transfer from {src}")
    return True
  
  def check_funds(self, amount: int) -> bool:
    if amount > self._balance:
      return False
    return True

  def _add_record(self, amount: int, description: str = "") -> None:
    self.ledger.append({"amount": amount, "description": description})
    self._balance += amount
  
  def get_ledger(self) -> list:
    return self.ledger

  def get_balance(self) -> int:
    return self._balance

  


def create_spend_chart(categories):
  
  # get balance for each category
  category_percentage = dict()
  for c in categories:
    c_name = c.get_name()
    category_percentage[c_name] = 0
    ledger = c.get_ledger()
    for r in ledger:
      if r["amount"] < 0:
        category_percentage[c_name] += -r["amount"]
  total = sum(category_percentage.values())
  
  # compute percentage for each category
  for c in categories:
    c_name = c.get_name()
    category_percentage[c_name] /= total
    category_percentage[c_name] *= 100



  output = "Percentage spent by category"

  # percentages
  for p in range(100, -10, -10):
    eachLine = f"{p}| ".rjust(5, " ") 
    for c in categories:
      c_name = c.get_name()
      c_per = category_percentage[c_name]
      if c_per >= p:
        eachLine = eachLine + "o  "
      else:
        eachLine = eachLine + "   "
    output = output + "\n" + eachLine

  # line
  output = output + "\n" + " "*4 + "-"*(3*len(categories)+1)

  # category names
  maxLen = max([len(c.get_name()) for c in categories])
  for i in range(0, maxLen): 
    eachLine = " "*5 
    for category in categories:   
      cat_name = category.get_name()
      charOrSpace = ""
      if i < len(cat_name):
        charOrSpace = cat_name[i]
      else:
        charOrSpace = " "
      eachLine = eachLine + charOrSpace + "  "
    output = output + "\n" + eachLine
  return output