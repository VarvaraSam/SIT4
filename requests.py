import sqlite3
import pandas as pd


con = sqlite3.connect("farmassoc.sqlite")
cursor = con.cursor()
# Выводит фермы, которые выращивают заданные продукты, с сортировкой названий ферм по алфавиту
products = ("Лук", "Рожь")
df = pd.read_sql(f'''
 SELECT
 product_id,
 product_name,
 farm_id,
 farm_name
 FROM farm_has_product
 JOIN product USING (product_id)
 JOIN farm USING (farm_id)
 WHERE product_name IN {products}
 ORDER BY farm_name
''', con)
print(df)
# #Выводит какие продукты и сколько будут выращиваться в заданные год по увеличению колличества
year = 2021
df = pd.read_sql(f'''
 SELECT
 product_name,
 product_amount
 FROM product_has_plan
 JOIN product USING (product_id)
 JOIN plan USING (plan_id)
 WHERE year = {year}
 ORDER BY product_amount DESC
''', con)
print(df)
#Выводит сколько видов разных продуктов выращивают фермы

df = pd.read_sql(f'''
 SELECT
 farm_name,
 COUNT(product_id)
 FROM farm
 JOIN farm_has_product USING (farm_id)
 GROUP BY farm_name
''', con)
print(df)
#Выводит сколько всего посевных площадей использовалось в конкретный год
df = pd.read_sql(f'''
 SELECT
 year,
 SUM(cultivated_areas_amount)
 FROM task_for_farm
 GROUP BY year
''', con)
print(df)
#Выводит все продукты, которых нет в плане на заданный год
year = 2020
df = pd.read_sql(f'''
 SELECT
 product_name
 FROM product
 WHERE product_id NOT IN
 (SELECT product_id
 FROM product_has_plan
 JOIN plan USING (plan_id)
 WHERE year = {year}
 )
''', con)
print(df)

#Выводит все продукты, которые никто не выращивает
year = 2020
df = pd.read_sql(f'''
 SELECT
 product_name
 FROM product
 WHERE product_id NOT IN
 (SELECT product_id
 FROM farm_has_product
 )
''', con)
print(df)
#Удаляет номер телефона по id фермы
farm_id = 1
con.executescript(f'''
 UPDATE farm
 SET tel = NULL
 WHERE farm_id = {farm_id}
''')
con.commit()

#Удаляет все продукты, которые никто не выращивает
con.executescript(f'''
 DELETE FROM product
 WHERE product_id IN
 (SELECT
 product_id
 FROM product
 WHERE product_id NOT IN
 (SELECT product_id
 FROM farm_has_product
 )
 )
''')
con.commit()
con.close()
