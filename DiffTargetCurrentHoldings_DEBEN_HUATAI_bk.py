# -*- coding: cp936 -*-
'''
version: 6
�����˵�url��ȡ�ڻ�ʵʱ�۸񣬰��ս��׽��Ӵ�С���У���֤���Ƚ��׽���ĺ�Լ
yqi, 29, Feb, 2016
'''

from xml.dom import minidom
import time
import pdb
import os
import re
import urllib2

def XmlParse(file_xml):
    dom = minidom.parse(file_xml)
    path_target = dom.getElementsByTagName('target')[0].childNodes[0].nodeValue + time.strftime('%Y%m%d')
    path_current = dom.getElementsByTagName('current')[0].childNodes[0].nodeValue
    path_grouplist = dom.getElementsByTagName('grouplist')[0].childNodes[0].nodeValue
    path_Abandonlist = dom.getElementsByTagName('abandonlist')[0].childNodes[0].nodeValue
    path_specialist = dom.getElementsByTagName('specialist')[0].childNodes[0].nodeValue
    return path_target, path_current, path_grouplist, path_specialist

def ChooseTarget(path_target):
    file_list = []
    nGroup = 0
    all_list = os.listdir(path_target)
    for mlist in all_list:
        if mlist.startswith('LAST_HOLDING'):
            filedir = os.path.join(path_target, mlist)
            if os.path.isfile(filedir):
                file_list.append(mlist)
                tmp_num = int(mlist.split('_')[2])
                if tmp_num > nGroup:
                    nGroup = tmp_num
    file_list_group = []
    for i in range(nGroup):
        file_list_group.append([])  
    for mlist in file_list:
        tmp_num = int(mlist.split('_')[2])
        file_list_group[tmp_num - 1].append(mlist)
    print '�ļ�����Ӧ������£�\n'

    i = 1
    for mgroup in file_list_group:
        for mfile in mgroup:
            print '--->>> %d : %s' %(i, mfile)
            i += 1
        print '\n'
    num_file = i
    
    choice_list = []
    print 'Ĭ��ѡ���ļ����£�ȷ���밴\'y\'�����س��� �Լ������밴\'n\'�����س���'
    for mgroup in file_list_group:
        if mgroup:
            print '%s\n' %mgroup[-1]
            choice_list.append(mgroup[-1])   
    while True:
        sInput = raw_input()
        if 'y' == sInput:
            return choice_list
        elif 'n' == sInput:
            choice_list = []
            print '�������ļ���Ӧ��ţ�����ļ��ö��Ÿ�������\'�س���\'������롣\n'
            while True:
                num_input = raw_input()
                num_list = num_input.split(',')
                if len(set(num_list)) != len(num_list):
                    print '������Ų����ظ�������������'
                else:
                    for mnum in num_list:
                                if mnum.isdigit():
                                    num = int(mnum)
                                    if num <= num_file and num >= 1:
                                        print '%s: %s \n' %(u'ѡ�����ļ�',file_list[num-1])
                                        choice_list.append(file_list[num-1])
                                    else:
                                        print '���������������� 1 �� %d ֮������֣���������ö��Ÿ���' %num_file
                                else:
                                    print '���������������� 1 �� %d ֮������֣���������ö��Ÿ���' %num_file
                    if len(choice_list) == len(num_list):
                        return choice_list
                    else:
                        print '���������������� 1 �� %d ֮������֣���������ö��Ÿ���' %num_file
        else:
            print '�밴 \'y\' �� \'n\'�� ���س���'
                
def TargetParse(path_target, file_targets):
    tHolding = []
    tInstrument = []

    for file_target in file_targets:
        mfile = os.path.join(path_target, file_target)
        rfid = open(mfile, 'r')
        try:
            lines = rfid.readlines()
            for line in lines:
                words = line.split(' ')
                for word in words:
                    if word:
                        try:
                            tmp_quality = int(word[:-1])
                        except Exception,e:
                            tmp_instrument = word
                try:
                    p_tInstrument = tInstrument.index(tmp_instrument)
                    tHolding[p_tInstrument] += tmp_quality
                except Exception,e:
                    tInstrument.append(tmp_instrument)
                    tHolding.append(tmp_quality)
        except Exception, e:
            print '--->>> ���ļ� %s ʧ�ܣ���رճ���'
        finally:
            rfid.close()

    return tInstrument, tHolding

