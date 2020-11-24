from axovision import backtesting
import ray

from my_company import data_loader

data = data_loader()

ray.init()

cluster = BacktestingCluster(max_cpus=100, max_gpus=0)
# backtest

cluster.get_jupyter() # returns the link

session = backtest.connect(cluster)
backtest.run_on(session).
backtest.execute(data, command)
