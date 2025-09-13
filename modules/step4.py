import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import time

def show(proyecto):
    """Step 4: Taxonomy Queries"""
    st.header("📈 Step 4: Taxonomy Queries")

    st.markdown("""
    The entities generated in the previous step are imported into Atlas and the content is explored. 
    Once the RPCM entities and instances have been ingested into Apache Atlas, you can explore them through queries.
    """)

    # Crear tabs principales
    tab1, tab2 = st.tabs(["🌐 Atlas Interface", "🔍 Interactive Query Builder"])
    
    with tab1:
        show_atlas_interface()
    
    with tab2:
        show_interactive_query_builder(proyecto)

def show_atlas_interface():
    """Muestra la interfaz de Atlas embebida"""
    st.subheader("Atlas Web Interface")
    st.markdown("Explore the full Atlas interface with all imported entities:")
    
    # URL del proxy
    proxy_url = "http://localhost:8502"

    # Crear el iframe usando el proxy
    components.iframe(
        src=proxy_url,
        width=1400,
        height=800,
        scrolling=True
    )

def show_interactive_query_builder(proyecto):
    """Constructor interactivo con opciones calculadas"""
    st.subheader("Interactive DSL Query Builder")
    st.markdown("Build queries by selecting from available options in your data:")
    
    # Obtener las opciones disponibles para este proyecto
    query_options = get_query_options(proyecto)
    
    # Selector de tipo de consulta
    query_category = st.selectbox(
        "What do you want to explore?",
        list(query_options.keys())
    )
    
    if query_category:
        build_interactive_query(query_category, query_options[query_category], proyecto)

