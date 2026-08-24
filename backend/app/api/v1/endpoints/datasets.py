from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import pandas as pd
import io
import json

from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetRead
from app.schemas.common import GenericResponse

router = APIRouter()


def detect_column_type(series: pd.Series) -> str:
    """Detect the semantic type of a pandas Series."""
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_integer_dtype(series):
        return "int"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    # Check string columns for dates, categorical vs free text
    if pd.api.types.is_string_dtype(series):
        # Try to detect date strings
        non_null = series.dropna()
        if len(non_null) > 0:
            sample = non_null.head(10)
            date_patterns = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"]
            for fmt in date_patterns:
                try:
                    pd.to_datetime(sample, format=fmt)
                    return "datetime"
                except (ValueError, TypeError):
                    continue
            # Also try pandas auto-detection
            try:
                parsed = pd.to_datetime(sample, errors="coerce")
                if parsed.notna().sum() >= len(sample) * 0.8:
                    return "datetime"
            except Exception:
                pass
        # Check for categorical
        nunique = series.nunique()
        if nunique < min(20, len(series) * 0.3):
            return "category"
        return "string"
    return "string"


def analyze_dataset(df: pd.DataFrame) -> dict:
    """Analyze a DataFrame and return schema + quality stats."""
    columns = list(df.columns)
    types = {}
    null_counts = {}
    stats = {}

    for col in columns:
        col_type = detect_column_type(df[col])
        types[col] = col_type
        null_counts[col] = int(df[col].isnull().sum())

        col_stats: dict[str, Any] = {
            "null_count": null_counts[col],
            "null_pct": round(null_counts[col] / len(df) * 100, 1) if len(df) > 0 else 0,
            "unique_count": int(df[col].nunique()),
        }

        if col_type in ("float", "int"):
            col_stats["min"] = float(df[col].min()) if not df[col].isnull().all() else None
            col_stats["max"] = float(df[col].max()) if not df[col].isnull().all() else None
            col_stats["mean"] = round(float(df[col].mean()), 2) if not df[col].isnull().all() else None
            col_stats["std"] = round(float(df[col].std()), 2) if not df[col].isnull().all() else None

            # IQR outlier detection
            if col_type == "float" and not df[col].isnull().all():
                q1 = float(df[col].quantile(0.25))
                q3 = float(df[col].quantile(0.75))
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers = int(((df[col] < lower_bound) | (df[col] > upper_bound)).sum())
                col_stats["outlier_count"] = outliers
                col_stats["iqr_lower"] = round(lower_bound, 2)
                col_stats["iqr_upper"] = round(upper_bound, 2)

        stats[col] = col_stats

    return {
        "columns": columns,
        "types": types,
        "null_counts": null_counts,
        "stats": stats,
    }


@router.get("", response_model=GenericResponse[List[dict]])
async def list_datasets(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    stmt = select(Dataset).order_by(Dataset.created_at.desc())
    if current_user.organization_id:
        stmt = stmt.where(Dataset.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    datasets = res.scalars().all()
    out = [DatasetRead.model_validate(d).model_dump(mode="json") for d in datasets]
    return GenericResponse(success=True, message="Datasets retrieved successfully", data=out)


@router.post("/upload", response_model=GenericResponse[dict], status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    content = await file.read()
    filename = file.filename or "uploaded_data.csv"
    file_size = len(content)

    # Parse CSV or Excel
    try:
        if filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(content))
        elif filename.lower().endswith(".json"):
            df = pd.read_json(io.BytesIO(content))
        else:
            df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="File contains no data rows")

    # Analyze the dataset
    analysis = analyze_dataset(df)

    # Store sample rows (first 20) as JSON for preview
    sample_rows = df.head(20).fillna("").to_dict(orient="records")

    # Build column schema for DB storage
    column_schema = {
        "columns": analysis["columns"],
        "types": analysis["types"],
        "stats": analysis["stats"],
        "sample_rows": sample_rows,
    }

    dataset = Dataset(
        name=filename,
        file_path=f"/uploads/{filename}",
        file_size_bytes=file_size,
        row_count=len(df),
        column_schema=column_schema,
        status="COMPLETED",
        organization_id=current_user.organization_id or "demo-org-1",
        uploaded_by_id=current_user.id,
    )
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)

    return GenericResponse(
        success=True,
        message=f"Dataset '{filename}' uploaded and analyzed successfully ({len(df)} rows, {len(df.columns)} columns)",
        data=DatasetRead.model_validate(dataset).model_dump(mode="json"),
    )


@router.get("/{dataset_id}", response_model=GenericResponse[dict])
async def get_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    stmt = select(Dataset).where(Dataset.id == dataset_id)
    res = await db.execute(stmt)
    dataset = res.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return GenericResponse(
        success=True,
        message="Dataset details retrieved",
        data=DatasetRead.model_validate(dataset).model_dump(mode="json"),
    )


