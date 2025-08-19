    
import pandas as pd
import numpy as np

class Utils_scheduler:
    
    def __parse_level(level_str):
        """
        Parsea el string del nivel para extraer columna y valores específicos (si existen).
        Si el nivel tiene paréntesis, devuelve (columna, [valores]), si no, (columna, None)
        """
        if "(" in level_str and ")" in level_str:
            col, vals = level_str.split("(", 1)
            col = col.strip()
            vals = vals.strip(")")
            vals = [v.strip() for v in vals.split(",")]
            return col, vals
        else:
            return level_str.strip(), None

    def build_hierarchy(df, levels, idx=0):
        """
        Función recursiva para construir la jerarquía de niveles a partir de un DataFrame y una lista de niveles.
        """
        if idx >= len(levels):
            return []
        col, vals = self.__parse_level(levels[idx])
        if col not in df.columns:
            return {}
        if vals is not None:
            unique_vals = [v for v in vals if v in df[col].astype(str).unique()]
        else:
            unique_vals = df[col].astype(str).unique().tolist()
        result = {}
        for val in unique_vals:
            filtered = df[df[col].astype(str) == val]
            if idx + 1 < len(levels):
                result[val] = Utils_scheduler.build_hierarchy(filtered, levels, idx + 1)
            else:
                result[val] = []
        return result


    def get_level_combinations(df, levels):
        """
        Devuelve un diccionario donde la clave es el número de nivel (1-indexed) y el valor es una lista de combinaciones (listas) de valores hasta ese nivel.
        """
        combos = {}
        prev = [()]
        for i, level in enumerate(levels):
            col, vals = self.__parse_level(level)
            if col not in df.columns:
                combos[f"Nivel {i+1}"] = []
                prev = []
                continue
            # Si la cantidad de variables es mayor a cero
            if len(vals) > 0:
                # Toma cada valor v de vals (que normalmente provienen de los valores entre paréntesis en la jerarquía).
                unique_vals = [v for v in vals if v in df[col].unique()]
            else:
                # Toma todos los valores unicos
                unique_vals = df[col].unique().tolist()
            # variable auxiliar para realizar las combinacciones del nivel
            new_prev = []
            for comb in prev:
                if comb:
                    # crea una mascara del tamaño del vector
                    mask = pd.Series([True]*len(df))
                    for j, prev_level in enumerate(levels[:i]):
                        prev_col, _ = self.__parse_level(prev_level)
                        mask &= (df[prev_col].astype(str) == comb[j])
                    filtered = df[mask]
                else:
                    filtered = df
                for val in unique_vals:
                    if val in filtered[col].astype(str).unique():
                        new_prev.append(comb + (val,))
            combos[f"Nivel {i+1}"] = [list(c) for c in new_prev]
            prev = new_prev
        return combos