def CurrentParse(file_current):
    cHolding = []
    cInstrument = []

    rfid = open(file_current, 'r')
    try:
        lines = rfid.readlines()
        for line in lines[1:]:
            if line:
                words = line.split('\t')
                try:
                    p = cInstrument.index(words[3])
                    cHolding[p][0] = 1 if words[5] == '����' else -1             # �ղ�Ϊ-1�����Ϊ1
                    if words[6] == '��':                                       # ���
                        cHolding[p][1] = int(words[8]) + cHolding[p][1]
                    elif words[6] == '��':                                     # ���
                        cHolding[p][2] = int(words[8]) + cHolding[p][2]
                except Exception,e:
                    cInstrument.append(words[3])
                    tmp = [0] * 3
                    tmp[0] = 1 if words[5] == '����' else -1             # �ղ�Ϊ-1�����Ϊ1
                    tmp[1] = int(words[8]) if words[6] == '��' else 0  # ���
                    tmp[2] = int(words[8]) if words[6] == '��' else 0  # ���
                    cHolding.append(tmp)
            else:
                continue

        return cInstrument, cHolding

    except Exception, e:
        print e
    finally:
        rfid.close()
        
##        
##def Abandon(file_Abandonlist):
##    AbInst = []
##    rfid = open(file_Abandonlist, 'r')
##    try:        
##        lines = rfid.readlines()
##        if lines == []:
##            print 'AbandonlistΪ��'
##            AbInst = []
##        else:            
##            for line in lines:
##                if line :
##                    words = line.strip('\n').upper()
##                    AbInst.append(filter(str.isalpha, words))
##    except Exception, e:
##            print '--->>> ��Abdonlist�ļ�ʧ�ܣ���رճ���'
##    finally:
##            rfid.close()
##    return AbInst

    
def special(file_specialist):
    SpecialInst = []
    rfid = open(file_specialist, 'r')
    try:        
        lines = rfid.readlines()
        if lines == []:
##            print 'file_specialistΪ��'
            SpecialInst = []
        else:            
            for line in lines:
                if line :
                    words = line.strip('\n').upper()
                    SpecialInst.append(filter(str.isalpha, words))
    except Exception, e:
            print '--->>> ��Specialist�ļ�ʧ�ܣ���رճ���'
    finally:
            rfid.close()
    return SpecialInst  
    

def GroupParse(file_group):
    Inst = []
    Unit = []

    rfid = open(file_group[0], 'r')
    try:
        lines = rfid.readlines()
        for line in lines:
            if line:
                Inst.append(line[0:-1])
    except Exception, e:
        print e
    finally:
        rfid.close()
    
    rfid = open(file_group[1], 'r')
    try:
        lines = rfid.readlines()
        for line in lines:
            if line:
                tmp = re.match('\d+\s+\d+', line)
                strTmp = tmp.group()
                if strTmp:
                    strSplit = strTmp.split(' ')
                    Unit.append(float((strSplit[-1])))
    except Exception,e:
        print e
    finally:
        rfid.close()
    
    return Inst, Unit

def DiffTargetCurrent(tInstrument, tHolding, cInstrument, cHolding, Inst, Unit):
    Diff = []
    for ti in tInstrument:
        tmpDiff = [0] * 7
