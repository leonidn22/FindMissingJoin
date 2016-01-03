__author__ = 'lneizberg'
import os
import re
from os.path import join as path_join
import fnmatch
from stat import *
from operator import itemgetter

files_to_process = []
tables = []
dir = 'C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database'
#dir = 'C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\Editing\Shadow\Stored Procedures'
#dir = 'C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\Advanced Search'
#dir = 'C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\Editing'
#dir = 'C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\DP_Permissions\Shadow'
#dir = 'C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\AE\Shadow\Stored Procedures'
# dir = 'C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\GUI\Shadow\Stored Procedures'

files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\GUI\Shadow\Stored Procedures\ReviewAreaGraph-sp.sql']
files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\GUI\Shadow\Stored Procedures\DirectoriesView-sp.sql']
files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\GUI\Shadow\Stored Procedures\ReviewArea-sp.sql']
files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\AE\Shadow\Stored Procedures\SyncDual-sp.sql']
files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\Secure Migration\Shadow\Stored Procedures\RuleSummary.sql']
files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\DFS\Shadow\Stored Procedures\DFSPAthManipulations-sp.sql']
files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\AE\Shadow\Stored Procedures\SyncDual-sp.sql']
files_to_process = ['C:\\TFS\\Branches\\V6.3\\Development\\V6.3 [UnifiedDB]\\Database\\Pulling File Walk\\Shadow\\Stored Procedures\\DP-Logical-PullFileWalk-sp.sql']
files_to_process = ['C:\TFS\Branches\V6.3\Development\V6.3 [UnifiedDB]\Database\Secure Search\Shadow\Stored Procedures\RulePrepare-sp.sql']
#files_to_process = ['C:\\\\Users\\\\lneizberg\\PycharmProjects\\SProcs\\commentTest.sql']
process_files_from_dir = False
ext = 'sql'

tableList = 'C:\\Users\\lneizberg\\PycharmProjects\\SProcs\\tableList.txt'
#tableList = 'C:\\Users\\lneizberg\\PycharmProjects\\SProcs\\tableListVarTable.txt'
procList = 'C:\\Users\\lneizberg\\PycharmProjects\\SProcs\\procList.txt'
# tableList = ["SortedDirectoryTree"]


def get_files_to_process(dir,ext):

    for f in os.listdir(dir):
        pathname = os.path.join(dir, f)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            get_files_to_process(pathname,ext)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            if os.path.splitext(pathname)[1].replace('.','') == ext and '\\Shadow\\Stored Procedures\\' in pathname:
                files_to_process.append(pathname)
                #print pathname
        else:
            # Unknown file type
            pass
    return files_to_process


def findSps():

    with open(tableList,'r') as f:
        tables = f.read().splitlines()
    #tables = tuple(open(tableList, 'r'))
    tables.append('filer')
    tables.append('filerID')
    #print tables
    for table in tables:
        for f in files_to_process:
            content = open(f,'r').read();
            #if ('procedure' in content) and (table in content):
            if (table in content):
                print " %s exists in %s" %(table, f) ;
        pass
    pass

