#World life Expectancy Data Cleaning
SELECT *
FROM world_life_expectancy
;


SELECT Country,Year,CONCAT(Country,Year),COUNT(CONCAT(Country,Year))
FROM world_life_expectancy
GROUP BY Country,Year,CONCAT(Country,Year)
HAVING Count(CONCAT(Country,Year)) > 1
;

SELECT *
FROM 
(

SELECT Row_ID, CONCAT(Country,Year),
ROW_NUMBER() OVER(PARTITION BY CONCAT(Country,Year) ORDER BY CONCAT(Country,Year)) AS Row_Num
FROM world_life_expectancy ) AS Row_table
WHERE Row_Num > 1
;

DELETE FROM world_life_expectancy
WHERE 
   Row_ID IN
   (
SELECT Row_ID 
FROM 
(

SELECT Row_ID, CONCAT(Country,Year),
ROW_NUMBER() OVER(PARTITION BY CONCAT(Country,Year) ORDER BY CONCAT(Country,Year)) AS Row_Num
FROM world_life_expectancy ) AS Row_table
WHERE Row_Num > 1
)
;

SELECT *
FROM world_life_expectancy 
;

SELECT*
FROM world_life_expectancy
WHERE status = ''
;

SELECT DISTINCT(Status)
FROM world_life_expectancy
WHERE Status <> ''
;

SELECT DISTINCT(Country)
FROM world_life_expectancy
WHERE Status = 'Developing'
;

UPDATE world_life_expectancy
SET Status='Developing'
WHERE Country IN (
    SELECT DISTINCT(Country)
FROM world_life_expectancy
WHERE Status = 'Developing'
)
;

UPDATE world_life_expectancy t1
JOIN world_life_expectancy t2
    ON t1.Country=t2.Country
SET t1.Status = 'Developing'
WHERE t1.Status=''
AND t2.Status<> ''
AND t2.Status ='Developing'
;    


UPDATE world_life_expectancy t1
JOIN world_life_expectancy t2
    ON t1.Country=t2.Country
SET t1.Status = 'Developed'
WHERE t1.Status=''
AND t2.Status<> ''
AND t2.Status ='Developed'
;    

SELECT *
FROM world_life_expectancy
;


SELECT t1.`life expectancy`, t1.Year, t1.Country, 
       t2.`life expectancy` AS t2_LifeExpectancy, t2.Country AS t2_Country, t2.Year AS t2_Year, 
       t3.Year AS t3_Year, t3.Country AS t3_Country, t3.`life expectancy` AS t3_LifeExpectancy
FROM world_life_expectancy t1
JOIN world_life_expectancy t2 
       ON t1.Country = t2.Country
       AND t1.Year = t2.Year - 1
JOIN world_life_expectancy t3
       ON t1.Country = t3.Country
       AND t1.Year = t3.Year + 1
WHERE t1.`life expectancy` = '';


SELECT t1.`life expectancy`, t1.Year, t1.Country, 
       t2.`life expectancy` AS t2_LifeExpectancy, t2.Country AS t2_Country, t2.Year AS t2_Year, 
       t3.Year AS t3_Year, t3.Country AS t3_Country, t3.`life expectancy` AS t3_LifeExpectancy,
       ROUND((t2.`life expectancy` + t3.`life expectancy`) / 2, 1) AS Average_Life_Expectancy
FROM world_life_expectancy t1
JOIN world_life_expectancy t2 
       ON t1.Country = t2.Country
       AND t1.Year = t2.Year - 1
JOIN world_life_expectancy t3
       ON t1.Country = t3.Country
       AND t1.Year = t3.Year + 1
WHERE t1.`life expectancy` = '';


UPDATE world_life_expectancy t1
JOIN world_life_expectancy t2
   ON t1.Country = t2.Country
   AND t1.Year = t2.Year + 1
JOIN world_life_expectancy t3
   ON t1.Country = t3.Country
   AND t1.Year = t3.Year - 1
SET t1.`Life expectancy` = ROUND((t2.`life expectancy` + t3.`life expectancy`) / 2, 1) 
WHERE t1.`Life expectancy` = '';



#which country done good for increasing life expectancy
SELECT Country,MIN(`life expectancy`), MAX(`life expectancy`)
FROM world_life_expectancy
group by Country
ORDER BY Country DESC
;


