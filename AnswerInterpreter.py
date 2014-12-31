'''
Chet Gnegy
chetgnegy@gmail.com

A script for interepereting input involving complex numbers



The MIT License (MIT)

Copyright (c) 2014 Chet Gnegy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import re

class Term:
  desc = ""
  negative = False
  imaginary = False
  inverse = False
  val = None

  def __str__(self):
    s = ''
    if self.negative: s += "-"
    if self.inverse: s += "1/"
    if self.val != None:
      if self.imaginary: s += "j"
      return s+str(self.val)
    else:
      return s+str(self.desc)

def error(msg):
  print msg
  exit()

def interpret(query):
  if type(query) is not str:
    return query

  # Converts string number to numerical type
  if (predict_number(query) or predict_complex(query)):
    # Double negatives mean plus
    query = query.replace('--','+')
    query = fix_minuses(query)
    query = fix_imaginaries(query)
    # Double characters are problematic
    violation = re.findall(r'([\+\*/])([\+\*/])+', query)
    if len(violation):
      error(">> Parse error: multiple consecutive operators")
    if query[0] in '\+\*/' or query[-1] in '\+-\*/':
      error(">> Stray operator found in symbol"+ query)

    return term_to_value(evaluate_string__no_parens(query))

  return query

# Reduces a string to a real term and an imaginary term. Returns them in
# a list with the real part first. String must not contain parenthesis
def evaluate_string__no_parens(query):
  all_addends = []
  # Handles addition and subtraction
  for term in aunt_sally(query):
    term_m = my_dear(term.desc)
    post_multiply = get_product(term_m)
    if term.negative:
      post_multiply.negative = not post_multiply.negative
    
    # Combine multiplicative terms
    all_addends.append(post_multiply)

  zero = Term()
  zero.val = 0
  # Group real and imaginary
  real = [t for t in all_addends if not t.imaginary]
  imag = [t for t in all_addends if t.imaginary]
  # Combine additive terms
  real_part = get_sum(real) if len(real) else zero
  imag_part = get_sum(imag) if len(imag) else zero
  
  return [real_part, imag_part]



# Converts a term or list of terms to a numerical value
def term_to_value(terms):
  zero = Term()
  zero.val = 0
  # Group real and imaginary
  real = [t for t in terms if not t.imaginary]
  imag = [t for t in terms if t.imaginary]
  # Combine multiplicative terms
  real_part = get_sum(real) if len(real) else zero
  imag_part = get_sum(imag) if len(imag) else zero

  if type(terms) is not list:
    terms = [terms]
  # Returns in a number format
  if imag_part.val == 0:
    return real_part.val if not real_part.negative else -real_part.val
  else:
    return complex(real_part.val if not real_part.negative else -real_part.val,
      imag_part.val if not imag_part.negative else -imag_part.val)

# Tries to tell if the entered string should be parsed to a number or not
def predict_number(query):
  # There is a stray letter or two. Not a number
  if any(letter in 'abcdefghijklmnopqrstuvwxyz' for letter in query): 
    return False# All numbers are digits, simple operations, or imaginary coefficients
  if all(letter in '0123456789.+-*/' for letter in query): 
    return True
  return False



# Tries to tell if the entered string should be parsed to a complex number or not
def predict_complex(query):
  query = query.replace(' ','')
  # Check if imaginary number used
  contains_i = 'i' in query 
  contains_j = 'j' in query
  strange_looking = 'ii' in query or 'jj' in query
  # Contains no i's or j's. If it contains both, 
  # it's silly and isn't a good complex number
  if contains_i == contains_j or strange_looking:
    return False
  # There is a stray letter or two. Not complex.
  if any(letter in 'abcdefghklmnopqrstuvwxyz' for letter in query): 
    return False
  # All numbers are digits, simple operations, or imaginary coefficients
  if all(letter in '0123456789.+-*/ij' for letter in query): 
    return True




# A parser that only looks for the addition and subtraction operations
# returns a list of Term objects whose only valid fields are the 
# description and whether it is positive or negative. This ignores 
# parenthesis
def aunt_sally(query):
  query = query.strip() #lose the spaces
  terms = []
  # Addition Layer
  addends = [i for i in query.split('+') if i != '']
  for addend in addends:
    addend = addend.strip() #lose the spaces
    
    # Subtraction Layer
    t = Term()
    if addend.count('-')%2 == 1:
      t.negative = True 
    addend = addend.replace('-','')
    t.desc = addend.strip()
    terms.append(t)
  return terms



# A parser that only looks for the multiplication and divison operations
# returns a list of Term objects whose only valid fields are the 
# description and whether it is positive or negative. This ignores 
# parenthesis
def my_dear(query):
  query = query.strip() #lose the spaces
  terms = []
  #Multiplication Layer
  multiplicands = query.split('*')
  if query[0] == '*' or query[-1] == '*':
    error(">> Parse Error at token '*' for symbol "+ query)
  for multiplicand in multiplicands:
    multiplicand.strip() #lose the spaces
    #Division Layer
    dividends = multiplicand.split('/')
    # Out of place divide symbol
    if multiplicand[0] == '/' or multiplicand[-1] == '/':
      error(">> Parse Error at token '/' for symbol "+ multiplicand)
    #The first term is not an inverse
    t = parse_token(dividends[0])
    terms.append(t)
    #The rest of the terms are inverses
    for dividend in dividends[1:]:
      t = parse_token(dividend)
      t.inverse = True
      if (t!=-1):
        terms.append(t)
  return terms




# Pareses a single token, which no longer contains any operators,
# only digits, decimals, and imaginary terms
def parse_token(query):
  query = query.strip()
  # All numbers are digits, simple operations, or imaginary coefficients
  if not all(letter in '0123456789.ij ' for letter in query): 
    error(">> Parse error for symbol "+ query)
  if query.count('.') > 1:
    error(">> Parse error at token '.' for symbol "+ query)
  contains_i = 'i' in query 
  contains_j = 'j' in query
  
  # Multiple complex coefficients in a row
  if 'ii' in query or 'jj' in query:
    error(">> Repeated complex coefficients disallowed for symbol "+ query)
  t = Term()
  t.desc = query
  
  # If it is a complex number
  if contains_i or contains_j:
    complex_term = 'i' if 'i' in query else 'j'
    # Spaces near complex terms can be removed
    query = complex_term.join([i.strip() for i in query.split(complex_term)])
    # The query is just 'i' or 'j'
    if query == complex_term: 
      t.val = 1
      t.imaginary = True
      return t
    if query[0] != complex_term and query[-1] != complex_term:
      if contains_i: error(">> Parse error at token 'i' "+ query)
      elif contains_j: error(">> Parse error at token 'j' "+ query)
    
    query = query.replace(complex_term,'')
    t.imaginary = True
  
  if ' ' in query:
    error(">> Unexpected whitespace for symbol "+ query)
  
  # Handle numerical info
  if '.' in query:
    t.val = float(query)
  else:
    t.val = int(query)
  return t
  


# Multiplies a list of terms together and returns a product term.
# Assumes signs are already stripped from terms and put in 'negative'
# field with their val fields assigned
def get_product(terms):
  if type(terms) is not list:
    error(">> Error in get_product: Expected list")
  if len(terms)== 1:
    return terms[0] 
  result = Term()
  result.val = 1;
  for term in terms:
    if term.val == None:
        error(">> Val not set in token "+ term.desc)
    # Division
    if term.inverse:
      if term.val == 0:
        error(">> Divide by zero error")
      #1/i = -i, no integer division
      if term.imaginary!=term.negative: 
        result.negative = not result.negative 
      result.val *= 1 / (1.0*term.val)
    # Multiplication
    else:
      if term.negative:
        result.negative = not result.negative
      result.val *= 1 * term.val
    # i * i = -1
    if term.imaginary and result.imaginary:
      result.negative = not result.negative
    result.imaginary = term.imaginary != result.imaginary

  return result



# Combines several terms into one additively. Terms must either
# all be imaginary or all real
def get_sum(terms):
  sum_term = Term()
  if all(t.imaginary for t in terms):
    sum_term.imaginary = True
  elif all(not t.imaginary for t in terms):
    sum_term.imaginary = False
  else:
    error(">> get_sum cannot add real and imaginary components")
  sum_term.val = 0

  for t in terms:
    if t.negative:
      sum_term.val -= t.val
    else: 
      sum_term.val += t.val
  if sum_term.val < 0:
    sum_term.val = abs(sum_term.val)
    sum_term.negative = True
  return sum_term



# It is easier to parse a string where all the minuses are unary than
# one where binary and unary minuses are mixed. For that reason, we make
# them all unary
def fix_minuses(query):
  # Remove spaces surrounding operators
  query = "+".join([seg.strip() for seg in query.split("+")])
  query = "-".join([seg.strip() for seg in query.split("-")])
  query = "*".join([seg.strip() for seg in query.split("*")])
  query = "/".join([seg.strip() for seg in query.split("/")])
  i=1
  # Add plusses in front of minus signs to correct any unary minuses
  while i < len(query):
    if query[i] == '-':
      if query[i-1] not in '+*/':
        query = query[:i]+'+'+query[i:]
        i=i-1
    i=i+1    

  return query

# Replaces 4j with 4*j. Just makes things explicit for order of operations later
def fix_imaginaries(query):
  query = "i".join([seg.strip() for seg in query.split("i")])
  query = "j".join([seg.strip() for seg in query.split("j")])
  i = 1
  while i < len(query):
    if query[i] == 'i' or query[i] == 'j':
      if query[i-1] in '0123456789':
        query = query[:i]+'*'+query[i:]
        i=i-1
    i=i+1    
  return query


 