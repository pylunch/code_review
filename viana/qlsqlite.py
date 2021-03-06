{
 "metadata": {
  "name": "qlsqlite_test"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "Tests for QLSQLite\n",
      "------------------\n",
      "\n",
      "These are some tests for the QLSQLite class. They requite the sqlite3 module and a working SQLite backend"
     ]
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import sqlite3\n",
      "\n",
      "class QLSQLite(object):\n",
      "    def __init__(self, database, verbose=False):\n",
      "        assert isinstance(verbose, bool), 'Verbose must be boolean.'\n",
      "        self.verbose = verbose\n",
      "        self.database = database\n",
      "        self.connection = sqlite3.connect(self.database)\n",
      "        \n",
      "    def __getattr__(self, method_name):\n",
      "        return getattr(self.connection, method_name)\n",
      "    \n",
      "    def close(self):\n",
      "        self.connection.close()\n",
      "    \n",
      "    def commit(self):\n",
      "        self.connection.commit()   \n",
      "  \n",
      "    def insert(self, table, input_dict):\n",
      "        command = 'INSERT INTO ' + table + ' ('\n",
      "        for key in input_dict:\n",
      "            command += '\"' + key +'\",'\n",
      "        command = command[:-1]\n",
      "        command += ') values ('\n",
      "        for key in input_dict:\n",
      "\t        command += '\"' + str(input_dict[key]) + '\",'\n",
      "        command = command[:-1]\n",
      "        command += ')'\n",
      "        self.run_cursor(command)\n",
      "        \n",
      "    def insert_or_update(self, table, input_dict, field_to_check):\n",
      "        id = self.select_id(table, field_to_check, input_dict[field_to_check])\n",
      "        if id == []:\n",
      "            self.insert(table, input_dict)\n",
      "        else:\n",
      "            for id_item in id:\n",
      "                self.update(table, input_dict, id_item[0])\n",
      "    \n",
      "    def run_cursor(self, command):\n",
      "        if self.verbose:\n",
      "            print command\n",
      "        cursor = self.cursor()\n",
      "        cursor.execute(command)\n",
      "        output = cursor.fetchall()\n",
      "        cursor.close()\n",
      "        if output != []:\n",
      "            return output\n",
      "\n",
      "        \n",
      "    def select_id(self, table, field, condition):\n",
      "        command = 'SELECT id FROM ' + table + ' WHERE ' + field + ' = \"' + str(condition) + '\"'\n",
      "        cursor = self.cursor()\n",
      "        cursor.execute(command)\n",
      "        id = cursor.fetchall()\n",
      "        cursor.close()\n",
      "        return id\n",
      "\n",
      "    def update(self, table, input_dict, id):\n",
      "        command = 'UPDATE OR ROLLBACK ' + table + ' SET '\n",
      "        for key in input_dict:\n",
      "            command += '\"' + key + '\" = \"' + str(input_dict[key]) + '\",'\n",
      "        command = command[:-1]\n",
      "        command += ' WHERE id = \"' + str(id) + '\"'            \n",
      "        self.run_cursor(command)"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 13
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "foo = QLSQLite('test.db', verbose = True)"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 14
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "test_dict = {'id':1, 'filename':'bar','status':'Derp'}"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 15
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "foo.insert('test', test_dict)"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "INSERT INTO test (\"status\",\"id\",\"filename\") values (\"Derp\",\"1\",\"bar\")\n"
       ]
      }
     ],
     "prompt_number": 16
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "foo.update('test', test_dict, 1)"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n"
       ]
      }
     ],
     "prompt_number": 17
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "foo.run_cursor('SELECT * FROM test')"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "SELECT * FROM test\n"
       ]
      },
      {
       "output_type": "pyout",
       "prompt_number": 18,
       "text": [
        "[(u'1', u'bar', u'Derp'),\n",
        " (u'1', u'bar', u'Derp'),\n",
        " (u'1', u'bar', u'Derp'),\n",
        " (u'1', u'bar', u'Derp'),\n",
        " (u'1', u'bar', u'Derp'),\n",
        " (u'1', u'bar', u'Derp'),\n",
        " (u'1', u'bar', u'Derp'),\n",
        " (u'1', u'bar', u'Derp'),\n",
        " (u'2', u'bar', u'777'),\n",
        " (u'1', u'bar', u'Derp')]"
       ]
      }
     ],
     "prompt_number": 18
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "foo.insert_or_update('test', test_dict, 'id')"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n",
        "UPDATE OR ROLLBACK test SET \"status\" = \"Derp\",\"id\" = \"1\",\"filename\" = \"bar\" WHERE id = \"1\"\n"
       ]
      }
     ],
     "prompt_number": 19
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "foo.commit()"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 146
    },
    {
     "cell_type": "code",
     "collapsed": true,
     "input": [
      "foo.close()"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 20
    },
    {
     "cell_type": "code",
     "collapsed": true,
     "input": [],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": "&nbsp;"
    }
   ],
   "metadata": {}
  }
 ]
}