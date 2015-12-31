

def basic():
    import war_sim
    my_sim = war_sim.Simulation(1, 2, False, 3)
    my_sim.run_simulation()

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("basic()", setup="from __main__ import basic", number=10000))

