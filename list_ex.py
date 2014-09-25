def isSubset(a,b):
  """ Given two lists (A and B) of unique strings, write a program to determine if A is a subset of B. That is, check if all the elements from A are contained in B. """
  is_sub = False
  for item in a:
    if item in b:
      is_sub = True
    else:
      is_sub = False
      break
  
  return is_sub
  
def main():   
  players = ['Sherman','Lynch','Smith','Thomas']
  defense = ['Browner','Maxwell','Sherman','Smith','Thomas','Thurmond']
  print players, 'in', defense, '? ', str(isSubset(players,defense))
  
if __name__ == '__main__':
  main()