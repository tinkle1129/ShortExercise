#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class DiffCommands():
    def __init__(self,filepath):
        self.cmd = []
        try:
            f_handle = open(filepath,'r')
            content = f_handle.readlines()

            for line in content:
                line = line.strip('\n')

                if line.strip() == '': # empty sentence
                    raise DiffCommandsError

                if len(''.join(line.split()))!=len(line): # empty space
                    raise DiffCommandsError

                if len(re.findall('[^acd0-9,]',line))>0: # wrong input
                    raise DiffCommandsError

                if 'd' in line: # wrong input
                    idx = line.index('d')
                    if len(line[idx+1:].split(','))>1:
                        raise DiffCommandsError

                if 'a' in line: # wrong input
                    idx = line.index('a')
                    if len(line[:idx].split(','))>1:
                        raise DiffCommandsError
                self.cmd.append(line)
            f_handle.close()

            if self.__check_logic()==False:
                raise DiffCommandsError

        except DiffCommandsError:
            print(__name__ + '.' + DiffCommandsError.__name__ + ': ' + 'Cannot possibly be the commands for the diff of two files')

    def __check_logic(self):
        l_pos = 0;r_pos = 0
        for line in self.cmd:
            if 'd' in line:
                idx = line.index('d')
                l_start = int(line[0:idx].split(',')[0])
                l_end = int(line[0:idx].split(',')[-1])
                r_start = int(line[idx + 1:])
                if (l_start - l_pos) != (r_start + 1 - r_pos):
                    return False
                l_pos = l_end + 1
                r_pos = r_start + 1
            elif 'c' in line:
                idx = line.index('c')
                l_start = int(line[0:idx].split(',')[0])
                l_end = int(line[0:idx].split(',')[-1])
                r_start = int(line[idx + 1:].split(',')[0])
                r_end = int(line[idx + 1:].split(',')[-1])
                if (r_start - r_pos) != (l_start - l_pos):
                    return False
                if (r_start - r_pos) == 0:
                    return False
                l_pos = l_end + 1
                r_pos = r_end + 1
            elif 'a' in line:
                idx = line.index('a')
                l_start = int(line[0:idx].split(',')[0])
                r_start = int(line[idx+1:].split(',')[0])
                r_end = int(line[idx + 1:].split(',')[-1])
                if (l_start-l_pos) != (r_start-1-r_pos):
                    return False
                r_pos = r_end+1
                l_pos = l_start + 1
        return True

    def __str__(self):
        return '\n'.join(self.cmd)

class DiffCommandsError(Exception):
    def __init__(self):
        pass

