import random
import math

def genNum(n = 16): #from 1 to n, inclusive
  return random.randint(1, n)

def lie(count):
  return count == WHENLIE

def check(secret, cond, count):
  ans = True
  if type(cond) == int: ans = secret == cond
  else: ans = cond(secret)
  return not ans if lie(count) else ans

def initGuess(checks, n):
  lower = 1
  upper = n
  for c in checks[::-1]:
    if c:
      lower += n//2
    else:
      upper -= n//2
    n = n//2
  if lower != upper: print("WHAT")
  return lower

def indexize(checks):
  ans = checks.copy()
  for i in range(len(ans)):
    ans[i] = (i+1, checks[i]) #1 to 4
  return ans

def genChecksChecker(indexed_checks):
  def cond(secret):
    for i in indexed_checks:
      cur = pow(2, i[0])
      if (secret%cur == 0 or secret%cur > cur//2) != i[1]: return False
    return True
  return cond

  #return boolean function

def alterChecks(checks, change): #change = (3, False)
  ans = checks.copy()
  ans[change[0]-1] = not change[1]
  return ans

def guess(secret: int, n: int):
  count = 0
  checks = []
  logn = math.ceil(math.log2(n))
  for i in range(logn): #16, 8, 4, 2
    count += 1
    cur = pow(2, i+1)
    cond = lambda secret: secret%cur == 0 or secret%cur > cur//2
    checks.append(check(secret, cond, count))
  #print(checks)

  init = initGuess(checks, n)
  #print(init)
  isInit = lambda secret: secret == init
  count += 1
  if check(secret, isInit, count): return (init, count)
  count += 1
  if check(secret, isInit, count): return (init, count)
  #lie already used
  indexed_checks = indexize(checks)
  #print(indexed_checks)
  while len(indexed_checks) > 2:
    #print(indexed_checks)
    front = indexed_checks[:len(indexed_checks)//2]
    back = indexed_checks[len(indexed_checks)//2:]
    count += 1
    ans = check(secret, genChecksChecker(front), count)
    indexed_checks = front if not ans else back
  #print(indexed_checks)
    
  secondlastguess = initGuess(alterChecks(checks, indexed_checks[0]), n)
  #print(secondlastguess)
  count += 1
  if check(secret, secondlastguess, count): return (secondlastguess, count)

  #print(lastguess)
  lastguess = initGuess(alterChecks(checks, indexed_checks[1]), n)
  count += 1
  return (lastguess, count)


n = 8
upper = int(math.pow(2, n))
print("upper: ", upper)

WHENLIE = random.randint(1, n)

print("expected: ", n+math.floor(math.log2(n))+2)

print("whenlie: ", WHENLIE)

avg = 0
for i in range(1, upper+1):
  ans = guess(i, upper)
  if ans[0] != i: print("ERROR: ", i, ans[0])
  avg += ans[1]

print("average: ", avg/upper)


#print(initGuess([False, True, False, False, False, False, True, True], 256))
