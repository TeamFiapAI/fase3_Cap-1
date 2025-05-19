SELECT 
    Produtor.id_Produtor, 
    Produtor.nome AS PRODUTOR,
    Fazenda.nome AS FAZENDA,
    Cultura.nome_cultura,
    Sensor.id_sensor, 
    Sensor.modelo,
    TipoSensor.nome_tipo,
    (
        SELECT COUNT(*) 
        FROM LeituraSensor LS 
        WHERE LS.id_sensor = Sensor.id_sensor
    ) AS total_leituras
FROM
    Produtor
LEFT JOIN Produtorfazenda
    ON Produtor.id_produtor = Produtorfazenda.id_produtor
LEFT JOIN Fazenda
    ON Fazenda.id_fazenda = Produtorfazenda.id_fazenda
LEFT JOIN Plantacao
    ON Plantacao.id_fazenda = Fazenda.id_fazenda
LEFT JOIN Cultura
    ON Cultura.id_cultura = Plantacao.id_cultura
LEFT JOIN Sensor
    ON Sensor.id_plantacao = Plantacao.id_plantacao
LEFT JOIN TipoSensor
    ON TipoSensor.id_tipo_sensor = Sensor.id_tipo_sensor
ORDER BY 
    PRODUTOR;