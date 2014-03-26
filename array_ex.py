from array import *
import string

def sales_by_product(product_qty):
  """ You are given a 2 dimensional array of sales data where the 1st column is a product ID and the 2nd column is the quantity. Write a function to take this list of data and return a new 2 dimensional array with total sales for each Product ID """
  product_sales = {}
  
  for item in product_qty:
    vals = item.split(':')
    if vals[0] in product_sales:
      product_sales[vals[0]] += int(vals[1])
    else:
      product_sales[vals[0]] = int(vals[1])

  return product_sales

def reverse_elements_in_array(my_array):
  """ Reverse the order of elements in an array without creating a new array. """
  num = len(my_array)
  mod = num % 2
  mid = num/2 + mod
  last = num-1
  
  for i in range(mid):
    curVal = my_array[i]
    newVal = my_array[last]
    my_array[i] = newVal
    my_array[last]= curVal
    last += -1

  return my_array
    
def add_element_to_array(my_array, new_element):
  """ Given a sorted array of positive integers with an empty spot (zero) at the end insert an element in sorted order """
  my_array.append(new_element)
  sorted_array = sorted(my_array)
  
  return sorted_array

def main():
  sales = ['211:4','262:3','211:5','216:6']
  total_sales = sales_by_product(sales)
  for key in total_sales:
    print key, total_sales[key]

#   array_ex = array('i',[1,5,4,3,6,7,99])
#   print 'original array'
#   for x in array_ex:
#     print x
#   
#   reversed = reverse_elements_in_array(array_ex)
#   print 'reversed array'
#   for x in reversed:
#     print x
# 
#   added = add_element_to_array(array_ex, 8)
#   print 'added 8 and sorted array'
#   for x in added:
#     print x
    
if __name__ == '__main__':
  main()