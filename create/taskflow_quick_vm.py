from vrtManager import taskflow_base


class ClearIfSet(taskflow_base.TaskBase):
    def do_execute(self, quick_model):
        pass
        
class Step2(taskflow_base.TaskBase):
    def do_execute(self, raw_model):
        pass



class END(taskflow_base.TaskBase):
    def do_execute(self, raw_model):
        return True

STEPS = (
    ClearIfSet,
    Step2,
    END,
)