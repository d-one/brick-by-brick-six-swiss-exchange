# Databricks notebook source
# MAGIC %md
# MAGIC # Read a table from Unity Catalog
# MAGIC Namespace
# MAGIC * Catalog = six_swiss_exchange_catalog
# MAGIC * Schema = deltademo
# MAGIC * Table = churn_modelling

# COMMAND ----------

df = spark.table("six_swiss_exchange_catalog.deltademo.churn_modelling")

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC Using SQL

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM six_swiss_exchange_catalog.deltademo.churn_modelling

# COMMAND ----------

# MAGIC %md
# MAGIC Using embedded SQL

# COMMAND ----------

catalog = "six_swiss_exchange_catalog"
df = spark.sql(f"SELECT * FROM {catalog}.deltademo.churn_modelling")

# COMMAND ----------

# MAGIC %md
# MAGIC # Save and read temporary views

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW temptable_sql 
# MAGIC AS
# MAGIC SELECT * FROM six_swiss_exchange_catalog.deltademo.churn_modelling

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM temptable_sql

# COMMAND ----------

df = spark.table("temptable_sql")
display(df)

# COMMAND ----------

# MAGIC %md 
# MAGIC Use Python to create a temporary view

# COMMAND ----------

df = spark.table("six_swiss_exchange_catalog.deltademo.churn_modelling")
df.createOrReplaceTempView("temptable_python")


# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VIEWS

# COMMAND ----------

# MAGIC %md
# MAGIC # Delta table history
# MAGIC
# MAGIC Here we will write to one of our own tables to inspect the history.
# MAGIC
# MAGIC Make sure you change the `table namepsace` before running the command

# COMMAND ----------

# Lets creata a catalog and a Schema for you inside your own catalog
catalog_name = "<firstname_lastname>" # usr_<firstname>_<lastname>
schema_name = "deltademo"

if not catalog_name:
    dbutils.notebook.exit("Please create/provide a name for your catalog following this naming convention:<firstname>_<lastname>")

spark.sql(
    f"""
    CREATE CATALOG IF NOT EXISTS {catalog_name}
    """
)


spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")

# COMMAND ----------


df = spark.table(f"six_swiss_exchange_catalog.deltademo.churn_modelling")

df.write.format("delta").mode("append").saveAsTable(f"{catalog_name}.{schema_name}.churn_modelling")


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM robert_yousif.deltademo.churn_modelling

# COMMAND ----------


history = spark.sql(f"DESCRIBE HISTORY {catalog_name}.deltademo.churn_modelling")
display(history)

# COMMAND ----------

# Lets write a second time to the table
df.write.format("delta").mode("append").saveAsTable(f"{catalog_name}.{schema_name}.churn_modelling")

# COMMAND ----------

df_v1 = spark.table(f"{catalog_name}.{schema_name}.churn_modelling@v0")
print(df_v1.count())

df_v2 = spark.table(f"{catalog_name}.{schema_name}.churn_modelling@v1")
print(df_v2.count())

# COMMAND ----------

# MAGIC %md 
# MAGIC Using SQL to read an older version

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM robert_yousif.deltademo.churn_modelling VERSION AS OF 2

# COMMAND ----------

# MAGIC %md
# MAGIC ## Show the `Variable Explorer`, `Revision History` & `Python Libraries`

# COMMAND ----------

