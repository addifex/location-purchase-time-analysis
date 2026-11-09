import argparse
import os
import matplotlib.pyplot as plt
import seaborn as sns
import get_data
from constants import DOW_ORDER, HOUR_ORDER

def main():
	arg_parser = argparse.ArgumentParser("Generates heatmaps for locations for analyzing the distribution of when customers purchase.")
	
	arg_parser.add_argument("--filePath", type=str, help="Path to csv file")
	arg_parser.add_argument("--leadTime", default=0, type=int, help="Filter by time from entry")
	arg_parser.add_argument("--dateStart", default="0001-01-01", type=str, help="Only transactions after start time")
	arg_parser.add_argument("--outputDir", default="output", type=str, help="The output directory")
	
	args = arg_parser.parse_args()
	
	os.makedirs(args.outputDir, exist_ok=True)
	
	data = get_data.load(args.filePath, args.leadTime, args.dateStart)
	
	month_order = sorted(data["Month"].unique())
	locations = sorted(data["Location"].dropna().unique())
	
	for loc in locations:
		loc_dow = data[data["Location"] == loc]
		loc_mon = data[data["Location"] == loc]
		
		if loc_dow.empty:
			continue
		
		dow_counts = (
			loc_dow.groupby(["Hour", "DayOfWeek"])
			.size()
			.unstack(fill_value=0)
			.reindex(index=HOUR_ORDER, columns=DOW_ORDER, fill_value=0)
		)
		dow_total = dow_counts.values.sum()
		dow_pct = (dow_counts / dow_total * 100) if dow_total else dow_counts.astype(float)
		
		mon_counts = (
			loc_mon.groupby(["Hour", "Month"])
			.size()
			.unstack(fill_value=0)
			.reindex(index=HOUR_ORDER, columns=month_order, fill_value=0)
		)
		mon_total = mon_counts.values.sum()
		mon_pct = (mon_counts / mon_total * 100) if mon_total else mon_counts.astype(float)
		
		fig, (ax1, ax2) = plt.subplots(
			1, 2,
			figsize=(8 + len(month_order) * 0.6, 9),
			gridspec_kw={"width_ratios": [7, max(7, len(month_order))]},
		)
		
		sns.heatmap(
			dow_pct, ax=ax1, cmap="YlOrRd", annot=True, fmt=".1f",
			linewidths=0.3, cbar_kws={"label": "% of purchases"},
		)
		ax1.set_title(f"{loc} — Purchases by Hour × Day of Week")
		ax1.set_xlabel("Day of Week")
		ax1.set_ylabel("Hour of Day")
		ax1.tick_params(axis="x", rotation=30)
		ax1.tick_params(axis="y", rotation=0)
		
		sns.heatmap(
			mon_pct, ax=ax2, cmap="YlOrRd", annot=True, fmt=".1f",
			linewidths=0.3, cbar_kws={"label": "% of purchases"},
		)
		ax2.set_title(
			f"{loc} — Purchases by Hour × Month"
		)
		ax2.set_xlabel("Month")
		ax2.set_ylabel("Hour of Day")
		ax2.tick_params(axis="x", rotation=30)
		ax2.tick_params(axis="y", rotation=0)
		
		fig.suptitle(
			f"{loc}  —  purchases made ≥ {args.leadTime}h before entry (n={dow_total:,})",
			fontsize=13, y=1.00,
		)
		plt.tight_layout()
		safe = loc.replace(" ", "_").replace("/", "_")
		out_path = os.path.join(args.outputDir, f"{safe}.png")
		plt.savefig(out_path, dpi=130, bbox_inches="tight")
		plt.close(fig)
		print(f"  ✓ {out_path}")
	
	print("\nDone.")

if __name__ == "__main__":
	main()