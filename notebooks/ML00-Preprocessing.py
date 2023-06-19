# Databricks notebook source
import pandas as pd
import numpy as np
import re

# COMMAND ----------

catalog_name = "spyros_cavadias"
schema_name = "bronze"
table_name = "laptop_prices_euro"

sdf_raw = spark.read.table(f"{catalog_name}.{schema_name}.{table_name}")

# COMMAND ----------

# What are the attributes?
sdf_raw.printSchema()
# Let's have a look at the first couple of records
sdf_raw.limit(5).display()

# COMMAND ----------

#check if all id unique. 
sdf_raw.select("laptop_ID").distinct().count() == sdf_raw.count()
#print n_rows
print(f"n_rows in dataset: {sdf_raw.count()}")

# COMMAND ----------

# Dataset is pretty small, switching to Pandas
df = sdf_raw.toPandas()
df["Price_euros"] = df["Price_euros"].astype('float')

# COMMAND ----------

#obtain statistics for nominal features
df.describe(include=['object'])

# COMMAND ----------

#round down the screen sizes
df['screen_size_norm']=df['Inches'].astype('float').astype('int64')

# COMMAND ----------

# extract pixels
df['pixels']  = df['ScreenResolution'].str.extract(r'(\d+x\d+)')
df[['x_pixels', 'y_pixels']] = df['pixels'].str.extract(r'(\d+)x(\d+)')
# screen resolution in total_pixels
df['x_pixels'] = df['x_pixels'].astype('int64')
df['y_pixels'] = df['y_pixels'].astype('int64')
df['total_pixels'] = df['x_pixels'] * df['y_pixels']

#cleanup temp columns
df.drop(columns=['x_pixels','y_pixels', 'pixels'], inplace = True)

# COMMAND ----------

# extract op system
df['OpSys'] = df['OpSys'].apply(str.lower)
df['operating_system'] = df['OpSys'].str.extract(r'(windows|mac|no os|linux)', flags=re.IGNORECASE)
# fillna with other os
df['operating_system'].fillna(value="other", inplace=True)

# COMMAND ----------

# extract ram size
df['ram_size']  = df['Ram'].str.extract(r'(\d+)GB').astype('int64')

# extract weight
df['weight_kg']  = df['Weight'].str.replace("kg", "").astype(float)

# extract Memory type
df['memory_tmp'] = df['Memory'].str.replace('Flash Storage', 'SSD')
df['memory_type'] = df['memory_tmp'].str.extract(r'(SSD|HDD)', flags=re.IGNORECASE)
# if memory_tmp contains Hybrid then hybrid
df['memory_type'] = df['memory_type'].where(~df['memory_tmp'].str.contains('Hybrid'), 'Hybrid').apply(str.lower)

# Extract memory size and convert TB to GB
df[['memorysize1', "memorysize2"]] =  df['memory_tmp'].str.extract(r'(\d+(\.\d+)?)').astype(float)
df.loc[df['memorysize1'].isna(), 'memorysize1'] = 0 # these are for hybrid options
df.loc[df['memorysize2'].isna(), 'memorysize2'] = 0 # these are for hybrid options
df.loc[df['memorysize1'] < 10, 'memorysize1'] *= 1024 # TB to GB
df.loc[df['memorysize2'] < 10, 'memorysize2'] *= 1024 # TB to GB
df['memory_size'] = df['memorysize1'] + df['memorysize2']

#cleanup temp columns
df.drop(columns=['memory_tmp','memorysize1', 'memorysize2'], inplace = True)

# COMMAND ----------

# CPU manufacturer
df['cpu_manufacturer'] = df['Cpu'].apply(str.lower).str.extract(r'(intel|amd)', flags=re.IGNORECASE)
# fillna with other os
df['cpu_manufacturer'].fillna(value="other", inplace=True)

# CPU clock spead
df['cpu_clock_spead'] = df['Cpu'].apply(str.lower).str.extract(r'(\d+\.\d+)ghz').astype('float')
df['cpu_clock_spead_tmp'] = df['Cpu'].apply(str.lower).str.extract(r'(\d+)ghz').astype('float')
df['cpu_clock_spead'] = np.where(df['cpu_clock_spead'].isna(), df['cpu_clock_spead_tmp'], df['cpu_clock_spead'])
df.drop(columns=["cpu_clock_spead_tmp"], inplace = True)


# GPU manufacturer
df['gpu_manufacturer'] = df['Gpu'].apply(str.lower).str.extract(r'(intel|nvidia|amd)', flags=re.IGNORECASE)
# fillna with other os
df['gpu_manufacturer'].fillna(value="other", inplace=True)

# COMMAND ----------

# pick features
columns = ["Company", "TypeName", "screen_size_norm", "total_pixels", "operating_system", "ram_size", "weight_kg", "memory_type", "memory_size", "cpu_manufacturer", "cpu_clock_spead", "gpu_manufacturer", "Price_euros"]
features_df = df[columns]

# COMMAND ----------

features_sdf =spark.createDataFrame(features_df) 
features_sdf.printSchema()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS spyros_cavadias.silver

# COMMAND ----------

target_schema_name = "silver"
target_table_name = "features"

features_sdf.write.format("delta").mode("overwrite").saveAsTable(f"{catalog_name}.{target_schema_name}.{target_table_name}")

# COMMAND ----------