##        if (filter(str.isalpha, ti).upper()) in (Abandon(file_Abandonlist)):
##            #print ti
##            continue
##        else:
        try:
            pt = tInstrument.index(ti)
            pc = cInstrument.index(ti)
            diff = tHolding[pt] - cHolding[pc][0] * (cHolding[pc][1] + cHolding[pc][2])
            tmpDiff[0] = abs(diff)
            # ���
            if cHolding[pc][0] > 0 and (filter(str.isalpha, ti).upper()) in (special(file_specialist)):

                if diff > 0:
                        tmpDiff[2] += diff
                elif diff < 0:
                    if cHolding[pc][1] > 0:
                        tmpDiff[1] = abs(diff) #���н�֣�ֱ�ӿ���
                    else:
                        tmpDiff[4] = cHolding[pc][2] #��ƽ���
                        tmpDiff[1] = abs(diff) - cHolding[pc][2]#ʣ�µĿ���
                                    
            elif cHolding[pc][0] > 0:
                if diff > 0:
                    tmpDiff[2] += diff
                elif diff < 0:
                    if abs(diff) <= cHolding[pc][2]: #ƽ���
                        tmpDiff[4] = abs(diff)
                    elif abs(diff) > cHolding[pc][2] and abs(diff) <= cHolding[pc][1] + cHolding[pc][2]:
                        tmpDiff[4] = cHolding[pc][2]#��ƽ���
                        tmpDiff[6] = abs(diff) - cHolding[pc][2]#��ƽ���
                    elif abs(diff) > cHolding[pc][1] + cHolding[pc][2]:
                        tmpDiff[4] = cHolding[pc][2]
                        tmpDiff[6] = cHolding[pc][1]
                        tmpDiff[1] = abs(diff) - cHolding[pc][1] - cHolding[pc][2]#ʣ�µĿ���
                    
            # �ղ�
            elif cHolding[pc][0] < 0 and (filter(str.isalpha, ti).upper()) in (special(file_specialist)):
                if diff < 0:
                    tmpDiff[1] = abs(diff)
                elif diff > 0:
                    if cHolding[pc][1] > 0: #���н�֣�ֱ�ӿ���
                        tmpDiff[2] = abs(diff)
                    else:
                        tmpDiff[3] = cHolding[pc][2]  #��ƽ���
                        tmpDiff[2] = abs(diff) - cHolding[pc][2] #ʣ�µĿ���

                
            elif cHolding[pc][0] < 0:
                if diff < 0:
                    tmpDiff[1] = abs(diff)
                elif diff > 0:
                    if diff <= cHolding[pc][2]:
                        tmpDiff[3] = diff
                    elif diff > cHolding[pc][2] and diff <= cHolding[pc][1] + cHolding[pc][2]:
                        tmpDiff[3] = cHolding[pc][2]
                        tmpDiff[5] = diff - cHolding[pc][2]
                    elif diff > cHolding[pc][1] + cHolding[pc][2]:
                        tmpDiff[3] = cHolding[pc][2]
                        tmpDiff[5] = cHolding[pc][1]
                        tmpDiff[2] = diff - cHolding[pc][1] - cHolding[pc][2]

                            
        except Exception,e:
                if tHolding[pt] > 0:
                        tmpDiff[0] = tHolding[pt]
                        tmpDiff[2] = tHolding[pt]
                elif tHolding[pt] < 0:
                        tmpDiff[0] = abs(tHolding[pt])
                        tmpDiff[1] = abs(tHolding[pt])
        tmpDiff.append(ti)
    Diff.append(tmpDiff)
        
    for ci in cInstrument:
        tmpDiff = [0] * 7
        if ci[0:2] == 'IC' or ci[0:2] == 'IF' or ci[0:2] == 'IH':
