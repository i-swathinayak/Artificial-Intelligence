import numpy as numpy
import time


class Applicant:
    def __init__(self, a_info):
        self.id = a_info[0:5]
        self.gender = a_info[5]
        self.age = int(a_info[6:9])
        if (a_info[9] == 'Y'):
            self.pet = True
        else:
            self.pet = False

        if (a_info[10] == 'Y'):
            self.med = True
        else:
            self.med = False

        if (a_info[11] == 'Y'):
            self.car = True
        else:
            self.car = False

        if (a_info[12] == 'Y'):
            self.lic = True
        else:
            self.lic = False

        self.days = a_info[13:20]
        self.type = self.sendpType()
        self.Available_Spaces = self.sendResCount()

    def getGender(self):
        if (self.gender == 'F'):
            return 1
        return 0

    def sendpType(self):
        if (self.car and self.lic and not (self.med) and self.age > 17 and self.gender == 'F' and not (self.pet)):
            return 'P'
        if (self.car and self.lic and not (self.med)):
            return 'SP'
        if (self.age > 17 and self.gender == 'F' and not (self.pet)):
            return 'LP'
        return 'N'

    def checkLHSA(self):
        if (self.type == 'L'):
            return True
        return False

    def checkSPLA(self):
        if (self.type == 'S'):
            return True
        return False

    def checkType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def sendResCount(self):
        sum = 0
        for i in self.days:
            sum += int(i)
        return sum

    def sendDays(self):
        res = []
        for i in self.days:
            res.append(int(i))
        return res

    def checkInfo(self):
        print(self.id)
        print(self.gender)
        print(self.age)
        print(self.pet)
        print(self.med)
        print(self.car)
        print(self.lic)
        print(self.type)
        print(self.days + '\n')

    def checkAge(self):
        return self.id

    def checkId(self):
        return self.id


class Available_Spaces:
    def __init__(self, b, p):
        self.b = b
        self.p = p
        self.bed = [b, b, b, b, b, b, b];
        self.parking = [p, p, p, p, p, p, p];

    def sumRes(self, Applicant, type):
        if (type == "SPLA"):
            list = Applicant.sendDays();
            for i in range(7):
                self.parking[i] = self.parking[i] + list[i]
            return self.parking
        if (type == "LHSA"):
            list = Applicant.sendDays();
            for i in range(7):
                self.bed[i] = self.bed[i] + list[i]
            return self.bed

    def add(self, resource, type):
        res = []
        if (type == "LHSA"):
            for i in range(7):
                res[i] = self.bed[i] + resource.bed
        else:
            for i in range(7):
                res[i] = self.parking[i] + resource.parking
        return res

    def removeLFinal(self, list):
        for i in range(7):
            self.bed[i] = self.bed[i] - list[i]

    def removeSFinal(self, list):
        for i in range(7):
            self.parking[i] = self.parking[i] - list[i]

    def isNegative(self, list):
        for i in range(7):
            if (list[i] < 0):
                return False
        return True

    def removeSelected(self, list, type):
        res = []
        if (type == "SPLA"):
            for i in range(7):
                res.append(self.parking[i] - list[i])
        else:
            if (type == "LHSA"):
                for i in range(7):
                    res.append(self.bed[i] - list[i])
        return res

    def sum(self, type):
        sum = 0
        if (type == "LHSA"):
            for i in range(7):
                sum = sum + int(self.bed[i])
        else:
            for i in range(7):
                sum = sum + int(self.parking[i])
        return sum

    def better(self, resource, type):
        sumS = self.sum(type)
        sumR = resource.sum(type)

        if (sumS > sumR):
            return "true"
        if (sumS < sumR):
            return "false"
        if (sumS == sumR):
            return "equal"


# check space for applicant
def compute_space(generic_c, req):
    temp = [] * 7
    count, flag = 0, 0
    for i in req:
        temp.append(generic_c[count] - int(i))
        if temp[count] == -1:
            flag = 1;
            break;
        count += 1

    if (flag == 1):
        return -1
    else:
        generic_c[:] = list(temp)
        return 0


