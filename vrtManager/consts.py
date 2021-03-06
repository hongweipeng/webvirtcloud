


# 通用常量定义
RUNNING = 'RUNNING'
SUCCESS = 'SUCCESS'
FAIL    = 'FAIL'
HANGUP  = 'HANGUP'
END     = "END"
DESTROY = "DESTROY"
POWER_OFF = "POWER_OFF"


# 状态
TASK_RUNNING = RUNNING # 部署中
TASK_SUCCESS = SUCCESS # 单步骤成功
TASK_FAIL    = FAIL    # 部署失败
TASK_HANGUP  = HANGUP  # 部署挂起
TASK_SCHEDULING = 'SCHEDULING' # 部署前状态
TASK_FINISH  = 'FINISH'  # 部署完成

# 任务状态的选择框
TASK_CHOICE = (
    (HANGUP, HANGUP),
    (TASK_RUNNING, TASK_RUNNING),
    (TASK_SUCCESS, TASK_SUCCESS),
    (TASK_FAIL, TASK_FAIL),
    (TASK_SCHEDULING, TASK_SCHEDULING),
    (TASK_FINISH, TASK_FINISH),
)

HISTORY_STATUS = (
    (SUCCESS, SUCCESS),
    (FAIL, FAIL),
)

CLOCK_CHOICE = (
    ('utc', 'utc'),
    ('localtime', 'localtime'),
)

NETWORK_CHOICE = (
    ('default', 'default'),
    ('bridge', 'bridge'),
)