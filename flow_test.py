import taskflow.engines
from taskflow.patterns import linear_flow as lf
from taskflow import task

def flow_watch(state, details):
    print("Flow State:{}".format(state))
    print("Flow Details:{}".format(details))

class A(task.Task):
    def execute(self, a_msg, *args, **kwargs):
        print('A:{}' . format(a_msg))
        return 'AAA'

class B(task.Task):
    def execute(self, b_msg, *args, **kwargs):
        print('B : {}' . format(b_msg))
        return 'BBB'

flow = lf.Flow('simple-linear-listen').add(
    A(),
    B()
    )

engine = taskflow.engines.load(flow, store = dict(a_msg = 'a', b_msg = 'b'))

engine.notifier.register('*', flow_watch)

engine.run()