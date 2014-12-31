'''
Chet Gnegy
chetgnegy@gmail.com

A framework for building problem sets



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
import copy
from AnswerInterpreter import interpret 

class Problem:
  question = 0
  data = 0
  ordering_counts = False
  answer = 0
  eval_function = 0
  tolerance = 0.001

  # Checks to see if the entered question is in valid format. 
  # p.question must be set before calling this
  # Return: The number of variables used, or -1 if invalid
  def count_variables(self):
    #Tests if question is unset or is an invalid format
    if self.question == 0 or type(self.question) is not str: 
      print "You must enter a question! Use %0, %1 and so on for variables!"
      print "Example: p.question = \"What are the roots of %0x^2 + %1x + %2?\""
      return -1
    
    # Extract all instances of percent signs followed by numbers
    variables = re.findall(r'(%\d+)+', self.question)

    # No variables is not invalid, 1 doesn't need any additional checking
    if len(variables) < 2:
      return len(variables)

    var_strip = [int(var.strip('%')) for var in variables]
    #Remove duplicates and sort
    var_strip = sorted(list(set(var_strip)))

    #Makes sure sorted list of variables go from zero to len(vars)-1
    if (var_strip[0] == 0 and var_strip[-1] == len(var_strip) - 1):
      return len(var_strip)
    else:
      print 'You must enter variables in your question using the following format:' 
      print '\t %# \t where # is any integer. Variables must start at 0  ' 
      print '\t and end at N-1 where N is the number of used variables.'
      print '\t You may repeat variables or use them in any order, but don\'t.'
      print '\t leave any out!'
      print 'Example: p.question = "If Bill has %0 apples that are valued at' 
      print '\t %1 cents apiece, if Sally wants to buy %2 apples from '
      print '\t Bill, how much will she end up paying (remember, Bill '
      print '\t only has %0 and cannot sell more than that)?'

  # Tests to see if the problem has been entered correctly and that the data
  # has been provided.
  def validate_problem(self):
    num_vars = self.count_variables()
    #Make sure data is entered
    if self.data == 0:
      print 'You haven\'t entered any data. Use p.data. Must be in list format.'
      print 'Example: p.data = [3, 4, \"Blue\", complex(2,4)]' 
      return -1
    #Make sure proper amount of data is supplied
    if (num_vars != len(self.data)):
      print 'You must enter some data for each variable. You have ' + str(num_vars) 
      print 'variables. Use p.data.'
      print 'Example: p.data = [3, 4, \"Blue\", complex(2,4)]' 
      return -1
    #Make sure answer is entered
    if self.answer == 0:
      print 'You haven\'t entered any answers. Use p.answers.'
      print 'Example: p.answers = [3, 4, \"Blue\", complex(2,4)]' 
      return -1
    #Make sure answer is a list
    if type(self.answer) is not list:
      print 'Answer must be specified in a list, even if it only has one element!'
      return -1
    return True
    


  # Checks to see if the answer that has been given is correct. Uses the
  # default evaluation function or uses the specified one
  def check(self, guess):
    if type(guess) is not list:
      guess = [guess]
    if self.validate_problem() == -1:
      return -1
    if len(guess) != len(self.answer):
      print 'You haven\'t entered the correct amount of answers!'
      return -1
    
    if self.eval_function == 0:
      match = self.default_check__(guess)
    else:
      match = self.eval_function(guess)
      if match != True and match != False:
        error("Your evaluation function must return a boolean!") 
        return -1
    if (match): print "Correct" 
    else: print "Incorrect"     
    


  # Does the most basic check on answer. A test for equality.
  def default_check__(self, guess):
    # Answers have to be in specified order
    if self.ordering_counts:
      for i in range(len(self.answer)):
        if not self.test_single_answer(guess[i], self.answer[i]):
          return False
      return True
    else:
      # Answers can be in any order, make a copy of the answers and remove
      # Entries as they are found
      ans_copy = copy.deepcopy(self.answer)
      guess_copy = copy.deepcopy(guess)
      if len(guess) == 1:
        return self.test_single_answer(guess[0], self.answer[0])

      while len(ans_copy)>0:
        match = False
        i = 0
        for this_one in guess_copy:
          if self.test_single_answer(this_one,ans_copy[0]):
            del ans_copy[0]
            del guess_copy[i]
            i = i-1
            match = True
            break
          else: match = False
          i = i+1
        if not match: 
          return False
    return True


  # Verifies the a single answer, doing a check for tolerances, which can
  # be specified using p.tolerance
  def test_single_answer(self, guess, correct_answer):
    mathlist = [float,int] #Things that may have a mathematical tolerance

    # Must check real and complex part
    if type(correct_answer) is complex:
      if type(guess) is complex:
        realpart = self.test_single_answer(guess.real, correct_answer.real) 
        imagpart = self.test_single_answer(guess.imag, correct_answer.imag)
        return realpart and imagpart
      else:
        realpart = self.test_single_answer(guess, correct_answer.real) 
        imagpart = abs(correct_answer.imag) < self.tolerance
        return realpart and imagpart
    
    # Tests for a tolerance
    if type(guess) in mathlist and type(correct_answer) in mathlist:
      if (correct_answer == 0):
        return guess == 0;
      return abs((guess-correct_answer)/correct_answer) < self.tolerance

    # Simple comparison for non-math types, or simple math types
    return guess == correct_answer


  def ask(self):
    if self.validate_problem():
      # Extract all instances of percent signs followed by numbers
      variables = re.findall(r'(%\d+)+', self.question)
      var_strip = [int(var.strip('%')) for var in variables]
      ask_string = self.question
      # Sub out variables, one by one
      for var in var_strip:
        ask_string = re.sub(r'%'+str(var), str(self.data[var]), ask_string)
      print ask_string
  
  def poll_for_responses(self):
    guess = []
    for i in range(len(self.answer)):
      raw = raw_input("Your Answer: ")
      parsed = interpret(raw)
      guess.append(parsed)
    return self.check(guess)
