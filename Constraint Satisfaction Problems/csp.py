#All rights reserved
#Authors - Praveen Alam & Muthukumar Suresh

import copy

global nodes_expanded
nodes_expanded = 0
best_output_course = []
best_output_ta = []
best_cost = -99999
best_capacity = -99999


def convertTime(time):
    timeList = time.split(" ")
    hoursMin = timeList[0].split(":")
    hours = hoursMin[0]
    min = hoursMin[1]
    if len(timeList) > 1:
        if timeList[1] == "PM":
            hours = int(hours) + 12
    return int(str(hours) + str(min))


# finds if there is a clash in the timings in any 2 lists (any 2 times) general function does not handle next day switch
def addTime(time, extra):
    minutes = time % 100
    minutes = minutes + extra
    hours = int(time / 100)
    hours = hours + int(minutes / 60)
    minutes = minutes % 60
    minutes = str(minutes)
    minutes = minutes.zfill(2)
    # print (hours)
    # print(minutes)
    # print (int(str(hours)+minutes))
    return int(str(hours) + minutes)


def time_clash(list1, duration1, list2, duration2):
    for i in range(0, len(list1), 2):
        start1 = list1[i + 1]
        end1 = addTime(list1[i + 1], duration1)
        for j in range(0, len(list2), 2):
            start2 = list2[j + 1]
            end2 = addTime(list2[j + 1], duration2)
            if list1[i] == list2[j]:
                if (start2 < end1 and start2 >= start1) or (start1 < end2 and start1 >= start2):
                    return True
    return False


def backTracking(taDict, coursesDict, check):
    assignment = {}
    for course in coursesDict.keys():
        coursesDict[course]['assignedTAs'] = []
        if coursesDict[course]['students'] < 25:
            taAssignment = 0.0
            coursesDict[course]['taNeed'] = 0
        elif coursesDict[course]['students'] < 40:
            taAssignment = 0.5
            coursesDict[course]['taNeed'] = 0.5
        elif coursesDict[course]['students'] < 60:
            taAssignment = 1.5
            coursesDict[course]['taNeed'] = 1.5
        else:
            taAssignment = 2
            coursesDict[course]['taNeed'] = 2
    for ta in taDict.keys():
        taDict[ta]['tutoring'] = []
        taDict[ta]['tacap'] = 1
    if backtrack_recursive(coursesDict, taDict, check):
        #print(coursesDict)
        #print(taDict)
        print("Assignment complete")

    print("Assignment Complete")
def backtrack_recursive(courseDict, taDict, check):
    global nodes_expanded
    global best_cost
    global best_output_course
    global best_output_ta
    global best_capacity
    nodes_expanded += 1
    cost = 0
    tot_capacity = 0
    # check if course-ta assignment is complete
    if isTaComplete(courseDict) or isTAListExhausted(taDict):
        outputstr = "\n"
        for course in courseDict.keys():
            #print(str(course)+" " +str(courseDict[course]['assignedTAs']))
            outputstr += "\n"
            outputstr += course
            outputstr +="--->"
            TAtupleList = courseDict[course]['assignedTAs']
            if len(TAtupleList) != 0:
                print
                cost = cost + 1
            for tatuple in TAtupleList:
                (taname, capacity) = tatuple
                tot_capacity += capacity
                outputstr += "  --  "
                outputstr += str(taname)
                outputstr += '~Capacity:'
                outputstr += str(capacity)

                #print(outputstr)
            outputstr += '  --  NOT ASSIGNED : '
            outputstr += str(courseDict[course]['taNeed'])
        if (cost > best_cost):
            # print(cost)
            # print(outputstr)
            best_output_course = outputstr
        if (cost == best_cost):
            if best_capacity<tot_capacity:
                best_output_course = outputstr
        outputstr = "\n"
        for ta in taDict:
            outputstr += ta
            outputstr +="--->"
            courseTupleList = taDict[ta]['tutoring']
            for courseTuple in courseTupleList:
                (course, capacity) = courseTuple
                outputstr += '  --  '
                outputstr += str(course)
                outputstr += '~Capacity:'
                outputstr += str(capacity)
            outputstr += "\n"
                #print(outputstr)
        if (cost > best_cost):
            best_cost = cost
            best_output_ta = outputstr
        if (cost == best_cost):
            if best_capacity<tot_capacity:
                best_capacity = tot_capacity
                best_output_ta = outputstr
        #return True
    else:
        if (check == 2 or check == 4 ) and not forward_check(courseDict, taDict):
            return False
        if (check == 3 or check == 4 ) and not constraint_propagation(courseDict, taDict):
            return False
        for course in courseDict.keys():
            #check for TAs who still have some ta capacity
            ta = findBestFitTA(course, courseDict, taDict)
            if not ta:
                return False
            #try full assignment of ta
            if courseDict[course]['taNeed'] >= 1.0 and taDict[ta]['tacap'] >= 1.0:
                courseTAneed = courseDict[course]['taNeed']
                taCapacity = taDict[ta]['tacap']
                #course needs a TA, assign  TA in full
                courseDict[course]['assignedTAs'].append((ta, 1.0))
                courseDict[course]['taNeed'] -= 1.0
                makeTAbusy(course, courseDict, ta, taDict)
                taDict[ta]['tutoring'].append((course, 1.0))
                taDict[ta]['tacap'] -= 1.0
                if backtrack_recursive(courseDict, taDict, check):
                    #assignment was successful exit
                    return True
                else:
                    #since assignment failed, reset the course needs.and free the TA
                    courseDict[course]['assignedTAs'].remove((ta, 1.0))
                    courseDict[course]['taNeed'] = courseTAneed
                    makeTAFree(course, courseDict, ta, taDict)
                    taDict[ta]['tutoring'].remove((course, 1.0))
                    taDict[ta]['tacap'] = taCapacity

            #try Half assignment
            if courseDict[course]['taNeed'] >= 0.5 and taDict[ta]['tacap'] >= 0.5:
                courseTAneed = courseDict[course]['taNeed']
                taCapacity = taDict[ta]['tacap']
                #course needs a TA, assign  TA in full
                courseDict[course]['assignedTAs'].append((ta, 0.5))
                courseDict[course]['taNeed'] -= 0.5
                makeTAbusy(course, courseDict, ta, taDict)
                taDict[ta]['tutoring'].append((course, 0.5))
                taDict[ta]['tacap'] -= 0.5
                if backtrack_recursive(courseDict, taDict, check):
                    #assignment was successful exit
                    return True
                else:
                    #since assignment failed, reset the course needs.and free the TA
                    courseDict[course]['assignedTAs'].remove((ta, 0.5))
                    courseDict[course]['taNeed'] = courseTAneed
                    makeTAFree(course, courseDict, ta, taDict)
                    taDict[ta]['tutoring'].remove((course, 0.5))
                    taDict[ta]['tacap'] = taCapacity

            #Check if TA assignement was successful, even half TA is fine
            if courseDict[course]['taNeed'] > 0.0:
                #no ta was assigned
                # print(course)
                # print(" Could not assign a TA")
                return False


