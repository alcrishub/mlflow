import openai
import pandas as pd

import mlflow

eval_df = pd.DataFrame(
    {
        "inputs": [
            "What is MLflow?",
            "What is Spark?",
            "What is Python?",
        ],
        "ground_truth": [
            "MLflow is an open-source platform for managing the end-to-end machine learning (ML) lifecycle. It was developed by Databricks, a company that specializes in big data and machine learning solutions. MLflow is designed to address the challenges that data scientists and machine learning engineers face when developing, training, and deploying machine learning models.",
            "Apache Spark is an open-source, distributed computing system designed for big data processing and analytics. It was developed in response to limitations of the Hadoop MapReduce computing model, offering improvements in speed and ease of use. Spark provides libraries for various tasks such as data ingestion, processing, and analysis through its components like Spark SQL for structured data, Spark Streaming for real-time data processing, and MLlib for machine learning tasks",
            "Python is a high-level programming language that was created by Guido van Rossum and released in 1991. It emphasizes code readability and allows developers to express concepts in fewer lines of code than languages like C++ or Java. Python is used in various domains, including web development, scientific computing, data analysis, and machine learning.",
        ],
    }
)

with mlflow.start_run() as run:
    system_prompt = "Answer the following question in two sentences"
    logged_model = mlflow.openai.log_model(
        model="gpt-3.5-turbo",
        task=openai.ChatCompletion,
        artifact_path="model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "{question}"},
        ],
    )

    results = mlflow.evaluate(
        logged_model.model_uri,
        eval_df,
        targets="ground_truth",
        model_type="question-answering",
        evaluators="default",
    )
    print(results.metrics)

    eval_table = results.table["eval_results_table"]
    print(eval_table)
