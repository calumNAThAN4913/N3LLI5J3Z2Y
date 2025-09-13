# 代码生成时间: 2025-09-13 15:03:13
from dash import Dash, dcc, html, Input, Output
from dash.dependencies import ALL
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# 定义定时任务调度器类
class DashboardScheduler():
    def __init__(self):
        # 初始化Dash应用
        self.app = Dash(__name__)
        self.app.layout = html.Div([
            html.H1('定时任务调度器'),
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # 刷新频率为1秒
                n_intervals=0
            ),
            html.Div(id='live-update-text')
        ])

        # 定义定时任务
        self.tasks = {}

        # 初始化调度器
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # 定义回调函数
        @self.app.callback(
            Output('live-update-text', 'children'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_metrics(n):
            # 获取当前时间
            now = datetime.now(pytz.utc).isoformat()
            # 返回当前时间
            return now

    def add_task(self, name, func, trigger, **trigger_args):
        """添加定时任务到调度器。
        :param name: 任务名称
        :param func: 执行的函数
        :param trigger: 触发器类型
        :param trigger_args: 触发器参数
        """
        # 如果任务已存在，则先移除
        if name in self.tasks:
            self.scheduler.remove_job(self.tasks[name])
        # 添加新的任务
        job = self.scheduler.add_job(func, trigger, **trigger_args)
        self.tasks[name] = job

    def run_server(self):
        # 运行Dash服务器
        self.app.run_server(debug=True)

# 实例化调度器
scheduler = DashboardScheduler()

# 添加一个示例任务，每10秒执行一次
def example_task():
    print("执行示例任务")

scheduler.add_task(
    name='example_task',
    func=example_task,
    trigger='interval',
    seconds=10
)

# 运行Dash服务器
scheduler.run_server()