def isTAListExhausted(taDict):
    for ta in taDict.keys():
        if taDict[ta]['tacap'] > 0.0:
            return False
    return True


def findBestFitTA(course, courseDict, taDict):
    bestFit = None
    bestmatchedSkills = 0
    neededSkills = courseDict[course]['skills']
    for ta in taDict.keys():
        if taDict[ta]['tacap'] < 0.5:
            # TA is has is full
            continue
        if courseDict[course]['attendClass']:
            if time_clash(taDict[ta]['classTime'], 90, courseDict[course]['classTime'], 90):
                # TA is not available during class
                continue
        # check if the TA is available during recitation
        if 'recitationTime' in courseDict[course].keys() and time_clash(taDict[ta]['classTime'], 80,
                                                                        courseDict[course]['recitationTime'], 80):
            continue
        matchedSkills = skillMatch(neededSkills, taDict[ta]['skills'])
        if matchedSkills > bestmatchedSkills:
            bestFit = ta
            bestmatchedSkills = matchedSkills
    if float(bestmatchedSkills) / len(neededSkills) >= 0.3:
        return bestFit
    else:
        return None


def findPossibleTAs(course, courseDict, taDict):
    possibleTAs = []
    neededSkills = courseDict[course]['skills']
    for ta in taDict.keys():
        if taDict[ta]['tacap'] < 0.5:
            # TA is  is full
            continue
        if courseDict[course]['attendClass']:
            if time_clash(taDict[ta]['classTime'], 90, courseDict[course]['classTime'], 90):
                # TA is not available during class
                continue
        # check if the TA is available during recitation
        if 'recitationTime' in courseDict[course].keys() and time_clash(taDict[ta]['classTime'], 80,
                                                                        courseDict[course]['recitationTime'], 80):
            continue
        matchedSkills = skillMatch(neededSkills, taDict[ta]['skills'])
        if float(matchedSkills) / len(neededSkills) >= 0.3:
            possibleTAs.append(ta)
    return possibleTAs


def skillMatch(needed, present):
    matched = 0
    for skill in needed:
        if skill in present:
            matched += 1
    return matched


def makeTAbusy(course, courseDict, ta, taDict):
    # add recitation schedule
    if 'recitationTime' in courseDict[course].keys():
        taDict[ta]['classTime'] += courseDict[course]['recitationTime']
    if courseDict[course]['attendClass']:
        #TA need to attend class
        taDict[ta]['classTime'] += courseDict[course]['classTime']


