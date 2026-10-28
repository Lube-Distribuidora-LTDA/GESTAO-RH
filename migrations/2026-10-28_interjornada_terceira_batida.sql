-- APLICADA em 2026-10-28 no projeto jhznrwmwszpfogvbjnjx.
-- O Relatório de Jornada do PontoMais traz a 3ª entrada/saída quando alguém bate o ponto
-- seis vezes no dia. Sem estas colunas a última saída do dia se perdia e o descanso entre
-- jornadas era medido a partir da 2ª saída.
ALTER TABLE public.interjornada_registros ADD COLUMN IF NOT EXISTS entrada3 TEXT;
ALTER TABLE public.interjornada_registros ADD COLUMN IF NOT EXISTS saida3 TEXT;
