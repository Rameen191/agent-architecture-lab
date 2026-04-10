class PerformanceMetrics:
    """Collection of performance measures for fair agent comparison"""

    @staticmethod
    def average_cost(agent, env):
        """Simple average cost per time step"""
        return agent.spent / env.time if env.time > 0 else 0

    @staticmethod
    def inventory_adjusted_cost(agent, env):
        """Adjust cost by value of remaining inventory"""
        if env.time == 0:
            return 0

        final_stock_value = env.stock * env.price
        return (agent.spent - final_stock_value) / env.time

    @staticmethod
    def holding_cost_metric(agent, env, holding_rate=0.02):
        """Include holding costs for inventory over time"""

        if env.time == 0:
            return 0

        total_holding_cost = 0

        for stock_level in env.stock_history:
            total_holding_cost += stock_level * holding_rate

        return (agent.spent + total_holding_cost) / env.time

    @staticmethod
    def service_level(agent, env):
        """Measure stockout rate (lower is better)"""

        if len(env.stock_history) == 0:
            return 0

        stockouts = sum(1 for stock in env.stock_history if stock < 0)
        return stockouts / len(env.stock_history)

    @staticmethod
    def composite_score(agent, env, weights=None):
        """Weighted combination of metrics"""

        if weights is None:
            weights = {'cost': 0.4, 'inventory': 0.3, 'service': 0.3}

        cost_score = PerformanceMetrics.average_cost(agent, env)
        inventory_score = PerformanceMetrics.inventory_adjusted_cost(agent, env)
        service_score = PerformanceMetrics.service_level(agent, env)

        return (
            weights['cost'] * cost_score +
            weights['inventory'] * abs(inventory_score) +
            weights['service'] * service_score * 1000
        )