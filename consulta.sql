SELECT 
       T.estoque AS "Estoque",
       SUM(T.estoque) OVER (PARTITION BY Z.codigo, A.produtoid, J.caminho) AS "QTDE ESTOQUE",
       Z.codigo AS "FILIAL SB",
       A.id AS "Embalagemid",
       A.produtoid AS "Produtoid",
       B.status AS "Status",
       B.descricao AS "Descricao",
       COALESCE(A.codigobarras, 'P' || CAST(A.produtoid AS VARCHAR)) AS "Codbarras",
       CASE
           -- Caso haja dois ou mais ">"
           WHEN position('>' IN substring(J.caminho from position('>' IN J.caminho) + 1)) > 0 THEN 
               trim(substring(J.caminho from position('>' IN J.caminho) + 2 
                              FOR position('>' IN substring(J.caminho from position('>' IN J.caminho) + 1)) - 2))
           -- Caso haja apenas um ">"
           ELSE trim(substring(J.caminho from position('>' IN J.caminho) + 2))
       END AS "Grupo Principal",
       E.nome AS "Nome",
       A.precovenda AS "Precovenda", 
       B.codigo AS "Codigo Produto",  
       L.nome AS "Curvavalor", 
       M.nome AS "Curvaquantidade",  
       H.customedio AS "Customedio",
       (H.customedio * SUM(T.estoque) OVER (PARTITION BY Z.codigo, A.produtoid, J.caminho)) AS "VALOR ESTOQUE"
FROM estoque T 
INNER JOIN embalagem A ON T.embalagemid = A.id
INNER JOIN unidadenegocio Z ON T.unidadenegocioid = Z.id  
INNER JOIN produto B ON A.produtoid = B.id
INNER JOIN fabricante D ON B.fabricanteid = D.id
INNER JOIN pessoa E ON D.pessoaid = E.id
INNER JOIN custoproduto H ON A.produtoid = H.produtoid AND T.unidadenegocioid = H.unidadenegocioid
INNER JOIN classificacaoproduto N ON A.produtoid = N.produtoid
INNER JOIN classificacao J ON N.classificacaoid = J.id  
LEFT JOIN curvaabcprodutounidadenegocio K ON K.produtoid = A.produtoid AND K.unidadenegocioid = Z.id 
LEFT JOIN curvaabc L ON L.id = K.curvaabcvalorid 
LEFT JOIN curvaabc M ON M.id = K.curvaabcquantidadeid
WHERE (
    CASE
        -- Caso haja dois ou mais ">"
        WHEN position('>' IN substring(J.caminho from position('>' IN J.caminho) + 1)) > 0 THEN 
            trim(substring(J.caminho from position('>' IN J.caminho) + 2 
                           FOR position('>' IN substring(J.caminho from position('>' IN J.caminho) + 1)) - 2))
        -- Caso haja apenas um ">"
        ELSE trim(substring(J.caminho from position('>' IN J.caminho) + 2))
    END
) NOT IN ('FOOD', 'NAO NEGOCIADOS', 'NEGOCIADOS');