"""
Purpose:
    - Python Project Template which includes
      - project structure
      - test stucture using pytest and coverage
      - configured logging, arg parsing and exception handling
      - .gitignore
      - LICENSE
      - README.md
      - requirements.txt

Usage:
    main.py [--hello]

Options:
    --hello        print "Hello World!"
"""
import docopt

def main():
    print("Hello World!")

if __name__=="__main__":
    main()