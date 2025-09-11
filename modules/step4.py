import streamlit as st
import time

def show(proyecto):
    """Step 4: Taxonomy Queries"""
    st.header("📈 Step 4: Taxonomy Queries")

    st.markdown("""
    The entities generated in the previous step are imported into Atlas and the content is explored. 
    Once the RPCM entities and instances have been ingested into Apache Atlas, you can explore them through queries.
    """)
    if proyecto == "Student Performance Analysis":
        show_all_queries_student_project()
    elif proyecto == "Retail Data Analytics":
        show_all_queries_retail_project()



def show_all_queries_student_project():
    """Display all queries as tabs"""
    
    # All queries in one list
    all_queries = [
        {
            "name": "Project Overview",
            "query": """from Project 
select qualifiedName, keywords, name""",
            "result": """qualifiedName = "student-performance-analysis@StudentPerformanceAn"
keywords = []
name = "Student Performance Analysis" """
        },
        {
            "name": "Project Creator",
            "query": """from Project 
select createdBy""",
            "result": """createdBy = "joelknapp" """
        },
        {
            "name": "Action Execution Details", 
            "query": """from Action 
where name = "Action - Notebook - Student Performance Analysis"
select qualifiedName, inputData, outputData, status""",
            "result": """qualifiedName = "notebook-student-performance-analysis.ipynb-v1@StudentPerformanceAn"
status = "Completed"
inputData = "Analysis of 1 datasets: Student_performance_data _.csv"
outputData = "Generated 16 outputs including models and visualizations" """
        },
        {
            "name": "Experiment Stages",
            "query": """from Experiment 
select name, stages""",
            "result": """name = "Student Performance Analysis"
stages = "stage@StudentPerformanceAn" """
        },
        {
            "name": "Input Datasets",
            "query": """from UsedData 
where format = "csv" 
select name, size, document""",
            "result": """name = "Dataset 1: Student_performance_data _.csv (Quality Verified - Original CSV)"
size = 166901
document = "Student_performance_data _.csv" """
        },
        {
            "name": "Generated Models",
            "query": """from UsedData 
where format = "pickle" 
select name""",
            "result": """Found 9 models:
- Model: SVC
- Model: RandomForestClassifier  
- Model: AdaBoostClassifier
- Model: KNeighborsClassifier
- Model: CatBoostClassifier
- Model: XGBClassifier
- Model: GradientBoostingClassifier
- Model: LGBMClassifier
- Model: DecisionTreeClassifier """
        },
        {
            "name": "Visualization Artifacts",
            "query": """from UsedData 
where format = "png" 
select name""",
            "result": """Found 5 charts:
- Chart: Figure 1 - KNeighborsClassifier - Correlation Among Features
- Chart: Figure 2 - KNeighborsClassifier - Selecting a Classification Model  
- Chart: Figure 3 - KNeighborsClassifier - Model Evaluation
- Chart: Figure 4 - SVC - Model Evaluation (again)
- Chart: Figure 5 - GradientBoostingClassifier - Reducing Dimensionality """
        },
        {
            "name": "Project Validation Status",
            "query": """from Consensus 
select typeConsensus, result, agreementLevel""",
            "result": """typeConsensus = "Individual Review"
result = "approved"
agreementLevel = 100 """
        },
        {
            "name": "Data Quality Assessment",
            "query": """from UsedData 
where name contains "Dataset"
select qualityScore, qualityStatus""",
            "result": """qualityScore = 100.0
qualityStatus = "Verified" """
        }
    ]
    
    # Create tabs for all queries
    tab_names = [query["name"] for query in all_queries]
    tabs = st.tabs(tab_names)
    
    for i, query_info in enumerate(all_queries):
        with tabs[i]:
            show_query_tab(query_info, i)





def show_all_queries_retail_project():
    """Display all queries for Retail Data Analytics as tabs"""
    
    # All queries in one list
    all_queries = [
        {
            "name": "Project Overview",
            "query": """from Project 
select qualifiedName, keywords""",
            "result": """qualifiedName = "retail-data-analytics@RetailDataAnalytics"
keywords = ["data analytics", "retail", "business intelligence"]"""
        },
        {
            "name": "Project Creator",
            "query": """from Project 
select createdBy""",
            "result": """createdBy = "manjeetsingh" """
        },
        {
            "name": "Action Execution Details", 
            "query": """from Action 
where name = "Action - Notebook - Retail Data Analytics"
select qualifiedName, inputData, outputData, status""",
            "result": """qualifiedName = "Action - Notebook - Retail Data Analytics"
status = "Completed"
inputData = "Analysis of retail dataset: retaildataset.csv"
outputData = "Generated 6 outputs including cleaned data and visualizations" """
        },
        {
            "name": "Experiment Stages",
            "query": """from Experiment 
select stages""",
            "result": """name = "stage@RetailDataAnalytics" """
        },
        {
            "name": "Input Datasets",
            "query": """from UsedData 
where format = "csv" 
select name, size""",
            "result": """document = ["retaildataset.csv"]
size = [45621]"""
        },
        {
            "name": "Visualization Artifacts",
            "query": """from UsedData 
where format = "png" 
select name""",
            "result": """- Chart: Figure 1 - Sales Distribution Analysis
- Chart: Figure 2 - Customer Segmentation Overview  
- Chart: Figure 3 - Product Category Performance
- Chart: Figure 4 - Seasonal Trends Analysis
- Chart: Figure 5 - Revenue by Region Heatmap"""
        },
        {
            "name": "Project Validation Status",
            "query": """from Consensus 
select typeConsensus, result""",
            "result": """typeConsensus = "Individual Review"
result = "approved" """
        },
        {
            "name": "Approved Actions",
            "query": """from Consensus 
where result = "approved" 
select action""",
            "result": """action.name = "Action - Notebook - Retail Data Analytics" """
        }
    ]
    
    # Create tabs for all queries
    tab_names = [query["name"] for query in all_queries]
    tabs = st.tabs(tab_names)
    
    for i, query_info in enumerate(all_queries):
        with tabs[i]:
            show_query_tab(query_info, i)


def show_query_tab(query_info, index):
    """Display individual query tab"""
    
    st.markdown(f"**{query_info['name']}**")
    
    # Query display
    st.markdown("**🔍 Query:**")
    st.code(query_info["query"], language="sql")
    
    
    # Results display
    st.markdown("**📊 Expected Results:**")
    st.code(query_info["result"], language="text")