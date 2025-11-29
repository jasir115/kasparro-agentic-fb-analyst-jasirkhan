from datetime import datetime, timedelta

class Planner:
    def __init__(self, cfg):
        self.cfg = cfg

    def plan(self, query, summary):
        # Simple rule-based planner: decide windows and checks
        date_col = self.cfg.get("date_col","date")
        # default windows: last 7 days vs prior 7 days
        tasks = [
            {"task":"compute_baseline","params":{"window":"last_7_days"}},
            {"task":"compare_periods","params":{"period1":"last_7_days","period2":"prior_7_days"}},
            {"task":"aggregate_by","params":{"keys":["campaign_id","creative_type"]}},
            {"task":"generate_hypotheses","params":{}},
            {"task":"validate_hypotheses","params":{}},
            {"task":"generate_creatives","params":{}}
        ]
        return tasks
