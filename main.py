#!/usr/bin/python
import sys
import pickle
from Lexer import Lexer
from Parser import Parser
from DFA import DFA
from PythonCodeGenerator import PythonCodeGenerator
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            scanner = Lexer(sys.argv[1])
        except Exception as e:
            print(e)
            print("""
                  
INPUT ERROR: Unable to open File! >>>
    use: python3 main.py <Grammar File dir>    
          
          """)
            exit(-1)
            
        parser = Parser(scanner)
        
        # Direct DFA
        dfa = DFA(
            parser.parse(parser.get_unique_expression()), 
            scanner.getCharacters(), 
            scanner.keywords, 
            scanner.ignore
        )
        pickle.dump(dfa, open('./temporal.p', 'wb'))

        PythonCodeGenerator('./generated_lexer.py', scanner.tokens, dfa).generate()

        print("""

The lexer has been written >>> lexer.py 

    use: python3 generated_lexer.py <File dir>

            """)
    else:
        
        print("""
INPUT ERROR: Submit the grammar File >>>
    use: python3 main.py <Grammar File dir>    
          
          """)