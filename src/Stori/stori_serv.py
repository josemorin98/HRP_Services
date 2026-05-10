import pandas as pd
import os


def validar_columnas(df, columnas):
    faltantes = [col for col in columnas if col not in df.columns]

    if faltantes:
        raise ValueError(f"Faltan columnas en el CSV: {faltantes}")


def generate_stori_matrix(config):

    print("Leyendo CSV...")

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )

    csv_path = os.path.join(
        BASE_DIR,
        config["csv_path"].replace("./", "")
    )

    print("Ruta CSV:", csv_path)

    df = pd.read_csv(csv_path, low_memory=False)

    print(df.columns.tolist())

    # Variables
    spatial_cols = list(config["spatialVariables"].values())

    temporal_col = config["temporalVariables"]["Date"]

    observable_col = list(
        config["observableVariables"].values()
    )[0]

    interest_cols = list(
        config["interestVariables"].values()
    )

    # Validar columnas
    validar_columnas(
        df,
        spatial_cols + [temporal_col, observable_col] + interest_cols
    )

    print("Transformando datos a formato STORI...")

    # Spatial
    df["spatial"] = (
        df[spatial_cols]
        .astype(str)
        .agg(".".join, axis=1)
    )

    # Temporal
    df["temporal"] = df[temporal_col]

    # Interest
    df["interest"] = (
        df[interest_cols]
        .astype(str)
        .agg(".".join, axis=1)
    )

    # Observation
    df["observation"] = df[observable_col]

    # Reference
    df["reference"] = df["TASA_TYPE"]

    # STORI final
    stori_df = df[
        [
            "spatial",
            "temporal",
            "interest",
            "observation",
            "reference"
        ]
    ]

    # Eliminar duplicados
    stori_df = stori_df.drop_duplicates()

    
    # Guardar directamente en /data
    output_path = os.path.join(
        BASE_DIR,
        "data",
        "Matriz_stori.csv"
    )

    # Exportar CSV
    stori_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )

    print(f"CSV generado: {output_path}")

    return {
        "output_path": output_path,
        "total_records": len(stori_df)
    }