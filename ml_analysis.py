# ============================================================
# HUMANITARIAN AID — ML PATTERN DETECTION
# Simulated Dataset | Portfolio Demonstration
# ============================================================
# Techniques used:
#   1. Anomaly Detection       (Isolation Forest)
#   2. Beneficiary Clustering  (K-Means)
#   3. Delay Risk Prediction   (Random Forest Classifier)
# ============================================================

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# ============================================================
# STEP 0 — Recreate the dataset (same logic as Excel builder)
# ============================================================
n = 1000
camps = ['Camp Alpha','Camp Beta','Camp Gamma','Camp Delta','Camp Epsilon','Camp Zeta']
camp_weights = [0.25,0.20,0.18,0.15,0.12,0.10]
aid_types = ['Food Basket','NFI Kit','Cash Transfer','Medical Kit','Shelter Kit']
vuln_cats = ['Child-headed HH','Female-headed HH','PWD Member','Elderly Head','Standard']

family_sizes = np.random.choice(range(1,13), size=n,
    p=[0.05,0.10,0.15,0.18,0.15,0.12,0.09,0.07,0.04,0.03,0.01,0.01])
camps_col   = np.random.choice(camps, size=n, p=camp_weights)
vuln_scores = np.round(np.random.beta(2,3,n)*100, 1)

vuln_categories = []
for s in vuln_scores:
    if s >= 75:
        vuln_categories.append(np.random.choice(['Child-headed HH','PWD Member']))
    elif s >= 55:
        vuln_categories.append(np.random.choice(['Female-headed HH','Elderly Head'], p=[0.6,0.4]))
    else:
        vuln_categories.append('Standard')

eligibility, distribution_status = [], []
for s, f in zip(vuln_scores, family_sizes):
    if s >= 60 or f >= 6:
        eligibility.append('Eligible')
    elif s >= 40 or f >= 4:
        eligibility.append('Eligible' if np.random.random() < 0.7 else 'Pending Review')
    else:
        r = np.random.random()
        eligibility.append('Eligible' if r < 0.3 else ('Not Eligible' if r < 0.5 else 'Pending Review'))

for e in eligibility:
    if e == 'Eligible':
        r = np.random.random()
        distribution_status.append('Distributed' if r < 0.72 else
                                   ('Pending Distribution' if r < 0.88 else 'Delayed'))
    elif e == 'Pending Review':
        distribution_status.append('On Hold')
    else:
        distribution_status.append('Not Applicable')

df = pd.DataFrame({
    'Case_ID'              : [f'HH-{i+1001}' for i in range(n)],
    'Camp'                 : camps_col,
    'Family_Size'          : family_sizes,
    'Vulnerability_Category': vuln_categories,
    'Vulnerability_Score'  : vuln_scores,
    'Aid_Type'             : np.random.choice(aid_types, n),
    'Eligibility_Status'   : eligibility,
    'Distribution_Status'  : distribution_status,
    'Cycle'                : np.random.choice(['Cycle 1','Cycle 2','Cycle 3','Cycle 4'], n,
                                               p=[0.28,0.27,0.25,0.20])
})

print("=" * 60)
print("HUMANITARIAN AID — ML PATTERN DETECTION")
print("Simulated Dataset | Portfolio Demonstration")
print("=" * 60)
print(f"\nDataset loaded: {len(df)} cases\n")

# ============================================================
# MODULE 1 — ANOMALY DETECTION (Isolation Forest)
# Goal: find households that are "unusual" — high need but
#       not receiving aid, or low score but marked eligible
# ============================================================
print("─" * 60)
print("MODULE 1 · ANOMALY DETECTION (Isolation Forest)")
print("─" * 60)

le_camp = LabelEncoder()
le_vuln = LabelEncoder()
le_aid  = LabelEncoder()

df['Camp_enc']  = le_camp.fit_transform(df['Camp'])
df['Vuln_enc']  = le_vuln.fit_transform(df['Vulnerability_Category'])
df['Aid_enc']   = le_aid.fit_transform(df['Aid_Type'])
df['Distributed_flag'] = (df['Distribution_Status'] == 'Distributed').astype(int)
df['Eligible_flag']    = (df['Eligibility_Status']  == 'Eligible').astype(int)

