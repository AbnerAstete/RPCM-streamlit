import streamlit as st
import plotly.express as px
import pandas as pd
import json
import time
import os

def get_project_paths(proyecto):
    """Get file paths based on project selection"""
    
    if proyecto == "Student Performance Analysis":
        project_folder = "student"
    elif proyecto == "Retail Data Analytics":
        project_folder =  "retail"
    
    base_path = f"assets/jsons/metadata_extraction/{project_folder}"
    return {
        "log_analysis": f"{base_path}/log_analysis.json",
        "kernel_metadata": f"{base_path}/kernel_metadata.json",
        "insights_notebook": f"{base_path}/insights_notebook.json",
        "entities_kaggle": f"{base_path}/entities_kaggle.json"
    }


def load_json_file(file_path, default_data=None):
    """Safely load JSON file with error handling"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            st.warning(f"File not found: {file_path}")
            return default_data if default_data else {}
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return default_data if default_data else {}


def show_extraction_process(notebook, metadata, outputs, proyecto, paths):
    """Show the interactive extraction process with real data"""
    
    st.subheader("Extraction in Progress...")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    extracted_data = {}
    step = 0
    total_steps = sum([notebook, metadata, outputs])
    
    # Project Metadata extraction
    if metadata:
        step += 1
        progress_bar.progress(step / total_steps)
        status_text.text(f"Extracting project metadata... ({step}/{total_steps})")
        time.sleep(1)
        
        st.subheader("📋 Project Metadata Extraction Results")
        metadata_data = load_json_file(paths["kernel_metadata"])
        extracted_data['project_metadata'] = metadata_data
        show_project_metadata_results(metadata_data)
    
    # Notebook extraction
    if notebook:
        step += 1
        progress_bar.progress(step / total_steps)
        status_text.text(f"Extracting notebook insights... ({step}/{total_steps})")
        time.sleep(1)
        
        st.subheader("📓 Notebook Extraction Results")
        notebook_data = load_json_file(paths["insights_notebook"])
        extracted_data['notebook_insights'] = notebook_data
        show_notebook_results(notebook_data)
    
    # Outputs extraction
    if outputs:
        step += 1
        progress_bar.progress(step / total_steps)
        status_text.text(f"Extracting execution outputs... ({step}/{total_steps})")
        time.sleep(1)
        
        st.subheader("📊 Output Extraction Results")
        output_data = load_json_file(paths["log_analysis"])
        extracted_data['output_analysis'] = output_data
        show_output_results(output_data)
    
    # Completion
    progress_bar.progress(1.0)
    status_text.text("Extraction completed successfully!")

    # Show consolidated results ONLY if all 3 sources were extracted
    if notebook and metadata and outputs:
        show_consolidated_metadata(extracted_data, proyecto, paths)
    else:
        st.info("ℹ️ Consolidated Kaggle Metamodel is only available when all three metadata sources are extracted.")


def show_project_metadata_results(data):
    """Display project metadata in a business-friendly format"""
    
    if not data:
        st.warning("No project metadata available")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Project ID", f"#{data.get('id_no', 'N/A')}")
    with col2:
        st.metric("Language", data.get('language', 'N/A').title())
    with col3:
        st.metric("Type", data.get('kernel_type', 'N/A').title())
    with col4:
        privacy = "🔒 Private" if data.get('is_private', False) else "🌐 Public"
        st.metric("Visibility", privacy)
    
    # Project details
    with st.container(border=True):
        st.markdown("### Project Information")
        st.markdown(f"**Title:** {data.get('title', 'N/A')}")
        st.markdown(f"**Author:** {data.get('id', 'N/A').split('/')[0] if '/' in data.get('id', '') else 'N/A'}")
        st.markdown(f"**Kaggle ID:** `{data.get('id', 'N/A')}`")
        st.markdown(f"**Code File:** {data.get('code_file', 'N/A')}")
        
        if data.get('dataset_sources'):
            st.markdown("**Data Sources:**")
            for source in data['dataset_sources']:
                st.markdown(f"• {source}")
        
        # Configuration inline
        st.markdown("**Runtime Configuration:**")
        config_col1, config_col2, config_col3 = st.columns(3)
        
        with config_col1:
            gpu_icon = "✅" if data.get('enable_gpu', False) else "❌"
            st.markdown(f"**GPU:** {gpu_icon}")
        with config_col2:
            tpu_icon = "✅" if data.get('enable_tpu', False) else "❌"
            st.markdown(f"**TPU:** {tpu_icon}")
        with config_col3:
            internet_icon = "✅" if data.get('enable_internet', False) else "❌"
            st.markdown(f"**Internet:** {internet_icon}")


def show_notebook_results(data):
    """Display notebook analysis results"""
    
    if not data:
        st.warning("No notebook insights available")
        return
    
    # Key insights metrics
    col1, col2, col3= st.columns(3)
    
    with col1:
        st.metric("ML Models", len(data.get('models', [])))
    with col2:
        st.metric("Visualizations", len(data.get('graphs', [])))
    with col3:
        st.metric("Analysis Sections", len(data.get('sections', [])))
    
    # Models used
    if data.get('models'):
        with st.container(border=True):
            st.markdown("### Machine Learning Models")
            
            models_per_row = 3
            models = data['models']
            for i in range(0, len(models), models_per_row):
                cols = st.columns(models_per_row)
                for j, model in enumerate(models[i:i+models_per_row]):
                    with cols[j]:
                        st.button(model, disabled=True, use_container_width=True)
            
            # Visualizations inline
            if data.get('graphs'):
                st.markdown("**Generated Visualizations:**")
                for graph in data['graphs']:
                    st.markdown(f"• **{graph.get('name', 'N/A')}** - {graph.get('section', 'N/A')} ({graph.get('model', 'N/A')})")


def show_output_results(data):
    """Display output analysis results"""
    
    if not data:
        st.warning("No output analysis available")
        return
    
    file_info = data.get('file_info', {})
    execution_time = data.get('execution_time', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        duration = execution_time.get('duration_seconds', 0)
        st.metric("Execution Time", f"{duration:.3f}s")
    with col2:
        total_bytes = file_info.get('total_bytes', 0)
        st.metric("Log File Size", f"{total_bytes:,} bytes")
    with col3:
        num_lines = file_info.get('num_lines', 0)
        st.metric("Log Lines", num_lines)
    
    with st.container(border=True):
        st.markdown("### Generated Files")
        st.markdown(f"**Log File:** {file_info.get('filename', 'N/A')}")
        created_at = file_info.get('created_at', '')
        if created_at:
            formatted_date = created_at[:19].replace('T', ' ')
            st.markdown(f"**Created:** {formatted_date}")
        st.markdown(f"**Encoding:** {file_info.get('encoding', 'N/A')}")
        st.markdown(f"**Path:** `{file_info.get('filepath', 'N/A')}`")


def show_consolidated_metadata(extracted_data, proyecto, paths):
    """Show the consolidated metadata results"""
    
    st.markdown("---")
    st.subheader("🏗️ Consolidated Kaggle Metamodel")
    
    st.markdown("""
    All extracted metadata has been consolidated into our standardized Kaggle project metamodel. 
    This unified structure is ready for transformation to RPCM entities in Step 3.
    """)
    
    tab1, tab2 = st.tabs(["Summary View", "Download JSON"])
    
    with tab1:
        show_metamodel_summary(extracted_data, paths)
    
    with tab2:
        # Load and display the entities-kaggle.json file
        entities_data = load_json_file(paths["entities_kaggle"])
        
        if entities_data:
            json_str = json.dumps(entities_data, indent=2)
            
            
            st.code(json_str[:500] + "...", language="json")
            st.download_button(
                label="⬇️ Download Kaggle Entities JSON",
                data=json_str,
                file_name=f"{proyecto.lower().replace(' ', '_')}_entities.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.warning("Entities data not available for download")




def show_metamodel_summary(data, paths):
    """Show a summary of the metamodel structure with entity mapping"""
    
    # Load the entities-kaggle.json data dynamically
    entities_data = load_json_file(paths["entities_kaggle"])
    
    if not entities_data:
        st.warning("No entities data available for metamodel summary")
        return
    
    st.markdown("### Kaggle Metamodel Entities")
    st.markdown("The extracted metadata has been structured into the following entities:")
    
    # Create entity cards
    col1, col2 = st.columns(2)
    
    with col1:
        # Project & Owner entities
        with st.container(border=True):
            st.markdown("**Project Context**")
            project_title = entities_data.get('Project', {}).get('title', 'N/A')
            owner_name = entities_data.get('Owner', {}).get('name', 'N/A')
            notebook_file = entities_data.get('Notebook', {}).get('file', 'N/A')
            
            st.markdown(f"• **Project:** {project_title}")
            st.markdown(f"• **Owner:** {owner_name}")
            st.markdown(f"• **Notebook:** {notebook_file}")
        
        # Data entities
        with st.container(border=True):
            st.markdown("**Data Assets**")
            
            files = entities_data.get('File', [])
            for file in files:
                if isinstance(file, dict):
                    name = file.get('name', 'N/A')
                    size_mb = file.get('totalbytes', 0) / (1024*1024)
                    st.markdown(f"• **File:** {name} ({size_mb:.1f} MB)")
            
            datasets = entities_data.get('DataSets', [])
            for dataset in datasets:
                if isinstance(dataset, dict):
                    title = dataset.get('title', 'N/A')
                    st.markdown(f"• **Dataset:** {title[:50]}...")
    
    with col2:
        # Code & Analysis entities
        with st.container(border=True):
            st.markdown("**Analysis Components**")
            
            code_line = entities_data.get('CodeLine', {})
            models = code_line.get('models', [])
            graphs = code_line.get('graphs', [])
            
            st.markdown(f"• **Models:** {len(models)} ML algorithms")
            st.markdown(f"• **Visualizations:** {len(graphs)} figures")
            
            # Show top 3 models
            if models:
                top_models = models[:3]
                for model in top_models:
                    st.markdown(f"  - {model}")
                if len(models) > 3:
                    st.markdown(f"  - +{len(models) - 3} more")
        
        # Output entities
        with st.container(border=True):
            st.markdown("**Generated Outputs**")
            
            log_info = entities_data.get('Log', {})
            log_filename = log_info.get('filename', 'N/A')
            log_bytes = log_info.get('total_bytes', 0)
            log_size_kb = log_bytes / 1024 if log_bytes else 0
            
            st.markdown(f"• **Log:** {log_filename}")
            st.markdown(f"• **Size:** {log_size_kb:.1f} KB")