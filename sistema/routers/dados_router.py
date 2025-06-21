import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from db import conectar

router = APIRouter(prefix="/dados", tags=["Leituras"])


class LeituraInput(BaseModel):
    temperatura: float
    umidade: float
    ph: float
    fosforo: bool
    potassio: bool
    modelo: str


from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from db import conectar
import numpy as np

router = APIRouter(prefix="/dados", tags=["Leituras"])


class LeituraInput(BaseModel):
    temperatura: float
    umidade: float
    ph: float
    fosforo: bool
    potassio: bool
    modelo: str


@router.post("/")
def receber_dados(leitura: LeituraInput, request: Request):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id_sensor, id_tipo_sensor FROM Sensor WHERE modelo = :modelo", {"modelo": leitura.modelo})
        sensores = cursor.fetchall()

        if not sensores:
            raise HTTPException(status_code=404, detail="Sensor com este modelo não encontrado.")

        valores = {
            1: leitura.umidade,
            2: leitura.ph,
            3: leitura.fosforo,
            4: leitura.potassio,
            5: leitura.temperatura
        }

        agora = datetime.now()
        inseridos = 0

        for id_sensor, id_tipo in sensores:
            valor = valores.get(id_tipo)
            if valor is None:
                continue
            if isinstance(valor, bool):
                valor = 1.0 if valor else 0.0

            cursor.execute("""
                INSERT INTO LeituraSensor (id_sensor, data_hora, valor_lido)
                VALUES (:id_sensor, :data_hora, :valor_lido)
            """, {
                "id_sensor": id_sensor,
                "data_hora": agora,
                "valor_lido": valor
            })
            inseridos += 1

        modelo = request.app.state.modelo_irrigacao
        scaler = request.app.state.scaler_irrigacao

        entrada = pd.DataFrame([{
            "temperature": leitura.temperatura,
            "humidity": leitura.umidade,
            "rainfall": 0.0
        }])

        entrada_scaled = scaler.transform(entrada)
        predicao = modelo.predict(entrada_scaled)[0]

        conn.commit()
        return {
            "status": "ok",
            "leituras_inseridas": inseridos,
            "precisa_irrigar": bool(predicao)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

