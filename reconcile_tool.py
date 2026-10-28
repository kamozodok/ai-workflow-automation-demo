import pandas as pd
import numpy as np
import datetime
import os

def generate_mock_data():
    """Generates synthetic e-commerce orders and bank transaction logs for demonstration."""
    np.random.seed(42)
    dates = [datetime.date(2026, 10, i) for i in range(1, 16)]
    
    # Generate Store Invoices (SellerCloud / Shopify style)
    invoices = []
    for i in range(100):
        inv_id = f"INV-{1000 + i}"
        date = np.random.choice(dates)
        amount = round(np.random.uniform(25.0, 450.0), 2)
        status = "Paid"
        invoices.append({"Invoice_ID": inv_id, "Date": date, "Amount_USD": amount, "Status": status})
    
    df_invoices = pd.DataFrame(invoices)
    
    # Generate Bank Statements (QuickBooks / Stripe settlement style)
    # Replicate invoices with some minor noise, fee deductions, missing items, and duplicates
    bank_records = []
    for idx, row in df_invoices.iterrows():
        # 85% perfect match
        if idx < 85:
            bank_records.append({"Transaction_Ref": f"TXN-{row['Invoice_ID']}", "Date": row['Date'], "Amount_Received": row['Amount_USD'], "Notes": "Settlement payment"})
        # 5% amount mismatch (payment processor fee deducted)
        elif idx < 90:
            bank_records.append({"Transaction_Ref": f"TXN-{row['Invoice_ID']}", "Date": row['Date'], "Amount_Received": round(row['Amount_USD'] * 0.97, 2), "Notes": "Partial payment / Fee deducted"})
        # 10% missing from bank (unreconciled invoice)
        else:
            pass

    # Add 3 unexpected deposits (unmatched bank transactions)
    for k in range(3):
        bank_records.append({"Transaction_Ref": f"TXN-UNMATCHED-{k+1}", "Date": datetime.date(2026, 10, 10), "Amount_Received": 150.00, "Notes": "Direct wire transfer"})

    df_bank = pd.DataFrame(bank_records)
    
    return df_invoices, df_bank

def reconcile_accounts(df_invoices, df_bank):
    """Core reconciliation engine matching invoice IDs with bank records."""
    # Extract Invoice ID reference from Transaction_Ref
    df_bank['Invoice_ID_Extract'] = df_bank['Transaction_Ref'].str.replace('TXN-', '', regex=False)
    
    # Merge datasets on Invoice ID
    merged = pd.merge(df_invoices, df_bank, left_on='Invoice_ID', right_on='Invoice_ID_Extract', how='outer')
    
    # Flag status
    conditions = [
        (merged['Invoice_ID'].notna()) & (merged['Transaction_Ref'].notna()) & (merged['Amount_USD'] == merged['Amount_Received']),
        (merged['Invoice_ID'].notna()) & (merged['Transaction_Ref'].notna()) & (merged['Amount_USD'] != merged['Amount_Received']),
        (merged['Invoice_ID'].notna()) & (merged['Transaction_Ref'].isna()),
        (merged['Invoice_ID'].isna()) & (merged['Transaction_Ref'].notna())
    ]
    choices = ['RECONCILED', 'AMOUNT_DISCREPANCY', 'UNPAID_INVOICE', 'UNMATCHED_DEPOSIT']
    
    merged['Reconciliation_Status'] = np.select(conditions, choices, default='UNKNOWN')
    merged['Variance'] = merged['Amount_USD'].fillna(0) - merged['Amount_Received'].fillna(0)
    
    return merged

def main():
    print("--- Starting Automated Reconciliation Pipeline ---")
    df_invoices, df_bank = generate_mock_data()
    
    reconciled_df = reconcile_accounts(df_invoices, df_bank)
    
    summary = reconciled_df['Reconciliation_Status'].value_counts()
    print("\n--- Summary Report ---")
    print(summary)
    print(f"\nTotal Discrepancy Amount: ${reconciled_df['Variance'].abs().sum():,.2f}")
    
    # Export outputs
    reconciled_df.to_csv("reconciliation_summary.csv", index=False)
    print("\n[SUCCESS] Reconciled data saved to 'reconciliation_summary.csv'")

if __name__ == "__main__":
    main()