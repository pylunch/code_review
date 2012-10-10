#! /usr/bin/env python
'''
ABOUT:
Plots contents of the 'missing' table in ql_log.db.  This script takes
an argument to plot a specific date range and an argument to plot specific
file types.  By default, all file types for all dates are plotted.

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
10/08/12 (Bourque)
'''

import argparse
import datetime
import re
import sqlite3
from datetime import datetime
import matplotlib.pyplot as mpl

# -----------------------------------------------------------------------------

def build_db_command(begin_date, end_date, filetypes):
    '''
    Builds a query for the ql_log.db database, based on the desired date range
    and desired file types.
    '''

    # With default parameters
    if filetypes == 'all' and begin_date == '' and end_date == '':
        command = 'SELECT date, flt, asn, drz, ima, jif, jit, jpg, raw, spt, '
        command += 'trl, crj FROM missing'
        filetypes = 'flt, asn, drz, ima, jif, jit, jpg, raw, spt, trl, crj'

    # With all fileytpes and specific date range
    elif filetypes == 'all' and begin_date != '' and end_date != '':
        command = 'SELECT date, flt, asn, drz, ima, jif, jit, jpg, raw, spt, '
        command += 'trl, crj FROM missing WHERE date BETWEEN "' + begin_date
        command += '" and "' + end_date + '"'
        filetypes = 'flt, asn, drz, ima, jif, jit, jpg, raw, spt, trl, crj'

    # With no begin or end date but specific filetypes
    elif filetypes != 'all' and begin_date == '' and end_date == '':
        command = 'SELECT date, ' + filetypes + ' FROM missing'

    # With specific date range and specific filetypes
    elif filetypes != 'all' and begin_date != '' and end_date != '':
        command = 'SELECT date, ' + filetypes + ' FROM missing '
        command += 'WHERE date BETWEEN "' + begin_date + '" and "'
        command += end_date + '"'

    return command, filetypes

# -----------------------------------------------------------------------------

def make_plot(data, filetypes, save_loc):
    '''
    Plots the data.
    '''

    data = zip(*data)

    # Convert dates to datetime format
    dates = [data[0][i] for i in range(len(data[0]))]
    converted_dates = []
    for date in dates:
        converted_dates.append(datetime.strptime(str(date), '%Y %m %d'))

    # Plotting parameters
    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.ylabel('Number of Missing Files')
    mpl.xlabel('Date')

    # Interpret filetypes for use in labels
    plot_labels = filetypes.split(',')
    plot_labels.insert(0, 'date')

    # Plot Date versus Number of Missing Files
    for i in range(1, len(data)):
        mpl.scatter(converted_dates, data[i], s = 5)
        mpl.plot(converted_dates, data[i], label = plot_labels[i])

    # Save plot
    mpl.legend(loc = 2)
    mpl.savefig(save_loc + 'missing_log_plot.png')
    mpl.clf()

# -----------------------------------------------------------------------------

def parse_args():
    '''
    Parse command line arguments, returns args object.
    '''

    # Create help strings
    begin_date_help = 'Plot begin date, in the form of "YYYY MM DD"'
    end_date_help = 'Plot end date, in the form of "YYYY MM DD"'
    filetype_help = 'File types to plot. The can be "all", one, or more of '
    filetype_help += 'the following: "flt", asn", "drz", "ima", "jif", "jit", '
    filetype_help += '"jpg", "raw", "spt", "trl", or "crj".'
    save_loc_help = 'Absolute path of save destination'

    # Add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--begin_date', dest = 'begin_date', action = 'store',
                        type = str, default = '', help = begin_date_help)
    parser.add_argument('--end_date', dest = 'end_date', action = 'store',
                        type = str, default = '', help = end_date_help)
    parser.add_argument('--filetypes', dest = 'filetypes', action = 'store',
                        type = str, default = 'all',  help = filetype_help)
    parser.add_argument('--save_loc', dest = 'save_loc', action = 'store',
                        type = str, default = '', help = save_loc_help)
    args = parser.parse_args()

    return args

# -----------------------------------------------------------------------------

def test_args(args):
    '''
    Ensures that the arguments are of proper format.  If they are not, an 
    assertion error is raised.
    '''

    # Assert that filetypes is of proper format
    filetypes_list = ['all', 'flt', 'asn', 'drz', 'ima', 'jif', 'jit', 'jpg']
    filetypes_list += ['raw', 'spt', 'trl','crj']
    filetypes_test = args.filetypes.split(',')
    for item in filetypes_test:
        assert item in filetypes_list, '%r is an invalid file type' % item

    # Assert that begin_date and end_date are of proper format
    re1= '((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}'             # Year
    re1+= '\\d{3})))(?![\\d])'
    re2= '(\\s+)'                                                 # White Space
    re3= '((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'         # Month
    re4= '(\\s+)'                                                 # White Space
    re5= '((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'         # Day
    re_test = re.compile(re1 + re2 + re3 + re4 + re5, re.DOTALL)

    if args.begin_date != '':
        assert bool(re_test.search(args.begin_date)) == True, \
                    '%r is of an invalid date format' % args.begin_date
    if args.end_date != '':
        assert bool(re_test.search(args.end_date)) == True, \
                    '%r is of an invalid date format' % args.end_date

    # Assert that end_date > begin_date
    if args.begin_date !=  '' or args.end_date != '':
        assert args.end_date > args.begin_date, 'End date is before begin date'

# -----------------------------------------------------------------------------
#   Main controller
# -----------------------------------------------------------------------------

def missing_log_plot(begin_date, end_date, filetypes, save_loc):
    ''''
    The main controller.
    '''

    database = '/grp/hst/wfc3a/Database/ql_log.db'

    # Open database connection
    conn = sqlite3.connect(database)
    conn.text_factory = str
    db_cursor = conn.cursor()

    # Build and execute command
    command, filetypes = build_db_command(begin_date, end_date, filetypes)
    db_cursor.execute(command)
    results = db_cursor.fetchall()

    # Send data to plotting function
    make_plot(results, filetypes, save_loc)

    # Close database connections
    conn.close()

# -----------------------------------------------------------------------------
# For command line execution
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    args = parse_args()
    test_args(args)
    
    missing_log_plot(args.begin_date, args.end_date, args.filetypes, 
                     args.save_loc)