class OriginalNewFiles():
    def __init__(self, file_1, file_2):
        def getcontents(fp):
            ret = []
            f_handle = open(fp,'r')
            content = f_handle.readlines()
            for line in content:
                line = line.strip('\n')
                ret.append(line)
            return ret
        self.out = []
        self._private={}
        self.all_formats=[]
        self.x = getcontents(file_1)
        self.y = getcontents(file_2)
        self.get_all_diff_commands()

    def Compute_LCS(self):
        xlength = len(self.x)
        ylength = len(self.y)
        self.direction_list = [None] * xlength
        for i in range(xlength):
            self.direction_list[i] = [None] * ylength
        self.lcslength_list = [None] * (xlength + 1)
        for j in range(xlength + 1):
            self.lcslength_list[j] = [None] * (ylength + 1)
        for i in range(0, xlength + 1):
            self.lcslength_list[i][0] = 0
        for j in range(0, ylength + 1):
            self.lcslength_list[0][j] = 0
        for i in range(1, xlength + 1):
            for j in range(1, ylength + 1):
                if self.x[i - 1] == self.y[j - 1]:
                    self.lcslength_list[i][j] = self.lcslength_list[i - 1][j - 1] + 1
                    self.direction_list[i - 1][j - 1] = 0  # left or up
                elif self.lcslength_list[i - 1][j] > self.lcslength_list[i][j - 1]:
                    self.lcslength_list[i][j] = self.lcslength_list[i - 1][j]
                    self.direction_list[i - 1][j - 1] = 1  # up
                elif self.lcslength_list[i - 1][j] < self.lcslength_list[i][j - 1]:
                    self.lcslength_list[i][j] = self.lcslength_list[i][j - 1]
                    self.direction_list[i - 1][j - 1] = -1  # left
                else:
                    self.lcslength_list[i][j] = self.lcslength_list[i - 1][j]
                    self.direction_list[i - 1][j - 1] = 2  # left or up
        self.lcslength = self.lcslength_list[-1][-1]
        return self.direction_list, self.lcslength_list

    def returnLCS(self):
        self.getCandidateList(0,0, 0,[],[])
        self.out = list(set(self.out))

    def getCandidateList(self,curlen,i,j,sx,sy):
        if i>=len(self.direction_list) or j>=len(self.direction_list[0]):
            return

        for idx in range(i,len(self.direction_list)):
            for idj in range(j,len(self.direction_list[0])):
                if self.direction_list[idx][idj]==0:
                    sx.append(str(idx+1))
                    sy.append(str(idj+1))
                    curlen +=1
                    if curlen==self.lcslength:
                        self.out.append(','.join(sx)+'|'+','.join(sy))
                    else:
                        self.getCandidateList(curlen, idx+1, idj+1, sx, sy)
                    sx.pop()
                    sy.pop()
                    curlen -=1

    def get_all_diff_commands(self):
        def getformat(l_pos,r_pos,l_stack,r_stack,fm):
            if len(l_stack) or len(r_stack):
                if len(r_stack) == 0:  # operate d
                    if len(l_stack) > 1:
                        fm += str(l_stack[0]) + ',' + str(l_stack[-1]) + 'd' + str(r_pos - 1) + '\n'
                    else:
                        fm += str(l_stack[0]) + 'd' + str(r_pos - 1) + '\n'
                    l_point = l_pos
                    r_point = r_pos

                elif len(l_stack) == 0:  # operate a
                    if len(r_stack) > 1:
                        fm += str(l_pos - 1) + 'a' + str(r_stack[0]) + ',' + str(r_stack[-1]) + '\n'
                    else:
                        fm += str(l_pos - 1) + 'a' + str(r_stack[0]) + '\n'
                    l_point = l_pos
                    r_point = r_pos
                else:
                    if len(l_stack) > 1:
                        fm += str(l_stack[0]) + ',' + str(l_stack[-1]) + 'c'
                    else:
                        fm += str(l_stack[0]) + 'c'
                    if len(r_stack) > 1:
                        fm += str(r_stack[0]) + ',' + str(r_stack[-1]) + '\n'
                    else:
                        fm += str(r_stack[0]) + '\n'
                    l_point = l_pos
                    r_point = r_pos

            else:
                l_point = l_pos
                r_point = r_pos
            return l_point,r_point,fm

        self.Compute_LCS()
        self.returnLCS()
        top_right = len(self.y)
        top_left = len(self.x)
        for item in set(self.out):
            left = item.split('|')[0]
            right = item.split('|')[1]
            left = list(map(lambda x:int(x),left.split(',')))
            right = list(map(lambda x:int(x),right.split(',')))
            l_point = 0;r_point = 0;l_stack = [];r_stack = [];fm = ''
            for l_pos,r_pos in zip(left,right):
                if l_pos>l_point+1:
                    l_point +=1
                    while(l_point<l_pos):
                        l_stack.append(l_point)
                        l_point+=1
                if r_pos>r_point+1:
                    r_point +=1
                    while(r_point<r_pos):
                        r_stack.append(r_point)
                        r_point+=1
                l_point,r_point,fm = getformat(l_pos,r_pos,l_stack,r_stack,fm)
                l_stack=[]
                r_stack=[]
            while(l_point<top_left):
                l_point +=1
                l_stack.append(l_point)
            while(r_point<top_right):
                r_point +=1
                r_stack.append(r_point)

            if len(l_stack) or len(r_stack):
                if len(l_stack)==0:
                    if len(r_stack) > 1:
                        fm += str(l_point) + 'a' + str(r_stack[0]) + ',' + str(r_stack[-1]) + '\n'
                    else:
                        fm += str(l_point) + 'a' + str(r_stack[0]) + '\n'
                if len(r_stack)==0:
                    if len(l_stack)>1:
                        fm += str(l_stack[0]) + ',' + str(l_stack[-1]) + 'd'+str(r_point)+'\n'
                    else:
                        fm += str(l_stack[0]) + 'd' + str(r_point) + '\n'
            #fm = fm.strip('\n')
            if fm not in self.all_formats:
                self.all_formats.append(fm)
            self._private.setdefault(fm, [])
            self._private[fm].append([left,right])
        self.all_formats.sort()

        ret = []
        for line in self.all_formats:
            ret.append(line.strip('\n'))
        return ret

    def is_a_possible_diff(self,diffobj):
        vertify = '\n'.join(diffobj.cmd)+'\n'
        for fm in self.all_formats:
            if vertify == fm:
                return True
        return False

    def output_diff(self, diffobj):
        commands = diffobj.cmd
        out_str = ''
        for cmd in commands:
            out_str+=cmd+'\n'
            if 'd' in cmd:
                idx = cmd.index('d')
                for i in cmd[:idx].split(','):
                    out_str+='< '+self.x[int(i)-1]+'\n'
            if 'a' in cmd:
                idx = cmd.index('a')
                for i in cmd[idx+1:].split(','):
                    out_str += '> ' + self.y[int(i)-1] + '\n'
            if 'c' in cmd:
                idx = cmd.index('c')
                ls =int(cmd[:idx].split(',')[0])
                le = int(cmd[:idx].split(',')[-1])
                rs = int(cmd[idx+1:].split(',')[0])
                re = int(cmd[idx + 1:].split(',')[-1])
                for i in range(ls,le+1):
                    out_str += '< ' + self.x[int(i)-1] + '\n'
                out_str +='---\n'
                for i in range(rs,re+1):
                    out_str += '> ' + self.y[int(i)-1] + '\n'
        print(out_str.strip('\n'))

    def output_unmodified_from_original(self, diffobj):
        out_str = ''
        vertify = '\n'.join(diffobj.cmd)+'\n'
        for fm in self.all_formats:
            if vertify == fm:
                left = self._private[fm][0][0]
        pre_idx = 0
        for idx in left:
            if idx - pre_idx > 1:
                out_str += '...\n'

            if idx <= len(self.x):
                out_str += self.x[idx - 1]+'\n'
            pre_idx = idx

        if pre_idx<len(self.x):
            out_str += '...\n'

        print (out_str.strip('\n'))

    def output_unmodified_from_new(self, diffobj):
        out_str = ''
        vertify = '\n'.join(diffobj.cmd)+'\n'
        for fm in self.all_formats:
            if vertify == fm:
                right = self._private[fm][0][1]
        pre_idx = 0
        for idx in right:
            if idx - pre_idx > 1:
                out_str += '...\n'
            if idx <= len(self.y):
                out_str += self.y[idx - 1]+'\n'
            pre_idx = idx
        if pre_idx<len(self.y):
            out_str += '...\n'
        print (out_str.strip('\n'))