##        or (filter(str.isalpha, ci).upper()) in Abandon(file_Abandonlist):
            continue
        else:
            try:
                pt = tInstrument.index(ci)
            except Exception, e:
                pc = cInstrument.index(ci)
                if cHolding[pc][0] > 0:
                    tmpDiff[0] = cHolding[pc][0]
                    tmpDiff[4] = cHolding[pc][2]
                    tmpDiff[6] = cHolding[pc][1]
                elif cHolding[pc][0] < 0:
                    tmpDiff[0] = abs(cHolding[pc][0])
                    tmpDiff[3] = cHolding[pc][2]
                    tmpDiff[5] = cHolding[pc][1]
        tmpDiff.append(ci)
        Diff.append(tmpDiff)
    # �ҳ�Diff�е�group��Ȼ���Ҷ�Ӧ�ĳ�����Ȼ������ܽ��׶Ȼ��Խ��׶��������
    for iDiff in range(0,len(Diff)):
        #get price
        Contract = Diff[iDiff][-1].upper()
        iContract = int(re.search('\d+', Contract).group())
        sContract = re.search('\D+', Contract).group()
        if iContract < 1000:
            iContract += 1000
            Contract = sContract + str(iContract)
        url = r'http://hq.sinajs.cn/list=' + Contract
        
        Data = urllib2.urlopen(url)
        strData = Data.readlines()
        splitStr = strData[0].split(',')
        price = float(splitStr[8])
        if not price:
            print e
            print '--->>> Error, when get price from WEB.'
            return
        
        tmpDiff = []
        tmp = re.match('\D+', Diff[iDiff][-1])
        if tmp:
            mInst = tmp.group()
            try:
                pInst = Inst.index(mInst)
                lots = sum(Diff[iDiff][1:-1])
                money = lots * Unit[pInst] * price / 10000
                Diff[iDiff].insert(0, money)
            except Exception,e:
                print e
                print '--->>> Error, when find the group information'
                return
    
    Diff.sort(reverse=True)
    arrow = '--->>>'
    for idiff in Diff:
        flag = True
        if idiff:
            if idiff[0] != 0:
                if idiff[4] != 0:
                    if flag:
                        print '%s\t%10.4f��\t%8s' %(arrow, idiff[0], idiff[-1]),
                        flag = False
                    print ',\tƽ��� %3d ��' %idiff[4],                           
                if idiff[5] != 0:
                    if flag:
                        print '%s\t%10.4f��\t%8s' %( arrow, idiff[0], idiff[-1]),
                        flag = False
                    print ',\tƽ��� %3d ��' %idiff[5],
                if idiff[6] != 0:
                    if flag:
                        print '%s\t%10.4f��\t%8s' %(arrow, idiff[0], idiff[-1]),
                        flag = False
                    print ',\tƽ��� %3d ��' %idiff[6],
                if idiff[7] != 0:
                    if flag:
                        print '%s\t%10.4f��\t%8s' %(arrow, idiff[0], idiff[-1]),
                        flag = False
                    print ',\tƽ��� %3d ��' %idiff[7],
                if idiff[2] != 0:
                    if flag:
                        print '%s\t%10.4f��\t%8s' %(arrow, idiff[0], idiff[-1]),
                        flag = False
                    print ',\t  ���� %3d ��' %idiff[2],
                if idiff[3] != 0:
                    if flag:
                        print '%s\t%10.4f��\t%8s' %(arrow, idiff[0], idiff[-1]),
                        flag = False
                    print ',\t  ���� %3d ��' %idiff[3],
                
                print ''
                
if __name__ == '__main__':
    file_config = r'.\config.xml'
    path_target, path_current, path_grouplist, path_specialist = XmlParse(file_config)

    str_date = time.strftime('%Y%m%d')
    file_target = ChooseTarget(path_target)
    file_current = path_current + str_date + '\\IF_Holdings_tmp.txt'
    file_group = [path_grouplist + 'group.list', path_grouplist + 'group2.list']
##    file_Abandonlist = path_Abandonlist + 'Abandonlist.txt'
    file_specialist = path_specialist + 'specialist.txt'
    
    tInstrument, tHolding = TargetParse(path_target, file_target)
    cInstrument, cHolding = CurrentParse(file_current)
    Inst, Unit = GroupParse(file_group);
    
    DiffTargetCurrent(tInstrument,tHolding, cInstrument, cHolding, Inst, Unit)

    print '\n\n--->>> ��\'�س���\'�˳�����.'
    y = raw_input()
