from Program import Program
import os

def main(): 
    program = Program()

    # all file in INPUT folder
    INPUT_DIR = '../INPUT'
    files = [name.replace('.txt', '') for name in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, name))]

    print('Available input files: ')
    sFile = ''
    for file in files:
        sFile += file + '    '
    print(sFile)

    inputValid = False
    while not inputValid:
        file = input("Enter filename: ")
        inputValid = program.Input(filename=file)

    program.solve('UCS')
    program.solve('IDS')
    program.solve('GBFS')
    program.solve('A*')

    program.Output()

    program.visual()

if __name__ == "__main__":
    main()

