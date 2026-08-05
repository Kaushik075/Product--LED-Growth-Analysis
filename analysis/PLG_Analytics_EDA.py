import os
import mysql.connector
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. SETUP: OUTPUT FILE
# ==========================================

# Create report file
REPORT_FILE = "PLG_Analytics_Report.txt"

def log_output(message, print_to_console=True):
    if print_to_console:
        print(message)
    
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

# ==========================================
# 2. DATABASE CONNECTION
# ==========================================

def connect_to_mysql():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password=os.environ.get("PLG_MYSQL_PASSWORD", "************"),
    database='********',
    charset='utf8mb4'
)
        log_output("✅ Connected to MySQL successfully!")
        return connection
    except mysql.connector.Error as e:
        log_output(f"❌ Error: {e}")
        return None

# ==========================================
# 3. DATA LOADING
# ==========================================

def load_data(connection):
    """Load all tables from MySQL"""
    log_output("\n📊 Loading data from database...")
    
    queries = {
        'users': 'SELECT * FROM dim_users',
        'events': 'SELECT * FROM fact_user_events',
        'ab_tests': 'SELECT * FROM fact_ab_tests',
        'cohorts': 'SELECT * FROM fact_cohort_data'
    }
    
    dfs = {}
    for name, query in queries.items():
        dfs[name] = pd.read_sql(query, connection)
        log_output(f"✅ Loaded {name}: {len(dfs[name]):,} rows")
    
    return dfs

# ==========================================
# 4. FUNNEL ANALYSIS
# ==========================================

def analyze_funnel(dfs):
    """Analyze conversion funnel"""
    log_output("\n" + "="*70)
    log_output("📊 FUNNEL ANALYSIS")
    log_output("="*70)
    
    events = dfs['events']
    
    # Count users at each stage
    funnel_stages = {
        'Signup': len(dfs['users']),
        'Activation': len(events[events['event_type'] == 'activation']['user_id'].unique()),
        'Feature Use': len(events[events['event_type'] == 'feature_use']['user_id'].unique()),
        'PQL Qualified': len(events[events['event_type'] == 'pql_qualified']['user_id'].unique()),
        'Paid': len(events[events['event_type'] == 'payment_complete']['user_id'].unique())
    }
    
    # Calculate conversions
    log_output("\n🔻 FUNNEL WATERFALL:")
    prev_count = 0
    for stage, count in funnel_stages.items():
        if prev_count == 0:
            prev_count = count
            log_output(f"  {stage}: {count:,} (100.0%)")
        else:
            conversion = (count / prev_count) * 100
            drop_off = 100 - conversion
            log_output(f"  {stage}: {count:,} ({conversion:.1f}%) | Drop-off: {drop_off:.1f}%")
            prev_count = count
    
    overall_conversion = (funnel_stages['Paid'] / funnel_stages['Signup']) * 100
    log_output(f"\n📈 Overall Conversion: {overall_conversion:.2f}%")
    
    return funnel_stages

# ==========================================
# 5. A/B TEST ANALYSIS
# ==========================================