@router.get("/{dataset_id}/preview", response_model=GenericResponse[dict])
async def preview_dataset(
    dataset_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Return sample rows and column stats for a dataset."""
    stmt = select(Dataset).where(Dataset.id == dataset_id)
    res = await db.execute(stmt)
    dataset = res.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    schema = dataset.column_schema or {}
    sample_rows = schema.get("sample_rows", [])[:limit]

    return GenericResponse(
        success=True,
        message="Dataset preview retrieved",
        data={
            "id": dataset.id,
            "name": dataset.name,
            "row_count": dataset.row_count,
            "columns": schema.get("columns", []),
            "types": schema.get("types", {}),
            "stats": schema.get("stats", {}),
            "sample_rows": sample_rows,
        },
    )


@router.get("/{dataset_id}/quality", response_model=GenericResponse[dict])
async def quality_report(
    dataset_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Generate a comprehensive data quality report for a dataset."""
    stmt = select(Dataset).where(Dataset.id == dataset_id)
    res = await db.execute(stmt)
    dataset = res.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    schema = dataset.column_schema or {}
    sample_rows = schema.get("sample_rows", [])
    if not sample_rows:
        raise HTTPException(status_code=400, detail="No data available for quality analysis")

    df = pd.DataFrame(sample_rows)
    total_rows = len(df)
    total_cols = len(df.columns)

    # 1. Completeness analysis
    null_info = []
    total_cells = total_rows * total_cols
    total_nulls = 0
    for col in df.columns:
        n_null = int(df[col].isnull().sum())
        n_empty = int((df[col].astype(str).str.strip() == "").sum())
        total_col_nulls = n_null + n_empty
        total_nulls += total_col_nulls
        null_info.append({
            "column": col,
            "null_count": n_null,
            "empty_count": n_empty,
            "total_missing": total_col_nulls,
            "missing_pct": round(total_col_nulls / total_rows * 100, 1) if total_rows > 0 else 0,
        })
    completeness_score = round((1 - total_nulls / total_cells) * 100, 1) if total_cells > 0 else 100

    # 2. Outlier analysis (IQR method)
    outlier_info = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            series = df[col].dropna()
            if len(series) > 4:
                q1 = float(series.quantile(0.25))
                q3 = float(series.quantile(0.75))
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                n_outliers = int(((series < lower) | (series > upper)).sum())
                outlier_info.append({
                    "column": col,
                    "outlier_count": n_outliers,
                    "outlier_pct": round(n_outliers / len(series) * 100, 1),
                    "lower_bound": round(lower, 2),
                    "upper_bound": round(upper, 2),
                })

    total_outliers = sum(o["outlier_count"] for o in outlier_info)
    outlier_score = round((1 - total_outliers / total_rows) * 100, 1) if total_rows > 0 else 100

    # 3. Uniqueness analysis (duplicate detection)
    duplicate_rows = int(df.duplicated().sum())
    uniqueness_score = round((1 - duplicate_rows / total_rows) * 100, 1) if total_rows > 0 else 100

    # 4. Consistency check (data type consistency per column)
    consistency_issues = []
    for col in df.columns:
        non_null = df[col].dropna()
        if len(non_null) > 0:
            types_found = set()
            for val in non_null:
                try:
                    float(val)
                    types_found.add("numeric")
                except (ValueError, TypeError):
                    types_found.add("text")
            if len(types_found) > 1:
                consistency_issues.append({
                    "column": col,
                    "issue": "Mixed types (numeric + text)",
                    "severity": "warning",
                })

    consistency_score = round((1 - len(consistency_issues) / total_cols) * 100, 1) if total_cols > 0 else 100

    # 5. Type distribution
    type_dist = {}
    for col in df.columns:
        t = detect_column_type(df[col])
        type_dist[t] = type_dist.get(t, 0) + 1

    # 6. Overall quality score (weighted average)
    overall_score = round(
        completeness_score * 0.30 +
        outlier_score * 0.20 +
        uniqueness_score * 0.25 +
        consistency_score * 0.25,
        1
    )

    # 7. Recommendations
    recommendations = []
    if completeness_score < 95:
        recommendations.append({
            "priority": "high",
            "message": f"Dataset has {round(100 - completeness_score, 1)}% missing values. Consider imputation or removing sparse columns.",
        })
    if outlier_score < 90:
        recommendations.append({
            "priority": "medium",
            "message": f"{total_outliers} outliers detected. Review for data entry errors or natural variation.",
        })
    if uniqueness_score < 95:
        recommendations.append({
            "priority": "medium",
            "message": f"{duplicate_rows} duplicate rows found. Consider deduplication.",
        })
    if consistency_issues:
        recommendations.append({
            "priority": "low",
            "message": f"{len(consistency_issues)} columns have mixed data types. Standardize for better ML results.",
        })
    if not recommendations:
        recommendations.append({
            "priority": "info",
            "message": "Dataset quality looks great! Ready for ML training.",
        })

    return GenericResponse(
        success=True,
        message="Data quality report generated",
        data={
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "total_rows": total_rows,
            "total_columns": total_cols,
            "overall_score": overall_score,
            "scores": {
                "completeness": completeness_score,
                "outlier_free": outlier_score,
                "uniqueness": uniqueness_score,
                "consistency": consistency_score,
            },
            "null_analysis": null_info,
            "outlier_analysis": outlier_info,
            "duplicates": {
                "count": duplicate_rows,
                "pct": round(duplicate_rows / total_rows * 100, 1) if total_rows > 0 else 0,
            },
            "type_distribution": type_dist,
            "consistency_issues": consistency_issues,
            "recommendations": recommendations,
        },
    )


@router.delete("/{dataset_id}", response_model=GenericResponse[None])
async def delete_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    stmt = select(Dataset).where(Dataset.id == dataset_id)
    res = await db.execute(stmt)
    dataset = res.scalar_one_or_none()
    if dataset:
        await db.delete(dataset)
        await db.commit()
    return GenericResponse(success=True, message="Dataset deleted successfully", data=None)