def return_max_key(s_list):
    n = int(s_list[1])
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


class BestTemp:
    sp_counter = []
    la_counter = []

    def __init__(self, bothSL, onlyS, onlyL, b_list, p_list):
        self.bothSL = bothSL
        self.onlyS = onlyS
        self.onlyL = onlyL
        self.spla_list = self.generateList(onlyS)
        self.lahsa_list = self.generateList(onlyL)
        self.spla_lahsa_list = self.generateList(bothSL)
        self.sp_counter = p_list
        self.la_counter = b_list

    def generateList(self, lis):
        res = []
        for x in lis:
            res.append([x.checkId(), x.days])
        return res

    def greed(self, spla_list, lahsa_list, spla_lahsa_list):
        # sort
        spla_list.sort(key=return_max_key, reverse=True)
        lahsa_list.sort(key=return_max_key, reverse=True)
        spla_lahsa_list.sort(key=return_max_key, reverse=True)

        spla_selected_apps = []
        lahsa_chosen_appl = []

        applicable = 1
        for i in range(len(spla_lahsa_list)):
            if (i % 2 == 0):
                if (compute_space(self.sp_counter, str(spla_lahsa_list[i][1])) != -1):
                    spla_selected_apps.append(spla_lahsa_list[i][0])
                else:

                    applicable = 0
                    break
            else:
                if (compute_space(self.la_counter, str(spla_lahsa_list[i][1])) != -1):
                    lahsa_chosen_appl.append(spla_lahsa_list[i][0])
                else:

                    applicable = 0
                    break

        if (applicable):
            for i in range(len(spla_list)):
                if (compute_space(self.sp_counter, str(spla_list[i][1])) != -1):
                    spla_selected_apps.append(spla_list[i][0])
                else:
                    applicable = 0
                    break

        if (applicable):
            for i in range(len(lahsa_list)):
                if (compute_space(self.la_counter, str(lahsa_list[i][1])) != -1):
                    spla_selected_apps.append(lahsa_list[i][0])
                else:

                    applicable = 0
                    break
        # selection time
        if not spla_lahsa_list and not spla_list:
            return "00000"
        elif not spla_lahsa_list:
            return spla_list[0][0]
        else:
            return spla_lahsa_list[0][0]

        # if (applicable):
        # file.close()
        # exit()


start_timer = time.time()


def check_timer():
    time_period = 176
    if time.time() > start_timer + time_period:
        return True
    return False


def sendoutput(printValue):
    sendoutput = open('output.txt', 'w')
    sendoutput.sendoutput(printValue)
    sendoutput.close()


def getEligibleApps(ApplicantList):
    eligCan = []
    for x in ApplicantList:
        if (x.checkType() == 'P'):
            eligCan.append(x)
    return eligCan


def getEligibleSortedApplicants(ApplicantList, param):
    eligCan = []
    for x in ApplicantList:
        if (x.checkType() == param):
            eligCan.append(x)
    return sortonSpaces(eligCan)


def popTypes(list, cType, ApplicantList):
    for x in range(len(list)):
        ApplicantList[int(list[x]) - 1].setType(cType)


def is_Valid(resType, resource, Applicant, type):
    check = resType.isNegative(resource.removeSelected(resType.sumRes(Applicant, type), type))
    if (check == False):
        resType.bed = resType.removeSelected(Applicant.sendDays(), type)
        return check
    else:
        return check


def is_App_Valid(resource, Applicant, type):
    return resource.isNegative(resource.removeSelected(Applicant.sendDays(), type))


def sortonSpace_Gender(eligCan):
    return sorted(eligCan, key=lambda Applicant: (Applicant.getGender(), Applicant.Available_Spaces), reverse=True)


def sortonSpaces(list):
    return sorted(list, key=lambda Applicant: Applicant.Available_Spaces, reverse=True)


def sendReqSpaces(resType, resource, list, type):
    res = []
    for x in list:
        if resType.isNegative(resource.removeSelected(resType.sumRes(x, type), type)):
            res.append(x)
        else:
            resType.removeSelected(x.sendDays(), type)
    return res


