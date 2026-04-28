import pandas as pd
from typing import Dict, Any, List

def get_dataframe_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Returns a dictionary containing summary statistics of a DataFrame."""
    summary = {
        "shape": df.shape,
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }
    return summary

def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Returns a list of numeric column names."""
    return df.select_dtypes(include=['number']).columns.tolist()

def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Returns a list of categorical column names."""
    return df.select_dtypes(exclude=['number']).columns.tolist()
