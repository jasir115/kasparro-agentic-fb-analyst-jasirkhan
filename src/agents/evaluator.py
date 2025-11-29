import numpy as np
import pandas as pd
from scipy import stats

class Evaluator:
    def __init__(self, cfg):
        self.cfg = cfg
        self.min_conf = float(cfg.get("min_confidence", 0.6))

    def validate_hypotheses(self, hypotheses, df):
        """
        For each hypothesis, run suggested checks and attach quantitative evidence.
        Returns enriched hypotheses.
        """
        results = []
        for i,h in enumerate(hypotheses):
            evidence = {}
            checks = h.get("suggested_checks", [])
            # run common checks
            if "compare_roas_by_campaign" in checks or "compare_roas" in checks:
                ev = self._compare_periods(df, metric="roas")
                evidence["roas_period_compare"] = ev
            if "compare_ctr" in checks or "ctr_by_creative" in checks:
                ev = self._compare_periods(df, metric="ctr")
                evidence["ctr_period_compare"] = ev
            if "ctr_by_creative" in checks:
                if "creative_type" in df.columns:
                    grp = df.groupby("creative_type")["ctr"].mean().sort_values(ascending=False).to_dict()
                    evidence["ctr_by_creative_type"] = grp
            # compute confidence rule-of-thumb
            conf = h.get("confidence", 0.5)
            # bump confidence if p-values small
            pvals = []
            for k,v in evidence.items():
                if isinstance(v, dict) and "p_value" in v:
                    pvals.append(v["p_value"])
            if pvals and any([p<0.05 for p in pvals]):
                conf = max(conf, 0.75)
            enriched = dict(h)
            enriched["evidence"] = evidence
            enriched["confidence"] = conf
            results.append(enriched)
        return results

    def _compare_periods(self, df, metric="roas"):
        """
        Compare last 7 days vs prior 7 days if date available; else simple two-sample t-test on halves.
        """
        if self.cfg.get("date_col") in df.columns:
            date_col = self.cfg["date_col"]
        else:
            date_col = "date" if "date" in df.columns else None

        if date_col:
            df = df.sort_values(date_col)
            last = df.tail(7)[metric].dropna()
            prior = df.tail(14).head(7)[metric].dropna()
        else:
            # split halves
            n = len(df)
            first = df[metric].dropna().iloc[:n//2]
            second = df[metric].dropna().iloc[n//2:]
            last, prior = second, first
        if len(last) < 2 or len(prior) < 2:
            return {"error":"insufficient_samples", "n_last": len(last), "n_prior": len(prior)}
        tstat, p = stats.ttest_ind(last, prior, equal_var=False, nan_policy="omit")
        return {"mean_last": float(last.mean()), "mean_prior": float(prior.mean()), "diff": float(last.mean()-prior.mean()), "tstat": float(tstat), "p_value": float(p), "n_last": int(len(last)), "n_prior": int(len(prior))}