def get_query_options(proyecto):
    """Retorna opciones de consulta específicas para cada proyecto"""
    
    if proyecto == "retail" or "retail" in proyecto.lower():
        return {
            "Project Information": {
                "entity": "Project",
                "description": "Explore project metadata and details",
                "filters": {
                    "None": {"query_part": "", "description": "Show all project info"},
                },
                "fields": {
                    "Basic Info": ["name", "createdBy"],
                    "Keywords": ["name", "keywords"], 
                    "Timeline": ["name", "startDate", "endDate"],
                    "Complete": ["name", "keywords", "createdBy", "startDate", "endDate"]
                },
                "known_values": {
                    "name": "Retail sales forecast",
                    "createdBy": "aremoto",
                    "keywords": ["data visualization", "finance", "business"]
                }
            },
            "Input Datasets": {
                "entity": "UsedData",
                "description": "Explore input data files and their properties",
                "filters": {
                    "CSV Files Only": {"query_part": "where format = \"csv\"", "description": "Show only CSV datasets"},
                    "Large Files (>1MB)": {"query_part": "where size > 1000000", "description": "Show files larger than 1MB"},
                    "All Data Files": {"query_part": "", "description": "Show all data files"}
                },
                "fields": {
                    "File Info": ["name", "format"],
                    "Size Details": ["name", "size", "document"],
                },
                "known_results": {
                    "csv_files": [
                        "Dataset 1: sales data-set.csv (Quality Verified - Original CSV)",
                        "Dataset 2: Features data set.csv (Quality Enhanced - CSV Cleaned)", 
                        "Dataset 3: stores data-set.csv (Quality Verified - Original CSV)"
                    ],
                    "formats": ["csv", "png", "ipynb", "log"]
                }
            },
            "Generated Outputs": {
                "entity": "UsedData",
                "description": "Explore charts, notebooks and other outputs",
                "filters": {
                    "Visualizations": {"query_part": "where format = \"png\"", "description": "Show generated charts and plots"},
                    "Notebooks": {"query_part": "where format = \"ipynb\"", "description": "Show Jupyter notebooks"},
                    "All Outputs": {"query_part": "", "description": "Show all generated files"}
                },
                "fields": {
                    "Names Only": ["name"],
                    "With Format": ["name", "format"],
                    "Complete Info": ["name", "format", "size", "producer"]
                },
                "known_results": {
                    "png_files": [
                        "Chart: Figure 1 - no model - Gain some graphical insight",
                        "Chart: Figure 2 - no model - Forecast of the total sales volume",
                        "Chart: Figure 3 - no model - Model definition",
                        "Chart: Figure 4 - no model - Forecast of the store-wise sales volume",
                        "Chart: Figure 5 - no model - Look for predictive power from external variables"
                    ]
                }
            },
            "Process Execution": {
                "entity": "Action",
                "description": "Explore notebook execution and data processing",
                "filters": {
                    "Completed Actions": {"query_part": "where status = \"Completed\"", "description": "Show completed processes"},
                    "Main Notebook": {"query_part": "where name = \"Action - Notebook - Retail sales forecast\"", "description": "Show main analysis action"},
                    "All Actions": {"query_part": "", "description": "Show all actions"}
                },
                "fields": {
                    "Status": ["name", "status"],
                    "Data Flow": ["name", "inputData", "outputData"],
                    "Complete": ["name", "status", "inputData", "outputData", "madeBy"]
                },
                "known_results": {
                    "main_action": {
                        "name": "Action - Notebook - Retail sales forecast",
                        "status": "Completed",
                        "inputData": "Analysis of 3 datasets: sales data-set.csv, Features data set.csv, stores data-set.csv",
                        "outputData": "Generated 7 outputs including models and visualizations"
                    }
                }
            },
            "Validation Results": {
                "entity": "Consensus",
                "description": "Check validation and approval status",
                "filters": {
                    "Approved Only": {"query_part": "where result = \"approved\"", "description": "Show approved validations"},
                    "All Validations": {"query_part": "", "description": "Show all validation results"}
                },
                "fields": {
                    "Results": ["result", "agreementLevel"],
                    "Details": ["name", "result", "typeConsensus"],
                    "Complete": ["name", "result", "agreementLevel", "typeConsensus", "resolvedBy"]
                },
                "known_results": {
                    "validation": {
                        "result": "approved",
                        "agreementLevel": 100,
                        "typeConsensus": "Individual Review"
                    }
                }
            }
        }
    
    else:  # student project
        return {
            "Project Information": {
                "entity": "Project",
                "description": "Explore project metadata and details",
                "filters": {
                    "None": {"query_part": "", "description": "Show all project info"},
                },
                "fields": {
                    "Basic Info": ["createdBy"],
                    "Project Info": ["qualifiedName", "startDate"]
                },
                "known_values": {
                    "name": "Student Performance Analysis",
                    "createdBy": "joelknapp"
                }
            },
            "Input Dataset": {
                "entity": "UsedData", 
                "description": "Explore the student performance dataset",
                "filters": {
                    "CSV Data": {"query_part": "where format = \"csv\"", "description": "Show the main dataset"},
                },
                "fields": {
                    "File Info": ["name", "format", "size"],
                },
                "known_results": {
                    "dataset": {
                        "name": "Dataset 1: Student_performance_data _.csv (Quality Verified - Original CSV)",
                        "size": 166901,
                        "qualityScore": 100.0
                    }
                }
            },
            "Machine Learning Models": {
                "entity": "UsedData",
                "description": "Explore generated ML models", 
                "filters": {
                    "Models Only": {"query_part": "where format = \"pickle\"", "description": "Show ML model files"},
                    "All Models": {"query_part": "where name contains \"Model\"", "description": "Show all model entities"}
                },
                "fields": {
                    "Model Names": ["name"],
                    "Model Details": ["name", "format", "size"],
                },
                "known_results": {
                    "models": [
                        "Model: SVC", "Model: RandomForestClassifier", "Model: AdaBoostClassifier",
                        "Model: KNeighborsClassifier", "Model: CatBoostClassifier", "Model: XGBClassifier", 
                        "Model: GradientBoostingClassifier", "Model: LGBMClassifier", "Model: DecisionTreeClassifier"
                    ]
                }
            },
            "Analysis Charts": {
                "entity": "UsedData",
                "description": "Explore visualization outputs",
                "filters": {
                    "Charts Only": {"query_part": "where format = \"png\"", "description": "Show generated charts"},
                },
                "fields": {
                    "Chart Names": ["name"],
                    "Chart Details": ["name", "format", "size"]
                },
                "known_results": {
                    "charts": [
                        "Chart: Figure 1 - KNeighborsClassifier - Correlation Among Features",
                        "Chart: Figure 2 - KNeighborsClassifier - Selecting a Classification Model",
                        "Chart: Figure 3 - KNeighborsClassifier - Model Evaluation",
                        "Chart: Figure 4 - SVC - Model Evaluation (again)",
                        "Chart: Figure 5 - GradientBoostingClassifier - Reducing Dimensionality"
                    ]
                }
            },
            "Process Execution": {
                "entity": "Action",
                "description": "Explore notebook execution details",
                "filters": {
                    "Main Analysis": {"query_part": "where name = \"Action - Notebook - Student Performance Analysis\"", "description": "Show main analysis action"},
                },
                "fields": {
                    "Execution": ["qualifiedName", "status"],
                    "Data Summary": ["inputData", "outputData"],
                    "Complete": ["qualifiedName", "status", "inputData", "outputData"]
                },
                "known_results": {
                    "action": {
                        "qualifiedName": "notebook-student-performance-analysis.ipynb-v1@StudentPerformanceAn",
                        "status": "Completed", 
                        "inputData": "Analysis of 1 datasets: Student_performance_data _.csv",
                        "outputData": "Generated 16 outputs including models and visualizations"
                    }
                }
            }
        }

def build_interactive_query(category, options, proyecto):
    """Construye la consulta de forma interactiva"""
    
    st.write(f"**{options['description']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Selector de filtro
        filter_option = st.selectbox(
            "Filter by:",
            list(options['filters'].keys()),
            help="Choose how to filter the results"
        )
        
        filter_info = options['filters'][filter_option]
        st.caption(filter_info['description'])
    
    with col2:
        # Selector de campos
        field_option = st.selectbox(
            "Show fields:",
            list(options['fields'].keys()),
            help="Choose which fields to display"
        )
        
        selected_fields = options['fields'][field_option]
    
    # Construir la query
    entity = options['entity']
    filter_part = options['filters'][filter_option]['query_part']
    fields_part = ", ".join(selected_fields)
    
    if filter_part:
        query = f"from {entity} {filter_part} select {fields_part}"
    else:
        query = f"from {entity} select {fields_part}"
    
    # Mostrar query generada
    st.subheader("Generated DSL Query")
    st.code(query, language="sql")