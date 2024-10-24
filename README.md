# brick-by-brick
Repository for the D ONE databricks brick-by-brick workshop

# Content
0. Setup Workspace
    * Adding the repository
    * Create a personal cluster

1. Delta + Unity Catalog
   * Read and Write Tables
   * Upload data to Unity Catalog
   * Time Travel + Installing Libraries

2. Medallion Architecture & Workflow Orchestration
   * 3 Notebooks - Medallion architecture 
   * Creating a Workflow Job

3. ML and MLOps


# 0. Setup Workspace
Login to the [workspace](https://adb-1353574989447196.16.azuredatabricks.net/?o=1353574989447196).

## Adding the repository
Adding the repository to your workspace: 
1. Click on `Workspace` in the navigation menu to the left.
2. Click on the directory `Home`.
3. Click on `Create` and choose `Git folder` and paste this [URL](https://github.com/d-one/brick-by-brick-six-swiss-exchange.git) into `Git repository` 
4. Click on `Create Git folder` 

Now you should see a repository named `brick-by-brick` under your own directory.

## Create a personal cluster to your workspace.
1. Click on the `Compute` tab in the navigation menu to the left.
2. Click on `Create compute` and choose the following settings:
3. Choose the `Personal Copmute` Policy
3. Make sure the `Single user access` is under your user
4. Click on `Create Compute`

# 1. Three Notebooks - the medallion architecture
Go to the following notebooks and follow the instructions:
1. `Bronze`. 
2. `Silver` 
3. `Gold`

# 2. Creating a Workflow Job
1. Click on the `Workflows` tab in the navigation menu to the left.
2. Click on the `Create job` button.
3. Add a Job name for your Workflow at the top: `bricks-<firstname_lastname>`.
3. Choose the following settings
   * **Task Name**: `bronze_task`
   * **Source**: `Workspace`
   * **Path**: Click on `Select Notebook` and choose your Bronze Notebook
   * **Cluster**: Choose your existing cluster that you created in your first exercise. 
4. Click on `Create`
   * Now you have created a workflow Job with one task inside.
5. Click on `Add task` and choose `Notebook`
6. Repeat the steps for both the `silver_task`and `gold_task`. 
   * Make sure that they are dependent on each other in the following order *bronze_task -> silver_task -> gold_task*
7. Click on `Run now` to run the whole Job.

Congratulations, you have now created a workflow Job.


# 3. ML and MLOps

1. Run the ML Preprocessing notebook in your catalog to create the feature table.
2. Move on to the ML MLflow Tracking notebook and walk through the steps to understand how to interact with MLflow experiments inside the Databricks workspace.
3. Move on to the ML Model Registry notebook and walk through the steps to understand how to interact with the model registry via python APIs or via the directly using the UI
4. (Optional)Tie steps 1-3 together by creating a new ML workflow! See the results of the workflow run in the UI.
5. (Optional)Finally move on to the AutoML notebook and see for yourself how easy it is to use databricks AutoML as a quick way to create baseline models.
  

Excellent, you have now mastered MLflow on Databricks and you are ready to apply these principals to your own project.