def val_ls(lis, Applicant):
    for i in range(len(lis)):
        if (lis[i].checkId() == Applicant.checkId()):
            return False
    return True


def return_val(rC, rCount, type):
    if (type == "SPLA"):
        if (rCount.p == 0):
            rCount.p = rC.p
            rCount.b = rC.b
        if (rC.p > rCount.p):
            rCount.p = rC.p
            rCount.b = rC.b
    else:
        if (rCount.b == 0):
            rCount.b = rC.b
            rCount.p = rC.p
        if (rC.b > rCount.b):
            rCount.b = rC.b
            rCount.p = rC.p


def lahsa_Traverse(lhsaRes, splaRes, l, lList, resource, ApplicantList, maxRes, rCount):
    if check_timer():
        return
    if (len(lList) == l):
        if (rCount.b < lhsaRes.sum("LHSA")):
            rCount.p = splaRes.sum("SPLA")
            rCount.b = lhsaRes.sum("LHSA")

        r = lhsaRes.better(maxRes, "LHSA")
        if r == "equal" or r == "true":
            for i in range(7):
                maxRes.bed[i] = lhsaRes.bed[i]
        return

    for i in range(l, len(lList)):
        if (is_Valid(lhsaRes, resource, lList[i], "LHSA")):
            lahsa_Traverse(lhsaRes, splaRes, i + 1, lList, resource, ApplicantList, maxRes, rCount)
            lhsaRes.bed = lhsaRes.removeSelected(lList[i].sendDays(), "LHSA")


def spla_Traverse(lhsaRes, splaRes, s, sList, resource, ApplicantList, maxRes, rCount):
    if check_timer():
        return
    if (len(sList) == s):
        if (rCount.p < splaRes.sum("SPLA")):
            rCount.p = splaRes.sum("SPLA")
            rCount.b = lhsaRes.sum("LHSA")

        r = splaRes.better(maxRes, "SPLA")
        if r == "equal" or r == "true":
            for i in range(7):
                maxRes.parking[i] = splaRes.parking[i]
        return

    for i in range(s, len(sList)):
        if (is_Valid(splaRes, resource, sList[i], "SPLA")):
            spla_Traverse(lhsaRes, splaRes, i + 1, sList, resource, ApplicantList, maxRes, rCount)
            splaRes.parking = splaRes.removeSelected(sList[i].sendDays(), "SPLA")


def get_All_Valid_Apps(fullList, lis):
    return [x for x in fullList if x not in lis]


def exhaustive_Search(splaRes, lhsaRes, s, l, sList, lList, resource, ApplicantList, maxRes, sLis, lLis, turn, rCount):
    if check_timer():
        return
    if (turn):
        # SPLA
        res = get_All_Valid_Apps(get_All_Valid_Apps(sList, lLis), sLis)
        eff_flag = True
        for i in range(len(res)):
            if is_Valid(splaRes, resource, res[i], "SPLA"):
                eff_flag = False
                sLis.append(res[i])
                rC = Available_Spaces(0, 0)
                exhaustive_Search(splaRes, lhsaRes, s, l, sList, lList, resource, ApplicantList, maxRes, sLis, lLis,
                                  not turn, rC)
                return_val(rC, rCount, "SPLA")
                sLis.remove(res[i])
                splaRes.parking = splaRes.removeSelected(res[i].sendDays(), "SPLA")
        if (eff_flag):
            lahsa_Traverse(lhsaRes, splaRes, 0, get_All_Valid_Apps(get_All_Valid_Apps(lList, lLis), sLis), resource,
                           ApplicantList, maxRes, rCount)
        return

    if (not turn):
        # LHSA
        res = get_All_Valid_Apps(get_All_Valid_Apps(lList, sLis), lLis)
        eff_flag = True
        for i in range(len(res)):
            if is_Valid(lhsaRes, resource, res[i], "LHSA"):
                eff_flag = False
                lLis.append(res[i])
                rC = Available_Spaces(0, 0)
                exhaustive_Search(splaRes, lhsaRes, s, l, sList, lList, resource, ApplicantList, maxRes, sLis, lLis,
                                  not turn, rC)
                return_val(rC, rCount, "LHSA")
                lLis.remove(res[i])
                lhsaRes.bed = lhsaRes.removeSelected(res[i].sendDays(), "LHSA")
        if (eff_flag):
            spla_Traverse(lhsaRes, splaRes, 0, get_All_Valid_Apps(get_All_Valid_Apps(sList, sLis), lLis), resource,
                          ApplicantList, maxRes, rCount)
        return