def analyze_ab_tests(dfs):
    """Analyze A/B test results. Returns a dict of results keyed by test_name
    so downstream sections (e.g. recommendations) can report real numbers
    instead of hardcoded ones."""
    log_output("\n" + "="*70)
    log_output("🧪 A/B TEST ANALYSIS")
    log_output("="*70)
    
    ab_tests = dfs['ab_tests']
    results = {}
    
    log_output("\n⚡ LIFT CALCULATIONS:")
    
    for test_name in sorted(ab_tests['test_name'].unique()):
        test_data = ab_tests[ab_tests['test_name'] == test_name]
        
        control = test_data[test_data['variant'].str.contains('control', case=False, na=False)]
        treatment = test_data[~test_data['variant'].str.contains('control', case=False, na=False)]
        
        control_rate = control['converted'].mean()
        treatment_rate = treatment['converted'].mean()
        
        if control_rate > 0:
            lift = ((treatment_rate - control_rate) / control_rate) * 100
            
            log_output(f"\n  📌 {test_name.upper()}:")
            log_output(f"    Control: {control_rate*100:.2f}% ({int(control['converted'].sum())}/{len(control)} conversions)")
            log_output(f"    Treatment: {treatment_rate*100:.2f}% ({int(treatment['converted'].sum())}/{len(treatment)} conversions)")
            log_output(f"    Lift: {lift:+.2f}%")
            
            # Chi-square test
            contingency = pd.crosstab(test_data['variant'], test_data['converted'])
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            is_significant = p_value < 0.05
            significance = "✅ DEPLOY" if is_significant else "❌ NOT SIGNIFICANT"
            log_output(f"    Statistical Significance: {significance} (p={p_value:.4f})")

            results[test_name] = {
                'control_rate': control_rate * 100,
                'treatment_rate': treatment_rate * 100,
                'relative_lift_pct': lift,
                'p_value': p_value,
                'is_significant': is_significant
            }
    
    return results

# ==========================================
# 6. COHORT ANALYSIS
# ==========================================

def analyze_cohorts(dfs):
    """Analyze cohort retention"""
    log_output("\n" + "="*70)
    log_output("📈 COHORT RETENTION ANALYSIS")
    log_output("="*70)
    
    cohorts = dfs['cohorts']
    
    # Retention by cohort week
    cohort_summary = cohorts.groupby('cohort_date').agg({
        'user_id': 'count',
        'activation_date': lambda x: (x.notna()).sum(),
        'feature_adoption_date': lambda x: (x.notna()).sum(),
        'pql_date': lambda x: (x.notna()).sum(),
        'payment_date': lambda x: (x.notna()).sum()
    }).rename(columns={
        'user_id': 'Total',
        'activation_date': 'Activated',
        'feature_adoption_date': 'Feature',
        'pql_date': 'PQL',
        'payment_date': 'Paid'
    })
    
    # Calculate retention %
    for col in ['Activated', 'Feature', 'PQL', 'Paid']:
        cohort_summary[f'{col}%'] = (cohort_summary[col] / cohort_summary['Total'] * 100).round(2)
    
    log_output("\n📊 Cohort Week-over-Week Retention:")
    log_output(f"\n{'Cohort Week':<12} {'Total':<8} {'Act%':<8} {'Feature%':<10} {'PQL%':<8} {'Paid%':<8}")
    log_output("-" * 54)
    
    for cohort_date, row in cohort_summary.iterrows():
        week_label = pd.to_datetime(cohort_date).strftime('%Y-%m-%d')
        log_output(f"{week_label:<12} {int(row['Total']):<8} {row['Activated%']:<8.1f} {row['Feature%']:<10.1f} {row['PQL%']:<8.1f} {row['Paid%']:<8.1f}")
    
    # Stability check
    log_output("\n✅ COHORT STABILITY CHECK:")
    act_range = cohort_summary['Activated%'].max() - cohort_summary['Activated%'].min()
    feat_range = cohort_summary['Feature%'].max() - cohort_summary['Feature%'].min()
    pql_range = cohort_summary['PQL%'].max() - cohort_summary['PQL%'].min()
    paid_range = cohort_summary['Paid%'].max() - cohort_summary['Paid%'].min()
    
    log_output(f"  Activation Range: {act_range:.2f}%")
    log_output(f"  Feature Range: {feat_range:.2f}%")
    log_output(f"  PQL Range: {pql_range:.2f}%")
    log_output(f"  Paid Range: {paid_range:.2f}%")

# ==========================================
# 7. REVENUE ANALYSIS
# ==========================================