SELECT Country,MIN(`life expectancy`), MAX(`life expectancy`)
FROM world_life_expectancy
group by Country
HAVING MIN(`life expectancy`) <> 0
AND  MAX(`life expectancy`) <> 0
ORDER BY Country DESC
;

SELECT 
    Country,
    MIN(`life expectancy`) AS Min_Life_Expectancy,
    MAX(`life expectancy`) AS Max_Life_Expectancy,
    ROUND(MAX(`life expectancy`) - MIN(`life expectancy`), 0) AS Life_Increase_In_15_Years
FROM 
    world_life_expectancy
GROUP BY 
    Country
HAVING 
    MIN(`life expectancy`) <> 0
    AND MAX(`life expectancy`) <> 0
ORDER BY 
    Country DESC;

SELECT year,ROUND(AVG(`life expectancy`),2)
FROM world_life_expectancy
GROUP BY(Year)
ORDER BY (Year)
;

SELECT year,ROUND(AVG(`life expectancy`),2)
FROM world_life_expectancy
WHERE 
    `life expectancy` <> 0
    AND `life expectancy` <> 0
GROUP BY(Year)
ORDER BY (Year)
;


#FINDING THE CORRELATION BETWEEN LIFE EXPECTANCY AND ALL OTHER COLUMNS


SELECT 
    Country,
    ROUND(AVG(`life expectancy`), 1) AS LIFE_EXP, 
    ROUND(AVG(GDP), 1) AS GDP
FROM 
    world_life_expectancy
GROUP BY 
    Country
HAVING 
    LIFE_EXP > 0
    AND GDP > 0
ORDER BY 
    LIFE_EXP;

SELECT 
    Country,
    ROUND(AVG(`life expectancy`), 1) AS LIFE_EXP, 
    ROUND(AVG(GDP), 1) AS GDP
FROM 
    world_life_expectancy
GROUP BY 
    Country
HAVING 
    LIFE_EXP > 0
    AND GDP > 0
ORDER BY 
    GDP;

#TO MAKE THE POSITIVE CORRELATION- DATA VISUALIZATION-SCATTER PLOT

SELECT 
    SUM(CASE WHEN GDP>=1500 THEN 1 ELSE 0 END) HIGH_GDP_COUNT
 FROM world_life_expectancy
 ;

SELECT 
    SUM(CASE WHEN GDP>=1500 THEN 1 ELSE 0 END) HIGH_GDP_COUNT,
    AVG(CASE WHEN GDP>=1500 THEN `life expectancy` ELSE NULL END) HIGH_GDP_LIFE_EXP
 FROM world_life_expectancy;
SELECT 
    SUM(CASE WHEN GDP>=1500 THEN 1 ELSE 0 END) HIGH_GDP_COUNT,
    AVG(CASE WHEN GDP>=1500 THEN `life expectancy` ELSE NULL END) HIGH_GDP_LIFE_EXP,
     SUM(CASE WHEN GDP<=1500 THEN 1 ELSE 0 END) LOW_GDP_COUNT,
    AVG(CASE WHEN GDP<=1500 THEN `life expectancy` ELSE NULL END) LOW_GDP_LIFE_EXP
 FROM world_life_expectancy;
 
 SELECT Status,ROUND(AVG(`life expectancy`),1)
 FROM world_life_expectancy
 GROUP BY Status
 ;
 
  SELECT Status,COUNT(DISTINCT Country)
 FROM world_life_expectancy
 GROUP BY Status
 ;
 SELECT Country,ROUND(AVG(`life expectancy`),1) AS LIFE_EXP,ROUND(AVG(BMI),1) AS BMI
 FROM world_life_expectancy
 GROUP BY Country
 HAVING LIFE_EXP > 0
 AND BMI > 0
 ORDER BY BMI ASC
 ;
  SELECT Country,ROUND(AVG(`life expectancy`),1) AS LIFE_EXP,ROUND(AVG(BMI),1) AS BMI
 FROM world_life_expectancy
 GROUP BY Country
 HAVING LIFE_EXP > 0
 AND BMI > 0
 ORDER BY BMI DESC
 ;
 

 ;
 
 SELECT 
    Country,
    Year,
    `life expectancy`,
    `adult mortality`,
    SUM(`adult mortality`) OVER(PARTITION BY Country ORDER BY Year) AS ROLLING_TOTAL
FROM 
    world_life_expectancy
WHERE 
    Country LIKE '%United%'
ORDER BY 
    Year;
 
 
 