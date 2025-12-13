import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
import json

# Initialize Faker with seed for reproducible data
fake = Faker()
fake.seed_instance(42)
random.seed(42)

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kaushikyeddanapudi_75',
    'database': 'plg_analytics',
    'charset': 'utf8mb4'
}

def connect_to_mysql():
    """Establish MySQL connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connected to MySQL successfully!")
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("💡 Check if MySQL is running and password is correct.")
        return None

def generate_users(connection, num_users=10000):
    """Generate user dimension data with UNIQUE emails"""
    print(f"\n🔄 Generating {num_users:,} users...")
    cursor = connection.cursor()
    
    user_segments = ['Organic', 'Paid', 'Referral', 'Direct']
    device_types = ['Desktop', 'Mobile', 'Tablet']
    platforms = ['Web', 'iOS', 'Android']
    industries = ['SaaS', 'Finance', 'Healthcare', 'Retail', 'Tech', 'E-commerce', 'Education', 'Media']
    
    users_data = []
    start_date = datetime(2024, 1, 1)
    
    # Clear any previous unique cache
    fake.unique.clear()
    
    for i in range(num_users):
        signup_date = start_date + timedelta(days=random.randint(0, 330))
        email = fake.unique.email()  # UNIQUE email guaranteed
        
        users_data.append((
            email,
            fake.company(),
            random.choice(user_segments),
            signup_date.date(),
            fake.country(),
            random.choice(device_types),
            random.choice(platforms),
            random.choice(industries)
        ))
    
    cursor.executemany("""
        INSERT INTO dim_users (email, company_name, user_segment, signup_date, country, 
                              device_type, platform, industry)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, users_data)
    
    connection.commit()
    cursor.close()
    print(f"✅ Generated {num_users:,} users!")

def generate_user_events(connection, num_users=10000):
    """Generate user event journey data"""
    print(f"\n🔄 Generating user events (funnel journey)...")
    cursor = connection.cursor()
    
    # Get all user IDs
    cursor.execute("SELECT user_id, signup_date FROM dim_users")
    users = cursor.fetchall()
    
    events_data = []
    batch_size = 50000
    event_count = 0
    
    # Event type probabilities (funnel conversion rates)
    activation_rate = 0.70
    feature_adoption_rate = 0.50
    pql_rate = 0.40
    conversion_rate = 0.25
    
    for user_id, signup_date in users:
        signup_timestamp = datetime.combine(signup_date, datetime.min.time())
        
        # EVENT 1: Signup (always happens)
        events_data.append((
            user_id,
            'signup',
            signup_timestamp,
            0,
            json.dumps({'source': 'web', 'plan': 'free'})
        ))
        event_count += 1
        
        # EVENT 2: Activation (70% of users)
        if random.random() < activation_rate:
            activation_timestamp = signup_timestamp + timedelta(hours=random.randint(1, 72))
            events_data.append((
                user_id,
                'activation',
                activation_timestamp,
                0,
                json.dumps({'event': 'completed_onboarding'})
            ))
            event_count += 1
            
            # EVENT 3: Feature Usage (50% of activated users)
            if random.random() < feature_adoption_rate:
                feature_timestamp = activation_timestamp + timedelta(hours=random.randint(2, 168))
                features = ['dashboard_view', 'analytics_report', 'data_export', 'automation_setup']
                events_data.append((
                    user_id,
                    'feature_use',
                    feature_timestamp,
                    0,
                    json.dumps({'feature': random.choice(features)})
                ))
                event_count += 1
                
                # EVENT 4: PQL Qualification (40% of engaged users)
                if random.random() < pql_rate:
                    pql_timestamp = feature_timestamp + timedelta(days=random.randint(1, 14))
                    events_data.append((
                        user_id,
                        'pql_qualified',
                        pql_timestamp,
                        0,
                        json.dumps({'pql_reason': 'high_usage_score'})
                    ))
                    event_count += 1
                    
                    # EVENT 5: Payment (25% of PQLs)
                    if random.random() < conversion_rate:
                        payment_timestamp = pql_timestamp + timedelta(days=random.randint(1, 30))
                        payment_amount = round(random.uniform(29, 299), 2)
                        events_data.append((
                            user_id,
                            'payment_complete',
                            payment_timestamp,
                            payment_amount,
                            json.dumps({'plan': 'pro', 'payment_method': 'credit_card'})
                        ))
                        event_count += 1
        
        # Batch insert for performance
        if len(events_data) >= batch_size:
            cursor.executemany("""
                INSERT INTO fact_user_events (user_id, event_type, event_timestamp, event_value, metadata)
                VALUES (%s, %s, %s, %s, %s)
            """, events_data)
            connection.commit()
            print(f"   Inserted {event_count:,} events...")
            events_data = []
    
    # Insert remaining events
    if events_data:
        cursor.executemany("""
            INSERT INTO fact_user_events (user_id, event_type, event_timestamp, event_value, metadata)
            VALUES (%s, %s, %s, %s, %s)
        """, events_data)
        connection.commit()
    
    cursor.close()
    print(f"✅ Generated {event_count:,} user events!")