def start_search(resource, ApplicantList, check):
    eligCan = getEligibleApps(ApplicantList)
    eligCan = sortonSpace_Gender(eligCan)

    spla_eligible_candidates = getEligibleSortedApplicants(ApplicantList, "SP")
    lahsa_eligible_candidates = getEligibleSortedApplicants(ApplicantList, "LP")

    BestTempo = BestTemp(eligCan, spla_eligible_candidates, lahsa_eligible_candidates, list(resource.bed),
                        list(resource.parking))
    BestTempAns = BestTempo.greed(BestTempo.spla_list, BestTempo.lahsa_list, BestTempo.spla_lahsa_list)

    sList = eligCan + spla_eligible_candidates
    sList = sortonSpaces(sList)
    lList = eligCan + lahsa_eligible_candidates
    lList = sortonSpaces(lList)

    maxRes = Available_Spaces(0, 0)
    resMax = Available_Spaces(0, 0)
    maxApplicant = Applicant(str(BestTempAns) + "O000YYNN0000000")
    for i in range(len(sList)):
        splaRes = Available_Spaces(0, 0)
        lhsaRes = Available_Spaces(0, 0)
        if (is_Valid(splaRes, resource, sList[i], "SPLA")):
            res = Available_Spaces(0, 0)
            rCount = Available_Spaces(0, 0)
            sLis = []
            lLis = []
            sLis.append(sList[i])
            turn = False
            exhaustive_Search(splaRes, lhsaRes, i + 1, 0, sList, lList, resource, ApplicantList, res, sLis, lLis, turn,
                              rCount)
            if (rCount.p == resMax.p):
                if (rCount.b == resMax.b):
                    if (maxApplicant.Available_Spaces == sList[i].Available_Spaces):
                        if (int(maxApplicant.checkId()) > int(sList[i].checkId())):
                            maxApplicant = sList[i]
                    if (maxApplicant.Available_Spaces < sList[i].Available_Spaces):
                        maxApplicant = sList[i]
                if (rCount.b > resMax.b):
                    maxApplicant = sList[i]
                    resMax.b = rCount.b
            if (rCount.p > resMax.p):
                maxApplicant = sList[i]
                resMax.p = rCount.p
                resMax.b = rCount.b
            splaRes.parking = splaRes.removeSelected(sList[i].sendDays(), "SPLA")
        if check_timer():
            return maxApplicant
    return maxApplicant


if __name__ == '__main__':
    read = open('input.txt', 'r')
    sendoutput = open('output.txt', 'w')
    prinValue = ""

    b = int(read.readline())
    p = int(read.readline())
    resource = Available_Spaces(b, p)

    L = int(read.readline())
    lhsaList = []
    for i in range(L):
        lhsaList.append(str(read.readline()))

    S = int(read.readline())
    splaList = []
    for i in range(S):
        splaList.append(str(read.readline()))

    A = int(read.readline())
    ApplicantList = []
    for i in range(A):
        ApplicantList.append(Applicant(read.readline()))

    check = False
    if A <= p:
        check = True

    popTypes(lhsaList, 'L', ApplicantList)
    popTypes(splaList, 'S', ApplicantList)

    for i in splaList:
        resource.removeSFinal(ApplicantList[int(i) - 1].sendDays())

    for i in lhsaList:
        resource.removeLFinal(ApplicantList[int(i) - 1].sendDays())

    prinValue = start_search(resource, ApplicantList, check).checkId()
    print(prinValue)
    read.close()