def analyze_revenue(dfs):
    """Revenue analysis — reports real, current revenue figures only.
    Does NOT project revenue impact from A/B test lift: fact_ab_tests and
    payment events are not linked at the schema level (test participation
    isn't joined to which users later paid), so a dollar-value projection
    here would be fabricated rather than derived. See README 'Future
    Enhancements' for what a real version of that calculation would need."""
    log_output("\n" + "="*70)
    log_output("💰 REVENUE ANALYSIS")
    log_output("="*70)
    
    events = dfs['events']
    payments = events[events['event_type'] == 'payment_complete']
    
    log_output(f"\n💵 CURRENT STATE:")
    log_output(f"  Total Customers: {len(payments):,}")
    log_output(f"  Total Revenue: ${payments['event_value'].sum():,.2f}")
    log_output(f"  Average ARPU: ${payments['event_value'].mean():.2f}")

# ==========================================
# 8. USER SEGMENTATION
# ==========================================

def analyze_segments(dfs):
    """Analyze by user segment"""
    log_output("\n" + "="*70)
    log_output("👥 USER SEGMENTATION ANALYSIS")
    log_output("="*70)
    
    users = dfs['users']
    events = dfs['events']
    
    paid_users = set(events[events['event_type'] == 'payment_complete']['user_id'].unique())
    
    log_output("\n📊 Conversion by User Segment:")
    log_output(f"\n{'Segment':<15} {'Total':<8} {'Converted':<12} {'Conv%':<8}")
    log_output("-" * 43)
    
    for segment in sorted(users['user_segment'].unique()):
        segment_users = users[users['user_segment'] == segment]
        converted = sum(segment_users['user_id'].isin(paid_users))
        conv_rate = (converted / len(segment_users) * 100) if len(segment_users) > 0 else 0
        
        log_output(f"{segment:<15} {len(segment_users):<8} {converted:<12} {conv_rate:<8.2f}%")

# ==========================================
# 9. MAIN REPORT GENERATION
# ==========================================

def generate_report(connection, dfs):
    """Generate complete EDA report"""
    
    # Clear previous report
    open(REPORT_FILE, 'w', encoding='utf-8').close()
    
    log_output("="*70)
    log_output("🎯 PLG ANALYTICS - COMPLETE EDA REPORT")
    log_output("="*70)
    log_output(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_output(f"Database: plg_analytics")
    log_output("")
    
    # Run all analyses
    analyze_funnel(dfs)
    ab_results = analyze_ab_tests(dfs)
    analyze_cohorts(dfs)
    analyze_revenue(dfs)
    analyze_segments(dfs)
    
    # Recommendations — built from the actual ab_results dict above,
    # not hardcoded. Ranked by relative lift, highest first.
    log_output("\n" + "="*70)
    log_output("🎯 RECOMMENDATIONS (ranked by measured relative lift)")
    log_output("="*70)

    ranked_tests = sorted(
        ab_results.items(),
        key=lambda kv: kv[1]['relative_lift_pct'],
        reverse=True
    )

    for rank, (test_name, r) in enumerate(ranked_tests, start=1):
        sig_note = "statistically significant" if r['is_significant'] else "NOT statistically significant — do not deploy on this result alone"
        log_output(f"\n{rank}️⃣ {test_name.upper()}")
        log_output(f"   Control: {r['control_rate']:.2f}%  |  Treatment: {r['treatment_rate']:.2f}%")
        log_output(f"   Relative Lift: {r['relative_lift_pct']:+.2f}%")
        log_output(f"   p-value: {r['p_value']:.4f} ({sig_note})")
    
    log_output("\n" + "="*70)
    log_output("✅ REPORT COMPLETE!")
    log_output("="*70)
    log_output(f"\n📄 Report saved to: {REPORT_FILE}")
    log_output("📁 Check your project folder to open it!")

# ==========================================
# 10. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    log_output("\n🚀 Starting PLG Analytics EDA...\n")
    
    connection = connect_to_mysql()
    
    if connection:
        dfs = load_data(connection)
        generate_report(connection, dfs)
        connection.close()
        log_output("\n🔒 Database connection closed.")
    else:
        log_output("❌ Failed to connect to database.")
    
    log_output("\n✨ Script execution completed!")
