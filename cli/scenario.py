import myEnv as me

if __name__ == '__main__':
    NUMOFQUEUE = 5
    env = me.MyEnv()
    classes = ['a']

    for i in classes:
        env.newClass(i)
    gens = []
    for i in classes:
        gens.append(env.MGenerater('g'+i, 5, i))
    qs = []
    for i in range(NUMOFQUEUE):
        qs.append(env.MPQueue('q%d' % i, 3))
    for i in qs:
        for j in classes:
            i.assignClass(j)
    for i in gens:
        i.nextQueue = qs[0]
    j = 1
    for i in qs[0:NUMOFQUEUE-1]:
        i.nextQueue = qs[j]
        j += 1
    # env.run(100000)
    for i in range(1000):
        env.run(1000*(i+1))
        print()
        print('======== %d times ========' % ((i+1)*1000))
        for i in range(NUMOFQUEUE):
            qs[i].printResult()
        env.printResult()
