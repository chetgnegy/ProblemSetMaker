'''
Chet Gnegy
chetgnegy@gmail.com

A sample problem set using complex numbers



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


from random import randint
from cmath import *
from ProblemSet import *

from AnswerInterpreter import * 

def prepareHW():
  prob = {}
  for i in [1,2,3,4,5]:
    prob[i] = Problem()
    prob[i].question = "What are the roots of %0x^2 + %1x + %2?"
    prob[i].ordering_counts = False # Roots can be entered in any order
  prob[4].question = "What are the roots of %0x^3 + %1x^2 + %2x?"
    

  prob[1].data = [1, 2, 1]
  prob[2].data = [5, 6, 1]
  prob[3].data = [5, -2, 1]
  prob[4].data = [1, 2, 1]
  prob[5].data = [complex(0,1), complex(0,1), complex(0,1)]


  for i in [1,2,3,5]:
    prob[i].answer = [( -prob[i].data[1] + sqrt(prob[i].data[1]*prob[i].data[1] - 4*prob[i].data[0]*prob[i].data[2]))/(2*prob[i].data[0]),
                      ( -prob[i].data[1] - sqrt(prob[i].data[1]*prob[i].data[1] - 4*prob[i].data[0]*prob[i].data[2]))/(2*prob[i].data[0]) ]
  prob[4].answer = [-1, -1, 0]
 

  for i in [7,8,9,10,11,12,13]:
      prob[i] = Problem()
      prob[i].ordering_counts = False # Roots can be entered in any order
      prob[i].data = [complex(randint(-10, 10), randint(-10, 10))]
      while abs(prob[i] == 0):
        prob[i].data = [complex(randint(-10, 10), randint(-10, 10))]
    
  prob[7].question = "What is the real part of %0?"
  prob[7].answer = [prob[7].data[0].real]
  
  prob[8].question = "What is the imaginary part of %0?"
  prob[8].answer = [prob[8].data[0].imag]
  
  prob[9].question = "What is the modulus (magnitude) of %0?"
  prob[9].answer = [abs(prob[9].data[0])]
  
  prob[10].question = "What is the phase of %0?"
  prob[10].answer = [phase(prob[10].data[0])]
  
  prob[11].question = "What is the complex conjugate of %0?"
  prob[11].answer = [prob[11].data[0].real - complex(0,1)*prob[11].data[0].imag]
  
  prob[12].question = "What is the reciporical in rectangular form of %0?"
  prob[12].answer = [(1/(prob[12].data[0]))]
  
  prob[13].question = "What is the reciporical in polar form of %0? (Enter the magnitude then the phase)"
  prob[13].answer = [abs(1/(prob[13].data[0])),phase(1/(prob[13].data[0]))]
    


  return prob;








def main():
  prob = prepareHW()

  for i in prob:
    prob[i].ask()
    print "DEBUG:", prob[i].answer
    prob[i].poll_for_responses()

 
  
if __name__ == "__main__":
  main()