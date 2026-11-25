import pandas as pd


class ValidationLogger:

    def __init__(self, key_column):
        self.key_column = key_column
        self.reject_tracker = {}

    def log(self, df_errors, reason):

        if df_errors.empty:
            return

        if self.key_column not in df_errors.columns:
            raise ValueError(
                f"Key column "
                f"'{self.key_column}' "
                f"not found."
            )

        for index, row in df_errors.iterrows():
            key = row[self.key_column]

            # Handle missing PKs
            if pd.isna(key):
                key = f"ROW_{index}"

            if key not in self.reject_tracker:
                record = row.to_dict()
                record["RejectReasons"] = set()
                self.reject_tracker[key] = record

            self.reject_tracker[key]["RejectReasons"].add(reason)

    def get_rejects(self):

        if not self.reject_tracker:
            return pd.DataFrame()

        rejects = pd.DataFrame( self.reject_tracker.values() )

        rejects["RejectReason"] = ( rejects["RejectReasons"].apply(
                lambda reasons:
                "; ".join(sorted(reasons))
            )
        )

        rejects.drop(
            columns=["RejectReasons"],
            inplace=True
        )

        return rejects

    def reject_count(self):
        return len(self.reject_tracker)

    def get_rejected_keys(self):
        return set(
            self.reject_tracker.keys()
        )