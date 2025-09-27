import streamlit as st
import streamlit.components.v1 as components
import os
import requests
from requests.auth import HTTPBasicAuth



def show(proyecto):
    """Step 4: Taxonomy Queries"""
    st.header("📈 Step 4: Taxonomy Queries")

    st.markdown("""
    The entities generated in the previous step are imported into Atlas and the content is explored. 
    Once the RPCM entities and instances have been ingested into Apache Atlas, you can explore them through queries.
    """)

    tab1, tab2 = st.tabs(["🔍 Interactive Query Builder", "🌐 Atlas Interface"])
    
    with tab1:
        show_interactive_query_builder(proyecto)
    
    with tab2:
        show_atlas_interface()
        

def show_atlas_interface():
    st.subheader("Atlas Web Interface")
    st.markdown("Explore the full Atlas interface with all imported entities:")

    # Detect host environment
    host_ip = os.getenv('HOST_IP', 'localhost')
    
    # Determine proxy URL
    if host_ip.startswith(('http://', 'https://')):
        # HOST_IP is a complete URL (Codespaces case)
        proxy_url = host_ip
        env_message = "Detected Codespace environment: using Option 3 (CODESPACE_NAME) automatically."
    else:
        # HOST_IP is an IP (local case)
        proxy_url = f"http://{host_ip}:8502"
        env_message = ("Running locally: using Option 2 (Machine IP address) by default, "
                       "which is similar to localhost but accessible from other devices on the same network.")

    print(f"Using proxy URL: {proxy_url}")

    # Show environment info
    st.info(
        f"Depending on where you are running Atlas, there are three main ways to access the web interface:\n\n"
        f"1. **localhost** – accessible only from this machine.\n"
        f"2. **Machine IP address** – accessible from other devices on the same network.\n"
        f"3. **CODESPACE_NAME** – accessible via the public URL provided by GitHub Codespaces.\n\n"
        f"{env_message}"
    )
    
    # Show login and link
    st.markdown(
        f"""
        **Username:** `admin`  
        **Password:** `admin`

        <a href="{proxy_url}" target="_blank">🔗 Open Atlas in a new window</a>  
        """,
        unsafe_allow_html=True
    )

    # Embed Atlas in iframe
    components.iframe(
        src=proxy_url,
        width=1400,
        height=800,
        scrolling=True
    )


def show_interactive_query_builder(proyecto):
    st.subheader("Interactive DSL Query Builder")
    st.markdown("Build queries by selecting from available options in your data:")
    
    # Get the options available for this project
    query_options = get_query_options(proyecto)
    
    # Query type selector
    query_category = st.selectbox(
        "What do you want to explore?",
        list(query_options.keys())
    )
    
    if query_category:
        build_interactive_query(query_category, query_options[query_category], proyecto)

