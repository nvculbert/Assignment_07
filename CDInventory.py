#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# nickculbert, 2021-Feb-21, added functions
# nickculbert, 2021-Feb-28, added error handling and pickling
#------------------------------------------#

# -- DATA -- #

import pickle
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dictRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage pickle file
objFile = None  # file object

# -- PROCESSING -- #

class DataProcessor:
    """Processing the data in inventory"""
    
    @staticmethod
    def add_tbl_item(intID, strTitle, strArtist, table): 
        """Adds items to the table lstTbl

        Args:
            intID (integer): CD's ID
            strTitle (string): CD's title
            strArtist (string): artist's name
            table (list of dicts): holds the CD inventory during runtime

        Returns:
            None.
        """
        dictRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dictRow)
        
    @staticmethod
    def CD_delete(intIDDel, table):   
        """Deletes a CD based on previous user input

        Args:
            intIDDel (integer): the ID of the CD to delete
            table (list of dicts): holds the CD inventory during runtime

        Returns:
            blnCDRemoved (boolean): tracks whether or not a CD
                                    was actually removed
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        return blnCDRemoved
        
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Ingests data from file to a list of dicts

        Reads the pickled data from file identified by file_name and assigns
        that data to the variable table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dicts): holds the CD inventory during runtime

        Returns:
            table (list of dicts): holds the CD inventory during runtime
        """
        table.clear()  # clears existing data and allows loading from file
        try:
            with open(file_name, 'ab+') as file:
                file.seek(0)
                table = pickle.load(file)
        except EOFError:
            print('Your CD Inventory is empty!')
        except Exception as e:
            print('There was an error...\n'
                  f'Error encountered: {e}\n')
        finally:
            return table

    @staticmethod
    def write_file(file_name, table):
        """Pickles current inventory data to text file

        Args:
            file_name (string): name of file used to read the data from
            table (list of dicts): holds the CD inventory during runtime

        Returns:
            None.
        """
        with open(file_name, 'ab') as file:
            pickle.dump(table, file)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('==== Menu === \n\n'
              '[l] load Inventory from file \n'
              '[a] Add CD\n[i] Display Current Inventory \n'
              '[d] delete CD from Inventory \n'
              '[s] Save Inventory to file \n'
              '[x] exit \n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input
            out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Please choose an operation: ').lower().strip()
        print()  # extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): holds the CD inventory during runtime

        Returns:
            None.

        """
        print()
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        print()
    
    @staticmethod
    def get_new_CD():
        """Gets user input for adding a new CD

        Args:
            None.

        Returns:
            intID (integer): CD's ID
            strTitle (string): CD's title
            strArtist (string): artist's name
        """
        intID = ''
        while type(intID) == str:
            try:
                intID = int(input('Enter ID: ').strip())
            except ValueError as e:
                print('Fail! You did not enter an integer.\n'
                      f'Error encountered: {e}\n'
                      'Please enter an integer....')
            except Exception as e:
                print('There was an error...\n'
                      f'Error encountered: {e}\n')
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, strArtist
        
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue,'
              ' all unsaved data will be lost'
              ' and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue'
                         ' and reload from file.'
                         ' Type anything else to cancel the reload: ')
        if strYesNo.lower() == 'yes':
            print('\nreloading...\n')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
        else:
            input('Canceling...Inventory data NOT reloaded.'
                  ' Press [ENTER] to continue to the menu.')
        IO.show_inventory(lstTbl)
        continue
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        intID, strTitle, strArtist = IO.get_new_CD()
        DataProcessor.add_tbl_item(intID, strTitle, strArtist, lstTbl)
        IO.show_inventory(lstTbl)
        continue
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        IO.show_inventory(lstTbl)
        intIDDel = ''
        while type(intIDDel) == str:
            try:
                intIDDel = int(input('Which ID would'
                                     ' you like to delete? ').strip())
            except ValueError as e:
                print('Fail! You did not enter an integer.\n'
                      f'Error encountered: {e}\n'
                      'Please enter an integer....')
            except Exception as e:
                print('There was an error...\n'
                      f'Error encountered: {e}\n')    
        cd_removed = DataProcessor.CD_delete(intIDDel, lstTbl)
        if cd_removed:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        continue
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        IO.show_inventory(lstTbl)
        strYesNo = input('Save inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file.'
                  ' Press [ENTER] to return to the menu.')
        continue
    
    # 3.7 catch-all should not be possible, but to be safe:
    else:
        print('General Error')