features_anomaly = ['Vulnerability_Score','Family_Size','Camp_enc',
                    'Vuln_enc','Eligible_flag','Distributed_flag']
X_anomaly = df[features_anomaly].copy()

scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X_anomaly)

iso = IsolationForest(contamination=0.07, random_state=42)
df['Anomaly'] = iso.fit_predict(X_scaled)
df['Anomaly_Flag'] = df['Anomaly'].map({1: 'Normal', -1: 'Anomaly'})

anomalies = df[df['Anomaly'] == -1]
print(f"\nTotal anomalies detected : {len(anomalies)} cases ({len(anomalies)/n*100:.1f}% of dataset)")
print(f"\nTop anomaly patterns:")

# High vulnerability + not distributed
critical = anomalies[
    (anomalies['Vulnerability_Score'] >= 60) &
    (anomalies['Distribution_Status'] != 'Distributed')
]
print(f"  · High-need cases NOT distributed : {len(critical)}")

# Eligible but delayed
delayed_elig = anomalies[
    (anomalies['Eligibility_Status'] == 'Eligible') &
    (anomalies['Distribution_Status'] == 'Delayed')
]
print(f"  · Eligible but DELAYED            : {len(delayed_elig)}")

# Low score but eligible
low_score_elig = anomalies[
    (anomalies['Vulnerability_Score'] < 35) &
    (anomalies['Eligibility_Status'] == 'Eligible')
]
print(f"  · Low score yet marked Eligible   : {len(low_score_elig)}")

print(f"\nAnomaly breakdown by camp:")
camp_anomaly = anomalies.groupby('Camp').size().sort_values(ascending=False)
for camp, count in camp_anomaly.items():
    total = len(df[df['Camp'] == camp])
    print(f"  {camp:<18} {count:>3} anomalies  ({count/total*100:.0f}% of camp)")

# ============================================================
# MODULE 2 — CLUSTERING (K-Means)
# Goal: group households into meaningful segments based on
#       vulnerability + need profile (unsupervised)
# ============================================================
print("\n" + "─" * 60)
print("MODULE 2 · BENEFICIARY CLUSTERING (K-Means, k=4)")
print("─" * 60)

features_cluster = ['Vulnerability_Score','Family_Size','Eligible_flag','Distributed_flag']
X_cluster = StandardScaler().fit_transform(df[features_cluster])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_cluster)

cluster_summary = df.groupby('Cluster').agg(
    Count            = ('Case_ID','count'),
    Avg_Score        = ('Vulnerability_Score','mean'),
    Avg_Family       = ('Family_Size','mean'),
    Pct_Eligible     = ('Eligible_flag','mean'),
    Pct_Distributed  = ('Distributed_flag','mean')
).round(1)

cluster_labels = {}
for idx, row in cluster_summary.iterrows():
    if row['Avg_Score'] >= 60 and row['Pct_Distributed'] < 0.6:
        label = "🔴 High-Need / Under-Served"
    elif row['Avg_Score'] >= 55 and row['Pct_Distributed'] >= 0.7:
        label = "🟡 High-Need / Being Served"
    elif row['Avg_Score'] < 45 and row['Pct_Eligible'] < 0.6:
        label = "🟢 Low-Need / Low Eligibility"
    else:
        label = "🔵 Medium-Need / Partial Coverage"
    cluster_labels[idx] = label

print()
for idx, row in cluster_summary.iterrows():
    print(f"  Cluster {idx} — {cluster_labels[idx]}")
    print(f"    Cases        : {int(row['Count'])}")
    print(f"    Avg vuln score : {row['Avg_Score']}")
    print(f"    Avg family size: {row['Avg_Family']}")
    print(f"    % Eligible     : {row['Pct_Eligible']*100:.0f}%")
    print(f"    % Distributed  : {row['Pct_Distributed']*100:.0f}%")
    print()

df['Cluster_Label'] = df['Cluster'].map(cluster_labels)

