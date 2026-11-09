import pandas as pd

def load(filePath: str, leadTime: int, dateStart: str) -> pd.DataFrame:
	df = pd.read_csv(filePath)
	
	df["TransactionDT"] = parse_datetime(df["TransactionDate"], df["TransactionTime"])
	df["EntryDT"] = parse_datetime(df["EntryDate"], df["EntryTime"])
	df.dropna(subset=["TransactionDT", "EntryDT"], inplace=True)
	
	df["LeadTime_hrs"] = (df["EntryDT"] - df["TransactionDT"]).dt.total_seconds() / 3600
	filtered = df[df["LeadTime_hrs"] >= leadTime].copy()
	
	filtered["Hour"] = filtered["TransactionDT"].dt.hour
	filtered["Month"] = filtered["TransactionDT"].dt.to_period("M").astype(str)
	filtered["DayOfWeek"] = filtered["TransactionDT"].dt.day_name()
	
	start_timestamp = pd.Timestamp(dateStart)
	filtered = filtered[filtered["TransactionDT"] > start_timestamp]
	
	return filtered

def parse_datetime(date_int: pd.Series, time_int: pd.Series) -> pd.Series:
	"""Combine YYYYMMDD + HHMM integer columns into a single datetime Series."""
	date_str = date_int.astype(str).str.zfill(8)
	time_str = time_int.astype(str).str.zfill(4)
	return pd.to_datetime(date_str + time_str, format="%Y%m%d%H%M", errors="coerce")