# MAGIC %md
# MAGIC # Exercises

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 1 

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Download the data from the repository: [churn_modelling](https://github.com/d-one/brick-by-brick/blob/churn_prediction/data/churn_modelling.csv)
# MAGIC 2. Upload the data as a workspace object to your personal directory.
# MAGIC 3. Read the data and display it
# MAGIC 4. Write to your own table inside your own catalog and schema
# MAGIC 5. See what other `DESCRIBE` commands you can run on your table to get more information
# MAGIC 6. Share the table with the person sitting next to you. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Download the data from the repository
# MAGIC Click on this [link](https://github.com/d-one/brick-by-brick/blob/churn_prediction/data/churn_modelling.csv) and download the data directly from github to your local machine. (You will find a `Download Raw File` Button at the top right of the document preview inside gitlab.)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Upload Workspace Objects
# MAGIC
# MAGIC 1. Click on the `Workspace` button in the panel, this will take you to another page (Open it in a new page to keep the intstruction up).
# MAGIC     * `Home`: Private directories for every user.
# MAGIC     * `Workspace`: Shared and Users directories.
# MAGIC     * `Repos`: All repositories.
# MAGIC
# MAGIC 2. Click on the `Workspace` -> `Users` and choose your name, if your name does not exist, create a directory with the email adress you are logged in (see top right of workspace). 
# MAGIC 3. Right click inside your directory and click on `Import`, this will open a new window with the name `Import`
# MAGIC 4. Choose File and either drop a file or browse for it. 
# MAGIC 5. Click on the `Import` button

# COMMAND ----------

# MAGIC %md 
# MAGIC ### 3. Read the data, display it and display the path where it resides
# MAGIC TIP: Use the path `"file:/Workspace/Users/<user_email>/<path-to-file>"`

# COMMAND ----------

path = f"file:/Workspace/Users/{user_email}/churn_modelling.csv"
# <TODO>

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Write to your own table inside your own catalog and the default schema

# COMMAND ----------

table_name = "my_uploaded_churn_modelling_table"
# <TODO>

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. See what other `DESCRIBE` commands you can run on your table to get more information
# MAGIC Hint: `DESCRIBE DETAIL`, `DESCRIBE HISTORY`
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- <TODO>

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6. Share the table with the person sitting next to you so they can read it from your catalog
# MAGIC This can be done either through the GUI or SQL commands such as: 
# MAGIC `GRANT <permission> ON <object> <objectname>` for example `GRANT SELECT ON TABLE sds_catalog.default.churn_modelling`

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Either do it here or in the GUI
# MAGIC -- <TODO>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Solution

# COMMAND ----------

# 3.
# # Make sure you have uploaded the file
# path = f"file:/Workspace/Users/{user_email}/churn_modelling.csv"
# dbutils.fs.ls(path)
# df = spark.read.format("csv").option("header", True).load(path)
# display(df)

# COMMAND ----------

# 4.
# table_name = "my_uploaded_churn_modelling_table"
# df.write.format("delta").saveAsTable(f"{catalog_name}.default.{table_name}")
# display(spark.table(f"{catalog_name}.default.{table_name}"))


# COMMAND ----------

# MAGIC %sql
# MAGIC -- 4.
# MAGIC -- DESCRIBE table EXTENDED panagiotis_goumenakis.default.my_uploaded_churn_modelling_table
# MAGIC -- DESCRIBE DETAIL panagiotis_goumenakis.default.my_uploaded_churn_modelling_table
# MAGIC -- DESCRIBE HISTORY panagiotis_goumenakis.default.my_uploaded_churn_modelling_table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 5.
# MAGIC -- GRANT SELECT on TABLE panagiotis_goumenakis.default.my_uploaded_churn_modelling_table TO `spyros_cavadias@ms.d-one.ai`

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 6.
# MAGIC -- GRANT USAGE ON CATALOG panagiotis_goumenakis TO `spyros.cavadias@ms.d-one.ai`
# MAGIC -- GRANT USAGE ON SCHEMA panagiotis_goumenakis.default TO `spyros.cavadias@ms.d-one.ai`
# MAGIC -- GRANT SELECT on TABLE panagiotis_goumenakis.default.my_uploaded_churn_modelling_table TO `spyros.cavadias@ms.d-one.ai`

# COMMAND ----------

# MAGIC %md 
# MAGIC # Exercise Extended 

# COMMAND ----------

# MAGIC %md
# MAGIC Install a library
# MAGIC * Install a Cluster library
# MAGIC * Install a Notebook-scoped library
# MAGIC
# MAGIC Follow the instructions here: Installing Libraries
# MAGIC
# MAGIC
# MAGIC Check the `Python Libraries` tab on the right panel or run a `pip freeze`

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cluster Library
# MAGIC
# MAGIC A cluster library will be available to all the Notebooks that are connected to that cluster.
# MAGIC
# MAGIC 1. Click compute icon `Compute` in the sidebar.
# MAGIC 2. Click a cluster name.
# MAGIC 3. Click the `Libraries` tab.
# MAGIC 4. Click `Install New`.
# MAGIC 5. Choose one of the `Library Source` buttons
# MAGIC     * You have a few options here i.e. `Upload` or `PyPI`
# MAGIC     * Every time you start the cluster, the libraries will be installed again

# COMMAND ----------

# MAGIC %md
# MAGIC ### Notebook-scoped Libraries
# MAGIC When you install a notebook-scoped library, only the current notebook and any jobs associated with that notebook have access to that library. Other notebooks attached to the same cluster are not affected.
# MAGIC
# MAGIC To install a library in a notebook scoped:
# MAGIC
# MAGIC ```sh
# MAGIC %pip install arrow
# MAGIC ```

# COMMAND ----------

# MAGIC %pip install arrow

# COMMAND ----------

# MAGIC %md
# MAGIC TIP: Try `Detach & re-attach`your cluster and see if the library is still installed
