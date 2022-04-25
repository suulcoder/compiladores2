from Token import ExecuteToken
from Variable import Variable
from VariableGenerator import VariableGenerator
from NodeType import NodeType
from Character import Character
from Keyword import Keyword
from Token import Token
from Node import Node

COCO_RESERVED_WORDS = [
     'CHARACTERS',
     'COMPILER',
     'END',
     'IGNORE',
     'KEYWORDS', 
     'PRODUCTIONS',
     'TOKENS']


class Lexer:
    def __init__(self, filepath):
        self.compiler_name = None
        self.current_index = 0
        self.characters = []
        self.keywords = []
        self.tokens = []
        self.ignore = []

        self.read(filepath)
        self.getNextLine()

        self.processLines()
        self._characters = set()
        
    def getCharacters(self):
        for character in self.characters:
            self._characters.update(character.value)
        for token in self.tokens:
            for node in token.value:
                if node.type == NodeType["CHAR"] or node.type == NodeType["STRING"]:
                    self._characters.update(node.value)

        return self._characters

    #This file is useful to get the data from the file
    def read(self, filepath):
        lines = []
        for line in open(filepath, 'r').readlines():
            if line == '\n':
                pass
            else:
                #Add all the characters to a single string, 
                #Ignoring uneuseful characeters
                lines.append(
                    [character for character in 
                     line.strip().strip('\r\t\n').split(' ') 
                     if character != '' or character]
                )
        #Update lines
        self.lines =  lines

    #Get the next line
    def getNextLine(self):
        if(self.current_index  < len(self.lines)):
            self.current_line = self.lines[self.current_index]
            self.current_index += 1
        else:
            self.current_line = None

    #Get all tokens from the lines
    def processLines(self):
        #While there is a new line
        while self.current_line != None:
            #If compiler is in the line
            if 'COMPILER' in self.current_line:
                #We have the compiler name
                self.compiler_name = self.current_line[self.current_line.index(
                    'COMPILER')+1]
                self.getNextLine()
            #If ignore is in the line
            elif 'IGNORE' in self.current_line:
                #We generate a set of variables that we will ignore and delete
                self.ignore = VariableGenerator(
                    Variable(' '.join(self.current_line).split('IGNORE', 1)[1].replace('.', ''), self.characters).parse_variable(),
                    self.characters
                    ).generateVariable()
                self.getNextLine()
            elif 'KEYWORDS' in self.current_line:
                self.getNextLine()
                self.readLine('KEYWORDS')
            elif 'CHARACTERS' in self.current_line:
                self.getNextLine()
                self.readLine('CHARACTERS')
            elif 'TOKENS' in self.current_line:
                self.getNextLine()
                self.readLine('TOKENS')
            elif '(.' in self.current_line[:2]:
                self.readComment()
                self.getNextLine()
            else:
                self.getNextLine()

    def readComment(self):
        while not '.)' in self.current_line:
            self.getNextLine()

    def readLine(self, cocoWord):
        temporal_token = ''
        has_reserved_words = False
        for word in self.current_line:
            has_reserved_words = has_reserved_words or word in COCO_RESERVED_WORDS
        while not has_reserved_words:
            current_set = ' '.join(self.current_line)
            if '(.' in self.current_line:
                self.readComment()
                self.getNextLine()
            elif '.' == current_set[-1] and '=' in current_set  and temporal_token != '':
                current_set = current_set[:-1]
                if cocoWord == 'KEYWORDS':
                        self.execute_keywords(current_set)
                elif cocoWord == 'CHARACTERS':
                    self.execute_declarations(current_set)
                elif cocoWord == 'TOKENS':
                    self.execute_tokens(current_set)
                self.getNextLine()
            elif not '.' == current_set[-1]:
                temporal_token += current_set
                self.getNextLine()
            elif '.' == current_set[-1]:
                temporal_token += current_set
                temporal_token = temporal_token[:-1]
                if cocoWord == 'KEYWORDS':
                        self.execute_keywords(temporal_token)
                elif cocoWord == 'CHARACTERS':
                    self.execute_declarations(temporal_token)
                elif cocoWord == 'TOKENS':
                    self.execute_tokens(temporal_token)
                self.getNextLine()
            else:
                self.getNextLine()  
            has_reserved_words = False
            for word in self.current_line:
                has_reserved_words = has_reserved_words or word in COCO_RESERVED_WORDS

    def GenerateSet(self, eval_set):
        generator = VariableGenerator(eval_set, self.characters)
        generated_set = generator.GenerateSet()
        return generated_set

    def execute_tokens(self, line):
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        key_content = None

        if 'EXCEPT' in value:
            key_index = value.index('EXCEPT')
            key_content = value[key_index:]
            value = value[:key_index]
            
        self.tokens.append(Token(
            key,
            list(ExecuteToken(value, self.characters).parse(token_id=key)),
            key_content))

    def execute_keywords(self, line):
        key, value = line.split('=', 1)
        key = key.strip()
        value = Node(
            NodeType["STRING"], value.strip().replace('.', '').replace('"', '')
            )
        self.keywords.append(Keyword(key, value))

    def execute_declarations(self, line):
        key, value = line.split('=', 1)
        key = key.strip()
        self.characters.append(
            Character(key, 
                      VariableGenerator(list(Variable(
                          value, 
                          self.characters
                    ).parse_variable()),self.characters).generateVariable()
                )
            )