# ============================================================
# MODULE 3 — DELAY RISK PREDICTION (Random Forest)
# Goal: predict which ELIGIBLE cases are at risk of being
#       delayed before distribution happens
# ============================================================
print("─" * 60)
print("MODULE 3 · DELAY RISK PREDICTION (Random Forest)")
print("─" * 60)

eligible_df = df[df['Eligibility_Status'] == 'Eligible'].copy()
eligible_df['Delay_Risk'] = (eligible_df['Distribution_Status'] == 'Delayed').astype(int)

le_cycle = LabelEncoder()
eligible_df['Cycle_enc'] = le_cycle.fit_transform(eligible_df['Cycle'])

features_rf = ['Vulnerability_Score','Family_Size','Camp_enc','Vuln_enc','Aid_enc','Cycle_enc']
X = eligible_df[features_rf]
y = eligible_df['Delay_Risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

print(f"\nModel trained on {len(X_train)} cases, tested on {len(X_test)} cases")
print(f"\nClassification Report:")
report = classification_report(y_test, y_pred, target_names=['No Delay','Delayed'], output_dict=True)
print(f"  {'Class':<15} {'Precision':>10} {'Recall':>8} {'F1':>8}")
print(f"  {'─'*45}")
for cls in ['No Delay','Delayed']:
    r = report[cls]
    print(f"  {cls:<15} {r['precision']:>10.2f} {r['recall']:>8.2f} {r['f1-score']:>8.2f}")
print(f"\n  Overall Accuracy : {report['accuracy']:.2f}")

importances = pd.Series(rf.feature_importances_, index=features_rf).sort_values(ascending=False)
print(f"\nFeature Importance (what drives delay risk):")
for feat, imp in importances.items():
    bar = "█" * int(imp * 40)
    print(f"  {feat:<22} {bar:<20} {imp:.3f}")

# High-risk cases
eligible_df['Delay_Probability'] = rf.predict_proba(X)[:,1]
high_risk = eligible_df[eligible_df['Delay_Probability'] >= 0.6].sort_values(
    'Delay_Probability', ascending=False)

print(f"\nHigh-risk cases (probability ≥ 60%) : {len(high_risk)}")
print(f"  Top 5 highest-risk cases:")
top5 = high_risk[['Case_ID','Camp','Vulnerability_Score','Family_Size',
                   'Aid_Type','Delay_Probability']].head(5)
for _, row in top5.iterrows():
    print(f"  {row['Case_ID']}  {row['Camp']:<16} "
          f"Score:{row['Vulnerability_Score']:>5.1f}  "
          f"Family:{int(row['Family_Size'])}  "
          f"Risk:{row['Delay_Probability']:.0%}")

# ============================================================
# EXPORT — save enriched dataset + ML results
# ============================================================
print("\n" + "─" * 60)
print("EXPORTING RESULTS")
print("─" * 60)

output_cols = ['Case_ID','Camp','Family_Size','Vulnerability_Category',
               'Vulnerability_Score','Aid_Type','Eligibility_Status',
               'Distribution_Status','Cycle','Anomaly_Flag','Cluster_Label']

eligible_df_export = eligible_df[['Case_ID','Delay_Probability']].copy()
eligible_df_export['Delay_Risk_Level'] = pd.cut(
    eligible_df_export['Delay_Probability'],
    bins=[0, 0.3, 0.6, 1.0],
    labels=['Low', 'Medium', 'High']
)

final_df = df[output_cols].merge(eligible_df_export, on='Case_ID', how='left')
final_df.to_csv('/home/claude/ml_results.csv', index=False)

print(f"\n  ml_results.csv saved — {len(final_df)} rows, {len(final_df.columns)} columns")
print(f"  Columns added: Anomaly_Flag, Cluster_Label, Delay_Probability, Delay_Risk_Level")

print("\n" + "=" * 60)
print("ML ANALYSIS COMPLETE")
print("=" * 60)
print("""
Summary for your README / rebuttal:
  · Isolation Forest   → detected unusual aid patterns (anomalies)
  · K-Means clustering → segmented beneficiaries into 4 need profiles
  · Random Forest      → predicted delay risk per eligible household
  · All techniques applied to simulated humanitarian data
  · Reflects real-world targeting & monitoring workflows
""")