def generate_ab_tests(connection, num_users=10000):
    """Generate A/B test assignment data - FIXED VERSION"""
    print(f"\n🔄 Generating A/B test assignments...")
    cursor = connection.cursor()
    
    cursor.execute("SELECT user_id FROM dim_users")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    test_scenarios = [
        ('onboarding_flow', ['control', 'treatment_quick_start'], 0.65),
        ('pricing_strategy', ['control_7day_trial', 'treatment_freemium'], 0.50),
        ('feature_adoption', ['control', 'treatment_tooltip_guide'], 0.55)
    ]
    
    ab_tests_data = []
    test_start = datetime(2024, 1, 15)
    test_end = datetime(2024, 6, 30)
    
    for test_name, variants, conversion_lift in test_scenarios:
        for user_id in user_ids[:8000]:
            variant = random.choice(variants)
            test_date = test_start + timedelta(days=random.randint(0, 166))
            
            # Determine if user converted
            if variant.startswith('treatment'):
                converted = 1 if random.random() < (0.15 + conversion_lift) else 0
            else:
                converted = 1 if random.random() < 0.15 else 0
            
            # Only set conversion_timestamp if converted
            if converted == 1:
                conversion_timestamp = test_date + timedelta(days=random.randint(1, 30))
            else:
                conversion_timestamp = None
            
            ab_tests_data.append((
                user_id,
                test_name,
                variant,
                test_date.date(),
                test_end.date(),
                converted,
                conversion_timestamp  # ✅ NOW HANDLES None PROPERLY
            ))
    
    # FIX: Insert in smaller batches to handle None values
    batch_size = 5000
    for i in range(0, len(ab_tests_data), batch_size):
        batch = ab_tests_data[i:i+batch_size]
        try:
            cursor.executemany("""
                INSERT INTO fact_ab_tests (user_id, test_name, variant, test_start_date, test_end_date, converted, conversion_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, batch)
            connection.commit()
        except Exception as e:
            print(f"   ⚠️ Error in batch {i//batch_size + 1}: {e}")
            connection.rollback()
            raise
    
    cursor.close()
    print(f"✅ Generated {len(ab_tests_data):,} A/B test assignments!")

def generate_cohort_data(connection, num_users=10000):
    """Generate cohort analysis data"""
    print(f"\n🔄 Generating cohort analysis data...")
    cursor = connection.cursor()
    
    cursor.execute("SELECT user_id, signup_date FROM dim_users")
    users = cursor.fetchall()
    
    cohort_data = []
    
    for user_id, signup_date in users:
        # Cohort = signup week
        cohort_date = signup_date - timedelta(days=signup_date.weekday())
        
        # Pull event timeline for this user
        cursor.execute("""
            SELECT event_type, event_timestamp FROM fact_user_events 
            WHERE user_id = %s ORDER BY event_timestamp
        """, (user_id,))
        events = cursor.fetchall()
        
        activation_date = None
        feature_date = None
        pql_date = None
        payment_date = None
        
        for event_type, event_timestamp in events:
            if event_type == 'activation' and not activation_date:
                activation_date = event_timestamp.date() if isinstance(event_timestamp, datetime) else event_timestamp
            elif event_type == 'feature_use' and not feature_date:
                feature_date = event_timestamp.date() if isinstance(event_timestamp, datetime) else event_timestamp
            elif event_type == 'pql_qualified' and not pql_date:
                pql_date = event_timestamp.date() if isinstance(event_timestamp, datetime) else event_timestamp
            elif event_type == 'payment_complete' and not payment_date:
                payment_date = event_timestamp.date() if isinstance(event_timestamp, datetime) else event_timestamp
        
        # Calculate days to each milestone
        days_to_activation = (activation_date - signup_date).days if activation_date else None
        days_to_pql = (pql_date - signup_date).days if pql_date else None
        days_to_payment = (payment_date - signup_date).days if payment_date else None
        
        cohort_data.append((
            user_id,
            cohort_date,
            signup_date,
            activation_date,
            feature_date,
            pql_date,
            payment_date,
            days_to_activation,
            days_to_pql,
            days_to_payment
        ))
    
    # Insert in batches
    batch_size = 5000
    for i in range(0, len(cohort_data), batch_size):
        batch = cohort_data[i:i+batch_size]
        cursor.executemany("""
            INSERT INTO fact_cohort_data (user_id, cohort_date, signup_date, activation_date, feature_adoption_date, 
                                          pql_date, payment_date, days_to_activation, days_to_pql, days_to_payment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        connection.commit()
    
    cursor.close()
    print(f"✅ Generated cohort analysis data ({len(cohort_data):,} records)!")

def print_statistics(connection):
    """Print final database statistics"""
    print("\n" + "="*60)
    print("📊 DATABASE STATISTICS")
    print("="*60)
    
    cursor = connection.cursor()
    
    tables_stats = [
        ('dim_users', 'Total Users'),
        ('fact_user_events', 'Total Events'),
        ('fact_ab_tests', 'Total A/B Test Assignments'),
        ('fact_cohort_data', 'Total Cohort Records')
    ]
    
    for table, label in tables_stats:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"✅ {label}: {count:,} records")
    
    print("\n📈 KEY METRICS:")
    
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN event_type = 'activation' THEN 1 ELSE 0 END) as activations,
            SUM(CASE WHEN event_type = 'feature_use' THEN 1 ELSE 0 END) as feature_uses,
            SUM(CASE WHEN event_type = 'pql_qualified' THEN 1 ELSE 0 END) as pqls,
            SUM(CASE WHEN event_type = 'payment_complete' THEN 1 ELSE 0 END) as payments
        FROM fact_user_events
    """)
    
    activations, feature_uses, pqls, payments = cursor.fetchone()
    
    print(f"   Signups: 10,000")
    print(f"   Activations: {activations:,} ({activations/100:.1f}%)")
    print(f"   Feature Users: {feature_uses:,} ({feature_uses/100:.1f}%)")
    print(f"   PQLs: {pqls:,} ({pqls/100:.1f}%)")
    print(f"   Paid Customers: {payments:,} ({payments/100:.1f}%)")
    
    cursor.close()

def main():
    print("\n" + "="*60)
    print("🚀 PLG ANALYTICS - DATA GENERATION STARTING")
    print("="*60)
    
    connection = connect_to_mysql()
    if not connection:
        print("\n❌ Failed to connect. Please check your MySQL connection.")
        return
    
    try:
        generate_users(connection, num_users=10000)
        generate_user_events(connection, num_users=10000)
        generate_ab_tests(connection, num_users=10000)
        generate_cohort_data(connection, num_users=10000)
        print_statistics(connection)
        
        print("\n" + "="*60)
        print("🎉 DATA GENERATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n✅ Your PLG Analytics database is ready!")
        print("📊 Next step: Run SQL analysis queries")
        
    except Exception as e:
        print(f"\n❌ Error during data generation: {e}")
        import traceback
        traceback.print_exc()
        connection.rollback()
    finally:
        connection.close()
        print("\n🔒 Database connection closed.")

if __name__ == "__main__":
    main()