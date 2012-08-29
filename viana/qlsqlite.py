import sqlite3

class QLSqlite(object):
    '''
	This class extends the sqlite3 connection/cursor object for common 
	quicklook tasks.
	'''
    def __init__(self, database):
		'''
		Sets up a connection object and cursor object as attributes. 
		Both can be be called as normal.
		'''
        self.database = database
        self.connection = sqlite3.connect(self.database)
        self.c = self.connection.cursor()
    
    def close(self):
		'''
		Closes the connection.
		'''
        self.connection.close()
    
    def commit(self):
		'''
		Commits any changes.
		'''
        self.connection.commit()   
  
    def insert(self, table, input_dict, verbose = False):
        '''
		Runs an insert command over a dictionary.
		'''
		assert type(input_dict) == dict, 'input_dict must be a dict type.'
		command = 'INSERT INTO ' + table + ' ('
        for key in input_dict:
            command += '"' + key +'",'
        command = command[:-1]
	    command += ') values ('
	    for key in input_dict:
	        command += '"' + str(input_dict[key]) + '",'
	    command = command[:-1]
	    command += ')'
        if verbose == True:
            print command
        self.c.execute(command)
        
    def insert_or_update(self, table, input_dict, field_to_check, verbose = False):
		'''
		Checks for the existence of a field called field_to_check with 
		a value matching the value in input_dict. If none is found the 
		input_dict values are inserted. If matching records are found 
		they are updated.
		'''
        id = self.select_id(table, field_to_check, input_dict[field_to_check])
        if id == []:
            self.insert(table, input_dict, verbose)
        else:
            for id_item in id:
                self.update(table, input_dict, id_item[0], verbose)
        
    def select_id(self, table, field, condition):
		'''
		Returns the id that matches the condition for the field.
		'''
        command = 'SELECT id FROM ' + table + ' WHERE ' + field + ' = "' + str(condition) + '"'
        self.c.execute(command)
        id = self.c.fetchall()
        return id

    def update(self, table, input_dict, id, verbose = False):
		'''
		Updates the field that matches the id.
		'''
        command = 'UPDATE OR ROLLBACK ' + table + ' SET '
        for key in input_dict:
            command += '"' + key + '" = "' + str(input_dict[key]) + '",'
        command = command[:-1]
        command += ' WHERE id = "' + str(id) + '"'            
        if verbose == True:
            print command   
        self.c.execute(command)