def get_query_options(proyecto):
    
    if proyecto == "retail" or "retail" in proyecto.lower():
        return {
            "Project Information": {
                "entity": "Project",
                "description": "Explore project metadata and details",
                "filters": {
                    "Project": {
                        "query_part": "", 
                        "description": "Show all project info", 
                        "entity": "Project",
                        "fields": {
                            "Basic Info": ["name", "createdBy"],
                            "Keywords": ["name", "keywords"], 
                            "Timeline": ["name", "startDate", "endDate"]
                        }
                    },
                    "Consensus": {
                        "query_part": "", 
                        "description": "Show consensus validation data", 
                        "entity": "Consensus",
                        "fields": {
                            "Complete": ["agreementLevel", "qualifiedName", "result", "typeConsensus"]
                        }
                    }
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
                    "CSV Files Only": {"query_part": "WHERE format = \"csv\"", "description": "Show only CSV datasets"},
                    "Large Files (>1MB)": {"query_part": "WHERE size > 1000000", "description": "Show files larger than 1MB"},
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
                    "Visualizations": {"query_part": "WHERE format = \"png\"", "description": "Show generated charts and plots"},
                    "Notebooks": {"query_part": "WHERE format = \"ipynb\"", "description": "Show Jupyter notebooks"},
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
                    "Completed Actions": {"query_part": "WHERE status = \"Completed\"", "description": "Show completed processes"},
                    "Main Notebook": {"query_part": "WHERE name = \"Action - Notebook - Retail sales forecast\"", "description": "Show main analysis action"},
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
                    "Approved Only": {"query_part": "WHERE result = \"approved\"", "description": "Show approved validations"},
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
                    "Project": {
                        "query_part": "", 
                        "description": "Show all project info", 
                        "entity": "Project",
                        "fields": {
                            "Basic Info": ["createdBy"],
                            "Project Info": ["qualifiedName", "startDate"]
                        }
                    },
                    "Consensus": {
                        "query_part": "", 
                        "description": "Show consensus validation data", 
                        "entity": "Consensus",
                        "fields": {
                            "Complete": ["agreementLevel", "qualifiedName", "result", "typeConsensus"]
                        }
                    }
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
                    "CSV Data": {"query_part": "WHERE format = \"csv\"", "description": "Show the main dataset"},
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
                    "Models Only": {"query_part": "WHERE format = \"pickle\"", "description": "Show ML model files"},
                    "All Models": {"query_part": "WHERE name contains \"Model\"", "description": "Show all model entities"}
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
                    "Charts Only": {"query_part": "WHERE format = \"png\"", "description": "Show generated charts"},
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
                    "Main Analysis": {"query_part": "WHERE name = \"Action - Notebook - Student Performance Analysis\"", "description": "Show main analysis action"},
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
    """Build the query interactively"""
    
    st.write(f"**{options['description']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Filter selector
        filter_option = st.selectbox(
            "Filter by:",
            list(options['filters'].keys()),
            help="Choose how to filter the results"
        )
        
        filter_info = options['filters'][filter_option]
        st.caption(filter_info['description'])
    
    with col2:
        # Field selector - use fields from the selected filter
        available_fields = filter_info.get('fields', options.get('fields', {}))
        field_option = st.selectbox(
            "Show fields:",
            list(available_fields.keys()),
            help="Choose which fields to display"
        )
        
        selected_fields = available_fields[field_option]
    
    # Build the query - use entity from filter if available, otherwise use default entity
    if 'entity' in filter_info:
        entity = filter_info['entity']
    else:
        entity = options['entity']
        
    filter_part = filter_info['query_part']
    fields_part = ", ".join(selected_fields)
    
    # To display the queries vertically
    if filter_part:
        query_display = f"SELECT {fields_part}\nFROM {entity}\n{filter_part}"
    else:
        query_display = f"SELECT {fields_part}\nFROM {entity}"
    
    st.subheader("DSL Query (visual)")
    st.code(query_display, language="sql")
    
    # To send to the API
    if filter_part:
        query_api = f"FROM {entity} {filter_part} SELECT {fields_part}"
    else:
        query_api = f"FROM {entity} SELECT {fields_part}"
    
    if st.button("Run Query"):
        results = execute_atlas_query(query_api)
        
        st.subheader("Query Results")
        
        if "error" in results:
            st.error(results["error"])
            if "details" in results:
                st.text(results["details"])
        else:
            # Show response in JSON 
            if "entities" in results:
                st.json(results["entities"])
            else:
                st.json(results)



    
def execute_atlas_query(query):
    """Execute the DSL query against the Apache Atlas API"""
    
    # Atlas URL 
    host_ip = os.getenv('HOST_IP', 'localhost')
    atlas_url = f"http://{host_ip}:21000/api/atlas/v2/search/dsl"
    
    try:
        response = requests.get(
            atlas_url,
            params={"query": query},
            auth=HTTPBasicAuth("admin", "admin")  # default credentials
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Atlas API returned {response.status_code}", "details": response.text}
    
    except Exception as e:
        return {"error": str(e)}