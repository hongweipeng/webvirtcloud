import io
import abc
import json
import logging
import traceback
import threading
from taskflow import task, engines
from taskflow.patterns import linear_flow as lf
from django.db import models
from . import consts

def save_history(name, status:str, result:str or dict,
                 model, history_model_cls, history_comment:str) -> None:
    """
    将执行结果保存到history表中
    :param name: 步骤名称
    :param status: 执行的结果状态
    :param result: 执行结果
    :param model: 模型
    :param history_model_cls: 历史模型
    :param history_comment: 字段
    :return:
    """
    kwargs = {
        'name': name,
        'status': status,
        'result': result,
        history_comment: model.id,
    }
    print(kwargs)
    history_model = history_model_cls(**kwargs)
    history_model.save()

def set_next_step(raw_model:models.Model, steps:list, step:str=''):
    """
    当前步骤执行完后，设置step为下一步要执行的步骤
    :param raw_model:
    :param steps:
    :param step:
    :return:
    """
    raw_model.refresh_from_db()
    if step:
        raw_model.step = step
        raw_model.save()
        return raw_model
    current_step = raw_model.step
    steps_len = len(steps)
    for index, task_cls in enumerate(steps):
        if task_cls.__name__ == current_step:
            if steps_len == index + 1: # 已是最后一步
                return raw_model
            raw_model.step = steps[index + 1].__name__
            raw_model.save()
            return raw_model
    else:
        raise Exception('unknown step: %s' % current_step)
        

class TaskBase(task.Task):
    def __init__(self, steps, history_model_cls, history_foreign_key, *args, **kwargs):
        super(TaskBase, self).__init__(*args, **kwargs)
        self.steps = steps
        self.history_model_cls = history_model_cls
        self.history_foreign_key = history_foreign_key
    
    def execute(self, raw_model, *args, **kwargs):
        res = self.do_execute(raw_model)
        save_history(raw_model.step, consts.SUCCESS, res, raw_model, self.history_model_cls, self.history_foreign_key)
        return set_next_step(raw_model, self.steps)
    
    @abc.abstractmethod
    def do_execute(self, raw_model):
        pass

class TaskWorker(threading.Thread):
    def __init__(self, engine, raw_model, history_model_cls, history_comment):
        super(TaskWorker, self).__init__()
        self.engine = engine
        self.raw_model = raw_model
        self.history_model_cls = history_model_cls
        self.history_comment = history_comment
    
    def run(self):
        whole_err_msg = ''
        try:
            self.raw_model.status = consts.RUNNING
            self.raw_model.save()
            self.engine.run()
        except Exception as e:
            with io.StringIO() as err_fp:
                traceback.print_exc(file=err_fp)
                whole_err_msg = err_fp.getvalue()

            save_history(self.raw_model.step, consts.FAIL, whole_err_msg, self.raw_model,
                         self.history_model_cls, self.history_comment)  # 记录历史
            self.raw_model.status = consts.HANGUP
            self.raw_model.save()
            
def build(raw_model, steps:list, history_model_cls, history_comment):
    """
    根据数据库创建
    :return:
    """
    current_step_index = 0
    current_step = raw_model.step
    
    if not current_step:
        current_step = steps[0].__name__
        raw_model.step = current_step
        raw_model.save()
    for index, step_cls in enumerate(steps):
        if step_cls.__name__ == current_step:
            current_step_index = index
            break
    else:
        raise Exception("unknown step:%s" % current_step)
        
    deploy_flow = lf.Flow("webvirt")
    deploy_flow.add(*[x(steps, history_model_cls, history_comment) for x in steps[current_step_index:]])
    eng = engines.load(deploy_flow, store={'raw_model': raw_model})
    return eng

def async_run(eng, game_model, history_model_cls, history_foreign_key):
    """
    异步执行taskflow
    """
    worker = TaskWorker(eng, game_model, history_model_cls, history_foreign_key)
    worker.start()

