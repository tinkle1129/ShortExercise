
from diff import *

DiffCommands('wrong_1.txt')
DiffCommands('wrong_2.txt')
DiffCommands('wrong_3.txt')
DiffCommands('wrong_4.txt')
DiffCommands('wrong_5.txt')
DiffCommands('wrong_6.txt')
DiffCommands('wrong_7.txt')

diff_1 = DiffCommands('diff_1.txt')
print diff_1
print '========'


diff_2 = DiffCommands('diff_2.txt')
print diff_2
print '========'

diff_3 = DiffCommands('diff_3.txt')
print diff_3

print '========'
pair_of_files = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
print '========'

print pair_of_files.is_a_possible_diff(diff_1)
print '========'

print pair_of_files.is_a_possible_diff(diff_2)
print '========'

print pair_of_files.is_a_possible_diff(diff_3)
print '========'

pair_of_files.output_diff(diff_1)
print '========'

pair_of_files.output_unmodified_from_original(diff_1)
print '========'

pair_of_files.output_unmodified_from_new(diff_1)
print '========'

diffs = pair_of_files.get_all_diff_commands()
print '========'

print(len(diffs))
print '========'

print(diffs[0])
print '========'

pair_of_files = OriginalNewFiles('file_1_2.txt', 'file_1_1.txt')
print '========'

diffs = pair_of_files.get_all_diff_commands()
print '========'

print len(diffs)
print '========'

print diffs[0]
print '========'


pair_of_files = OriginalNewFiles('file_1_1.txt', 'file_1_1.txt')
print '========'

diffs = pair_of_files.get_all_diff_commands()
print '========'

print len(diffs)
print '========'

print diffs[0]
print '========'

pair_of_files = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')
print '========'

print pair_of_files.is_a_possible_diff(diff_1)
print '========'

print pair_of_files.is_a_possible_diff(diff_2)
print '========'

print pair_of_files.is_a_possible_diff(diff_3)
print '========'

pair_of_files.output_diff(diff_2)
print '======'
pair_of_files.output_unmodified_from_original(diff_2)
print '========'

pair_of_files.output_unmodified_from_new(diff_2)
print '========'

diffs = pair_of_files.get_all_diff_commands()
print '========'

print(len(diffs))
print '========'

print(diffs[0])
print '========'

print(diffs[1])
print '========'

pair_of_files = OriginalNewFiles('file_2_2.txt', 'file_2_1.txt')
print '========'

diffs = pair_of_files.get_all_diff_commands()
print '========'

print len(diffs)
print '========'

print diffs[0]
print '========'

print diffs[1]
print '========'

pair_of_files = OriginalNewFiles('file_3_1.txt', 'file_3_2.txt')
print '========'

print pair_of_files.is_a_possible_diff(diff_1)
print '========'

print pair_of_files.is_a_possible_diff(diff_2)
print '========'

print pair_of_files.is_a_possible_diff(diff_3)
print '========'

pair_of_files.output_diff(diff_3)
print '========'

pair_of_files.output_unmodified_from_original(diff_3)
print '========'

pair_of_files.output_unmodified_from_new(diff_3)
print '========'

diffs = pair_of_files.get_all_diff_commands()
print '========'

print(len(diffs))
print '========'

print(diffs[0])
print '========'

print(diffs[1])
print '========'

print(diffs[2])
print '========'

pair_of_files = OriginalNewFiles('file_3_2.txt', 'file_3_1.txt')
print '========'

diffs = pair_of_files.get_all_diff_commands()
print '========'

print len(diffs)
print '========'

print diffs[0]
print '========'

print(diffs[1])
print '========'

print(diffs[2])
print '========'
