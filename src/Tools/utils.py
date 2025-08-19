import pandas as pd
import numpy as np

class Utils:
    def verificar_variable_observacion(df, observ_vars, logger):
        """
        Verifica que todas las variables de observación existan como columnas en el DataFrame y sean numéricas.
        Si alguna existe pero no es numérica, manda un warning y retorna False solo si falta la columna.
        observ_vars puede ser un dict o lista de nombres de columnas.
        """
        if isinstance(observ_vars, dict):
            variables = list(observ_vars.values())
        elif isinstance(observ_vars, list):
            variables = observ_vars
        else:
            logger.warning("El formato de observ_vars no es válido. Debe ser dict o list.")
            return False

        missing = [var for var in variables if var not in df.columns]
        if missing:
            logger.warning(f"Faltan variables de observación en el dataset: {missing}")
            return False

        non_numeric = [var for var in variables if not pd.api.types.is_numeric_dtype(df[var])]
        if non_numeric:
            logger.warning(f"Las siguientes variables de observación no son numéricas: {non_numeric}")
        # else:
        #     logger.info(f"Todas las variables de observación {variables} existen y son numéricas en el dataset.")
        return True

    def verificar_variable_temporal(df, temporal_vars, logger):
        """
        Verifica que la columna temporal especificada en el key 'Date' exista en el DataFrame.
        """
        date_col = temporal_vars.get('Date')
        if not date_col:
            logger.warning("No se especificó el nombre de la columna temporal en el key 'Date'.")
            return False
        if date_col in df.columns:
            # logger.info(f"Columna temporal '{date_col}' encontrada en el CSV.")
            return True
        else:
            logger.warning(f"Columna temporal '{date_col}' NO encontrada en el CSV.")
            return False
    
    def verificar_variable_espacial(df, spatial_key, spatial_col, logger):
        """Verifica si la columna y los valores existen para una variable espacial."""
        # Soporta formato columna(valor) o solo columna
        if '(' in spatial_col and spatial_col.endswith(')'):
            col_name = spatial_col.split('(')[0]
            valores = spatial_col[spatial_col.find('(')+1:-1].split(',')
            col_name = col_name.strip()
            valores = [v.strip() for v in valores]
            if col_name in df.columns:
                # logger.info(f"Columna espacial '{col_name}' encontrada para '{spatial_key}' en el CSV")
                # Verifica que todos los valores existan en la columna
                missing = [v for v in valores if v not in df[col_name].astype(str).unique()]
                if not missing:
                    # logger.info(f"Todos los valores {valores} existen en la columna '{col_name}' para '{spatial_key}'")
                    return True
                else:
                    if len(missing)==len(valores):
                        logger.error(f"Todos los valores {valores} faltan en la columna '{col_name}' para '{spatial_key}'")
                        return False
                    else:
                        logger.warning(f"Faltan algunos valores {missing} en la columna '{col_name}' para '{spatial_key}'")
                        return True
            else:
                logger.warning(f"Columna '{col_name}' para '{spatial_key}' NO encontrada en el CSV")
                return False
        else:
            if spatial_col in df.columns:
                # logger.info(f"Variable espacial '{spatial_key}' encontrada como columna '{spatial_col}' en el CSV")
                return True
            else:
                logger.warning(f"Variable espacial '{spatial_key}' ('{spatial_col}') NO encontrada en el CSV")
                return False

    def verificar_jerarquia_espacial(spatial_results, logger, jerarquia=['Country', 'State', 'City']):
        """
        La jerarquía solo es válida si los True son consecutivos desde el inicio y no hay un True después de un False.
        Debe haber al menos un True.
        """
        estados = [spatial_results.get(nivel, False) for nivel in jerarquia]
        if not any(estados):
            logger.warning("No hay ningún nivel espacial presente en la jerarquía.")
            logger.warning("La jerarquía espacial Country > State > City NO se cumple completamente.")
            return False
        # No puede haber True después de un False
        encontrado_false = False
        for idx, estado in enumerate(estados):
            if not estado:
                encontrado_false = True
            elif estado and encontrado_false:
                logger.warning(f"La jerarquía espacial se rompe en el nivel '{jerarquia[idx]}': hay un True después de un False.")
                logger.warning("La jerarquía espacial Country > State > City NO se cumple completamente.")
                return False
        # logger.info("Jerarquía espacial Country > State > City verificada correctamente.")
        return True

    def verificar_variable_interes(df, interest_vars, logger):
        """
        Verifica que todas las variables de interés existan como columnas en el DataFrame.
        interest_vars puede ser un dict o lista de nombres de columnas.
        """
        if isinstance(interest_vars, dict):
            variables = list(interest_vars.values())
        elif isinstance(interest_vars, list):
            variables = interest_vars
        else:
            logger.warning("El formato de interest_vars no es válido. Debe ser dict o list.")
            return False

        missing = [var for var in variables if var not in df.columns]
        if not missing:
            # logger.info(f"Todas las variables de interés {variables} existen en el dataset.")
            return True
        else:
            logger.warning(f"Faltan variables de interés en el dataset: {missing}")
            return False
