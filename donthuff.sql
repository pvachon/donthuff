CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

DROP TABLE IF EXISTS measurements;

CREATE TABLE measurements(
    time TIMESTAMPTZ NOT NULL,
    sensor_id INTEGER,
    temp_celsius FLOAT,
    humidity FLOAT,
    pm_1_0 INTEGER,
    pm_2_5 INTEGER,
    pm_10_0 INTEGER,
    pm_1_0_us_std INTEGER,
    pm_2_5_us_std INTEGER,
    pm_10_0_us_std INTEGER,
    count_gt_0_3_um INTEGER,
    count_gt_0_5_um INTEGER,
    count_gt_1_0_um INTEGER,
    count_gt_2_5_um INTEGER,
    count_gt_5_0_um INTEGER,
    count_gt_10_0_um INTEGER,
    co2_ppm INTEGER,
    formaldehyde FLOAT,
    tvoc FLOAT,
    source_id NOT NULL
);

SELECT create_hypertable('measurements', 'time');

