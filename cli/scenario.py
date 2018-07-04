import myEnv as me

if __name__ == '__main__':
    env = me.MyEnv()

    env.newClass('a')
    env.newClass('b')
    env.newClass('c')

    ga = env.MGenerater('ga', 100, 'a')
    gb = env.MGenerater('gb', 100, 'b')
    gc = env.MGenerater('gc', 100, 'c')
    sor1 = env.GFQueue('sor1', 1, 4)
    q1 = env.GFQueue('q1', 10)
    sor2 = env.GFQueue('sor2', 1, 4)
    q2 = env.GFQueue('q2', 10)

    sor1.assignClass('a')
    sor1.assignClass('b')
    sor1.assignClass('c')
    q1.assignClass('a')
    q1.assignClass('b')
    sor2.assignClass('a')
    sor2.assignClass('b')
    sor2.assignClass('c')
    q2.assignClass('a')
    q2.assignClass('c')

    ga.nextQueue = sor1
    gb.nextQueue = sor1
    gc.nextQueue = sor1
    sor1.nextQueue = q1
    q1.nextQueue = sor2
    sor2.nextQueue = q2

    env.run(100000000)

    print('')
    sor1.printResult()
    q1.printResult()
    sor2.printResult()
    q2.printResult()
    env.printResult()