def makeTAFree(course, courseDict, ta, taDict):
    # print("before "+str(taDict[ta]['classTime']))
    if 'recitationTime' in courseDict[course].keys():
        for i in range(0, len(courseDict[course]['recitationTime']), 2):
            day = courseDict[course]['recitationTime'][i]
            time = courseDict[course]['recitationTime'][i + 1]
            for j in range(0, len(taDict[ta]['classTime']), 2):
                ta_day = taDict[ta]['classTime'][j]
                ta_time = taDict[ta]['classTime'][j + 1]
                if day == ta_day and time == ta_time:
                    taDict[ta]['classTime'].pop(j)
                    taDict[ta]['classTime'].pop(j)
                    break
    if courseDict[course]['attendClass']:
        for i in range(0, len(courseDict[course]['classTime']), 2):
            day = courseDict[course]['classTime'][i]
            time = courseDict[course]['classTime'][i + 1]
            for j in range(0, len(taDict[ta]['classTime']), 2):
                ta_day = taDict[ta]['classTime'][j]
                ta_time = taDict[ta]['classTime'][j + 1]
                if day == ta_day and time == ta_time:
                    taDict[ta]['classTime'].pop(j)
                    taDict[ta]['classTime'].pop(j)
                    break
                    #print("End "+str(taDict[ta]['classTime']))


def isTaComplete(courseDict):
    for course in courseDict.keys():
        if not courseDict[course]['taNeed'] <= 0.5:
            return False
    return True


def forward_check(courseDict, taDict):
    # print('Entered forward check')
    # check if there is any course that can not get a TA
    for course in courseDict.keys():
        #print(courseDict[course])
        if courseDict[course]['taNeed'] > 0.0:
            #course needs a Ta
            ta = findBestFitTA(course, courseDict, taDict)
            if not ta:
                return False
    return True


def constraint_propagation(courseDict, taDict):
    # print("Entered Constraint propagation")
    courseTAs = []
    for course in courseDict.keys():
        if courseDict[course]['taNeed'] > 0:
            courseTAs.append(findPossibleTAs(course, courseDict, taDict))

    oneMorePass = True
    while oneMorePass:
        oneMorePass = False
        for list1 in courseTAs:
            if not list1:
                return False
            for list2 in courseTAs:
                if not list2:
                    return False
                if list1 != list2:
                    # check for each element in list1, there is a possibility in list2
                    for x in list1:
                        #there should be someone
                        remain_ta = [y for y in list2 if y != x]
                        if not remain_ta:
                            #remove from list
                            list.remove(x)
                            oneMorePass = True
    return True

    # test printing keys.

    #prune_constraints(assignment, taDict, coursesDict)
    #for key in assignment.keys():
    #print(key,':',assignment[key])


def main():
    courses = {}
    ta = {}
    f = open('testdata.txt')
    line = f.readline()
    while line != '':
        while (line != '\n' ):
            line = line.rstrip()
            # print(line)
            courseList = line.split(', ')
            # print(courseList)
            for i in range(2, len(courseList), 2):
                courseList[i] = convertTime(courseList[i])
            courses[courseList[0]] = {}
            courses[courseList[0]]['classTime'] = courseList[1:]
            # print( courseList[1:])
            line = f.readline()

        line = f.readline()
        while (line != '\n'):
            line = line.rstrip()
            courseList = line.split(', ')
            for i in range(2, len(courseList), 2):
                courseList[i] = convertTime(courseList[i])

            courses[courseList[0]]['recitationTime'] = courseList[1:]
            line = f.readline()
        line = f.readline()
        while (line != '\n'):
            line = line.rstrip()
            courseList = line.split(', ')

            courses[courseList[0]]['students'] = int(courseList[1])
            if courseList[2] == 'yes':
                courses[courseList[0]]['attendClass'] = True
            else:
                courses[courseList[0]]['attendClass'] = False
            line = f.readline()
        line = f.readline()
        while (line != '\n'):
            line = line.rstrip()
            courseList = line.split(', ')

            courses[courseList[0]]['skills'] = courseList[1:]
            line = f.readline()

        line = f.readline()
        while (line != '\n' ):
            line = line.rstrip()
            taList = line.split(', ')
            for i in range(2, len(taList), 2):
                taList[i] = convertTime(taList[i])
            ta[taList[0]] = {}
            ta[taList[0]]['classTime'] = taList[1:]

            line = f.readline()

        line = f.readline()
        while (line != '\n' and line != ''):
            line = line.rstrip()
            taList = line.split(', ')

            ta[taList[0]]['skills'] = taList[1:]
            line = f.readline()

    check = input(
        "(BT - Back tracking, FC - Forward Checking CS - Constraint Satisfaction\n : 1 - BT \n2 - BT + FC \n3 - BT + CS \n4 - BT + FC + CS. \n Enter your option: 1, 2, 3, 4.\n >>")
    # for course in courses.keys():
    # print(course,":",courses[course])
    # for tas in ta.keys():
    #         print(tas,":",ta[tas])

    backTracking(ta, courses, check)
    print("Course Requirements:\n")
    for course in courses.keys():
        if courses[course]['students'] < 25:
            print(course,"0")
        elif courses[course]['students'] < 40:
            print(course,"0.5")
        elif courses[course]['students'] < 60:
            print(course,"1.5")
        else:
            print(course,"2")

    print("COURSE Assignment:", best_output_course)
    print("TA Assignment:", best_output_ta)
    print("NODES EXPANDED:\n", nodes_expanded)

if __name__ == "__main__":
    main()