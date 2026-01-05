import pandas as pd

def read_excel_and_filter(file_path, filename_keyword=None, role=None, role_desc=None, closing_date=None):
    # Read the Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return f"Error reading the file: {e}"

    # Convert all column names to lowercase for case-insensitive matching
    df.columns = df.columns.str.lower()

    # Apply filters based on input parameters
    if filename_keyword:
        df = df[df['filename'].str.lower().str.startswith(filename_keyword.lower(), na=False)]
    if role and role_desc:
        role_column = role.lower()
        if role_column in df.columns:
            df = df[df[role_column].str.contains(role_desc, na=False, case=False)]
        else:
            return f"Role column '{role}' not found in the file."
    if closing_date:
        # Ensure the 'closingdate' column is parsed and normalized to match the closing_date
        if 'closingdate' in df.columns:
            # Attempt to parse the 'closingdate' column into datetime format
            df['closingdate'] = pd.to_datetime(df['closingdate'], errors='coerce', infer_datetime_format=True)
            # Convert to yyyy-mm-dd format for comparison
            df['closingdate'] = df['closingdate'].dt.strftime('%Y-%m-%d')
            # Filter rows matching the closing_date
            df = df[df['closingdate'] == closing_date]
        else:
            return "Closing date column 'closingdate' not found in the file."

    # Convert each column to a list and return as a dictionary
    result = [df[col].tolist() for col in df.columns]
    return result

# Example usage
if __name__ == "__main__":
    file_path = "example.xlsx"  # Replace with your Excel file path
    filename_keyword = "test"  # Replace with your filename keyword
    role = "role1"  # Replace with the role column (e.g., role1, role2, etc.)
    role_desc = "admin"  # Replace with the role description
    closing_date = "2023-10-01"  # Replace with the closing date

    result = read_excel_and_filter(file_path, filename_keyword, role, role_desc, closing_date)
    print(result)