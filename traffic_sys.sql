/* ===============================
   STEP 0: USE DATABASE
================================ */
USE smart_traffic;


/* ===============================
   STEP 1: CITIES TABLE
================================ */
CREATE TABLE IF NOT EXISTS cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE NOT NULL
);


/* ===============================
   STEP 2: INSERT REQUIRED CITIES
================================ */
INSERT IGNORE INTO cities (city_name) VALUES
('New Delhi'),
('Gurgaon'),
('Noida'),
('Ghaziabad'),
('Faridabad'),
('Bahadurgarh'),
('Nagpur');


/* ===============================
   STEP 3: ENSURE ROADS HAS city_id
================================ */
ALTER TABLE roads
ADD COLUMN IF NOT EXISTS city_id INT NULL;


/* ===============================
   STEP 4: AUTO MAP city_id USING
           LATITUDE + LONGITUDE
================================ */
UPDATE roads r
JOIN cities c
SET r.city_id =
CASE
    /* -------- NEW DELHI -------- */
    WHEN r.latitude BETWEEN 28.45 AND 28.90
     AND r.longitude BETWEEN 76.80 AND 77.40
     AND c.city_name = 'New Delhi'
    THEN c.city_id

    /* -------- GURGAON -------- */
    WHEN r.latitude BETWEEN 28.38 AND 28.55
     AND r.longitude BETWEEN 76.95 AND 77.15
     AND c.city_name = 'Gurgaon'
    THEN c.city_id

    /* -------- NOIDA -------- */
    WHEN r.latitude BETWEEN 28.50 AND 28.65
     AND r.longitude BETWEEN 77.30 AND 77.45
     AND c.city_name = 'Noida'
    THEN c.city_id

    /* -------- GHAZIABAD -------- */
    WHEN r.latitude BETWEEN 28.65 AND 28.75
     AND r.longitude BETWEEN 77.35 AND 77.55
     AND c.city_name = 'Ghaziabad'
    THEN c.city_id

    /* -------- FARIDABAD -------- */
    WHEN r.latitude BETWEEN 28.30 AND 28.45
     AND r.longitude BETWEEN 77.25 AND 77.40
     AND c.city_name = 'Faridabad'
    THEN c.city_id

    /* -------- BAHADURGARH -------- */
    WHEN r.latitude BETWEEN 28.65 AND 28.75
     AND r.longitude BETWEEN 76.85 AND 76.98
     AND c.city_name = 'Bahadurgarh'
    THEN c.city_id

    /* -------- NAGPUR -------- */
    WHEN r.latitude BETWEEN 21.05 AND 21.25
     AND r.longitude BETWEEN 79.00 AND 79.20
     AND c.city_name = 'Nagpur'
    THEN c.city_id

    ELSE r.city_id
END
WHERE r.city_id IS NULL;


/* ===============================
   STEP 5: SYNC city NAME COLUMN
================================ */
UPDATE roads r
JOIN cities c ON r.city_id = c.city_id
SET r.city = c.city_name
WHERE r.city IS NULL OR r.city = '';


/* ===============================
   STEP 6: VERIFICATION QUERIES
   (RUN TO CONFIRM SUCCESS)
================================ */

-- City-wise route count
SELECT city, COUNT(*) AS total_locations
FROM roads
GROUP BY city
ORDER BY total_locations DESC;

-- Any unmapped road? (should be ZERO rows)
SELECT road_id, road_name, latitude, longitude
FROM roads
WHERE city_id IS NULL;