def findSpsByFile():

    pattern_comment = re.compile(' *--.*', re.IGNORECASE)
    pattern_comment_aster_begin = re.compile('.*/\*.*', re.IGNORECASE)
    pattern_comment_aster_end = re.compile('.*/*/\.*', re.IGNORECASE)
    pattern_comment_aster_begin_end = re.compile('/\*[\S\s]*?\*/', re.IGNORECASE)
    pattern_comment_aster_begin = re.compile('/\*.*[^\*/].*', re.IGNORECASE)
    # '/\*[\S\s]*?\*/'

    with open(tableList,'r') as f:
        tables = f.read().splitlines()
    # tables = tuple(open(tableList, 'r'))
    # tables.append('filer')
    # tables.append('filerID')
    # print tables
    count_to_fix = 0
    lines_dict = {}
    for f in files_to_process:
        print f
        lines_dict.clear()
        with open(f, 'r') as f:
            lines = f.read().splitlines()
        for table in tables:
            # table_regex = '.*(from|join|left join).{0,12}'+table+' .{0,12}?(?P<alias>[a-zA-Z0-9_]+)'
            # find lines with alias at the end of line or long lines with table in the middle
            table_regex = r'.*( |from|join|left join){0,12}(?<!#)(\s|\.)[[]?'+table+'[]]?( as | |\)){1,12}(?P<alias>[a-zA-Z0-9_]+)'
            # table_regex = r'.*(from|join|left join){0,1}( |dbo\.){1,12}(?<!#)[[]?'+table+'[]]?( as | |\)){1,12}(?P<alias>[a-zA-Z0-9_]+)'
            # find if string empty after the table or alias
            # save  table_regex = r'.*(from|join|left join).{1,12}[^#][[]?'+table+'[]]?( as | |\))?(?P<alias>[a-zA-Z0-9_]+)'
            table_regex_end = r'.*(from|join|left join).{1,12}'+table+'( ?P<alias>[a-zA-Z0-9_]+)'
            # table_regex = '.*(from|join|left join).{1,15}'+table+'?(?P<alias>[a-zA-Z0-9_]+)'
            pattern_table = re.compile(table_regex, re.IGNORECASE)
            pattern_table_end = re.compile(table_regex_end, re.IGNORECASE)
            # content = open(f,'r').read();
            # if ('procedure' in content) and (table in content):
            # loop by file lines
            for idx,line in enumerate(lines):
                # if (table in line):
                # if(re.match(pattern_pool, line)):

                # replace multiply blank to one
                line = ' '.join(line.split()) + ' '
                # if re.match(pattern_comment_aster_begin,line):
                #      print 'Line %s Begin comment %s ' % (idx,line)
                # if re.match(pattern_comment_aster_end,line) and not re.match(pattern_comment_aster_begin, line):
                #      print 'Line %s End comment %s ' % (idx,line)
                # print 'Line number %s Line -  %s ' % (idx,line)
                match_table = pattern_table.search(line)
                match_table_end = pattern_table_end.search(line)
                alias = 'none'
                if match_table and not re.match(pattern_comment, line):
                        # and not re.match(pattern_comment_aster_begin_end, line):
                    alias = match_table.group('alias')
                    if alias is None:
                        alias = ''
                        #alias = '('+table +'){0,1}'
                    if alias.lower() in ('where','with','set'):
                        alias = ''
                        #alias = '('+table +'){0,1}'
                    if alias.lower() == 'on':
                        alias = table
                   # print "match_table line number - %s; alias=%s ;line -  %s" % (idx, alias, line)
                elif match_table_end and not re.match(pattern_comment, line):
                    alias = match_table_end.group('alias')
                    if alias is None:
                        alias = ''
                        #alias = '(|'+table +')'
                    if alias.lower() == 'where':
                        alias = ''
                        #alias = '(|'+table +')'
                    if alias.lower() == 'on':
                        alias = table
                    print "Match_table_END line number - %s; alias=%s ;line -  %s" % (idx, alias, line)
                # print
                if alias != 'none':
                    detected = False
                    # loop for 35 lines down
                    for line_join in lines[idx:idx+35]:
                        if re.match(pattern_comment, line_join):
                            continue
                        line_join = ' '.join(line_join.split())
                        join_field = 'FilerID'
                        if table.lower() in ('shares', 'tmp_shares', 'filers'):
                            join_field = 'filer_id'
                        if alias != '':
                            alias_regex1 = '.*(and|where) '+alias+'.'+join_field+' {0,1}='
                            alias_regex2 = '.*= '+alias+'\.'+join_field+' '
                        else:
                            alias_regex1 = '.*(and|where) ('+alias+'|'+table+'\.'+'){0,1}'+join_field+' {0,1}='
                            #alias_regex1 = '.*(and|where) ['+table+'\.'+']{0,1}'+join_field+' {0,1}='
                            alias_regex2 = '.*= '+alias+''+join_field+' '
                        pattern_join1 = re.compile(alias_regex1, re.IGNORECASE)
                        pattern_join2 = re.compile(alias_regex2, re.IGNORECASE)
                        if re.match(pattern_join1, line_join) or\
                                re.match(pattern_join2, line_join):
                            #print ('Detected join %s' %line_join)
                            detected = True
                            break
                    if not detected:
                        lines_dict[idx] = alias
                        count_to_fix = count_to_fix + 1
        # print result for each file
        for idx, alias in sorted(lines_dict.items(), key=itemgetter(0)):
            print ('Line number- %s; alias - %s' %(idx+1,alias))
            print lines[idx]

    print ('Should be fixed- %s joins' %count_to_fix )
    pass


def findSProcByFile():


    with open(procList,'r') as f:
        tables = f.read().splitlines()
    #tables = tuple(open(tableList, 'r'))
    print tables
    return
    for f in files_to_process:
        for table in tables:
            content = open(f,'r').read();
            #if ('procedure' in content) and (table in content):
            if (table in content):
                print "in %s exists  %s" %(f, table ) ;
        pass
    pass

def split_sql_statements(statement_string):
    line_comment = r'(?:--|#).*$'
    block_comment = r'/\*[\S\s]*?\*/'
    singe_quote_string = r"'(?:\\.|[^'\\])*'"
    double_quote_string = r'"(?:\\.|[^"\\])*"'
    go_word = r'^[^\S\n]*(?P<GO>GO)[^\S\n]*\d*[^\S\n]*(?:(?:--|#).*)?$'

    full_pattern = re.compile(r'|'.join((
        line_comment,
        block_comment,
        #singe_quote_string,
        #double_quote_string,
        go_word,
    )), re.IGNORECASE | re.MULTILINE)

    last_end = 0
    for match in full_pattern.finditer(statement_string):
        if match.group('GO'):
            yield statement_string[last_end:match.start()]
            last_end = match.end()
    yield statement_string[last_end:]

def split_comment():
    for f in files_to_process:
        print f
    #lines_dict.clear()
    with open(f, 'r') as f:
        lines = f.read().splitlines()
    for idx,line in enumerate(lines):
        #print line
        for statement in split_sql_statements(line):
            #print '======='
            print statement
    pass


if __name__ == '__main__':

    if process_files_from_dir:
        files_to_process[:] = []
        get_files_to_process(dir,ext);


    #split_comment()

    #findSps()

    findSpsByFile();

    #findSProcByFile()
    # for f in files_to_process:
    #     print f;